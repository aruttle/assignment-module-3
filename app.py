from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

BOOKINGS_FILE = "bookings.json"

# Sample accommodations
accommodations = [
    {"id": 1, "name": "Luxury Yurt", "price": 120, "available": True, "image": "yurt.jpg"},
    {"id": 2, "name": "Eco Cabin", "price": 150, "available": False, "image": "cabin.jpg"},
    {"id": 3, "name": "Treehouse", "price": 180, "available": True, "image": "treehouse.jpg"},
]

# Fallback for image
for acc in accommodations:
    acc.setdefault("image", "default.jpg")

# Load bookings from file
def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "r") as f:
            return json.load(f)
    return []

# Save bookings to file
def save_booking(booking):
    bookings = load_bookings()
    bookings.append(booking)
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=4)

@app.route("/")
def home():
    return render_template("home.html", accommodations=accommodations)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        print(f"New message from {name} ({email}): {message}")
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)

from datetime import datetime

@app.route("/book/<int:acc_id>", methods=["GET", "POST"])
def book(acc_id):
    acc = next((a for a in accommodations if a["id"] == acc_id), None)
    if not acc or not acc["available"]:
        return "Accommodation not available", 400

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            start_date_str = request.form["start_date"]
            end_date_str = request.form["end_date"]

            # Convert strings to datetime.date objects
            check_in_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # Validate date range
            if check_out_date <= check_in_date:
                return "Check-out date must be after check-in date.", 400

        except Exception as e:
            return f"Error processing booking: {e}", 400

        acc["available"] = False
        print(f"Booking confirmed for {name} ({email}) from {check_in_date} to {check_out_date} at {acc['name']}")
        return redirect(url_for("home"))

    return render_template("booking.html", accommodation=acc)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
