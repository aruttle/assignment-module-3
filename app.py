from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

BOOKINGS_FILE = "bookings.json"

# accommodations
accommodations = [
    {"id": 1, "name": "Luxury Yurt", "price": 120, "available": True, "image": "yurt.jpg"},
    {"id": 2, "name": "Eco Cabin", "price": 150, "available": True, "image": "cabin.jpg"},
    {"id": 3, "name": "Treehouse", "price": 180, "available": True, "image": "treehouse.jpg"},
]

# Fallback image
for acc in accommodations:
    acc.setdefault("image", "default.jpg")

# Load bookings from file
def load_bookings():
    if os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "r") as f:
            return json.load(f)
    return []

# Save new booking
def save_booking(new_booking):
    bookings = load_bookings()
    bookings.append(new_booking)
    with open(BOOKINGS_FILE, "w") as f:
        json.dump(bookings, f, indent=2)

# Get booked date ranges for accommodation
def get_booked_dates(acc_name):
    bookings = load_bookings()
    return [
        (
            datetime.strptime(b["check_in"], "%Y-%m-%d").date(),
            datetime.strptime(b["check_out"], "%Y-%m-%d").date()
        )
        for b in bookings if b["accommodation"] == acc_name
    ]

# Error handling for 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", error=error), 404

# Error handling for 500
@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html", error=error), 500

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

@app.route("/book/<int:acc_id>", methods=["GET", "POST"])
def book(acc_id):
    acc = next((a for a in accommodations if a["id"] == acc_id), None)
    if not acc or not acc["available"]:
        return "Accommodation not available", 400

    # Get already booked dates for this accommodation
    booked_dates = get_booked_dates(acc["name"])

    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            start_date_str = request.form["start_date"]
            end_date_str = request.form["end_date"]

            check_in_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            # Validate date range
            if check_out_date <= check_in_date:
                flash("Check-out date must be after check-in date.", "danger")
                return redirect(url_for("book", acc_id=acc_id))

            # Check for date overlap
            for booked_start, booked_end in booked_dates:
                if not (check_out_date <= booked_start or check_in_date >= booked_end):
                    flash("Selected dates are not available. Please choose different dates.", "danger")
                    return redirect(url_for("book", acc_id=acc_id))

            # Save booking
            booking = {
                "accommodation": acc["name"],
                "name": name,
                "email": email,
                "check_in": start_date_str,
                "check_out": end_date_str
            }
            save_booking(booking)

            # Mark as booked (you may later want to remove this if handling availability by date instead)
            acc["available"] = False

            flash("Booking confirmed!", "success")
            return redirect(url_for("home"))

        except Exception as e:
            flash(f"Booking failed: {e}", "danger")
            return redirect(url_for("book", acc_id=acc_id))

    return render_template("booking.html", accommodation=acc, booked_dates=booked_dates)


if __name__ == "__main__":
    app.run(debug=True, port=8080)
