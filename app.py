from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Accommodations
accommodations = [
    {"id": 1, "name": "Luxury Yurt", "price": 120, "available": True},
    {"id": 2, "name": "Eco Cabin", "price": 150, "available": False},
    {"id": 3, "name": "Treehouse", "price": 180, "available": True},
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Booking Route
@app.route('/book/<int:acc_id>', methods=['GET', 'POST'])
def book(acc_id):
    acc = next((a for a in accommodations if a['id'] == acc_id), None)
    if not acc or not acc['available']:
        return "Accommodation not available", 400
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        acc['available'] = False  # Mark as booked
        return redirect(url_for('home'))
    
    return render_template('booking.html', accommodation=acc)

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

if __name__ == '__main__':
    app.run(debug=True, port=8080)


