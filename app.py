from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  # for working with MongoDB ObjectIds
import config

app = Flask(__name__)
app.config["MONGO_URI"] = config.MONGO_URI
app.secret_key = config.SECRET_KEY

mongo = PyMongo(app)
db = mongo.db

# HOME route
@app.route("/")
def home():
    return render_template("index.html")

# ROOMS route
@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

# BOOKING page route (GET)
@app.route("/booking", methods=["GET"])
def booking():
    return render_template("booking.html")

# Book route (POST) - processes the booking data
@app.route("/book", methods=["POST"])
def book_now():
    room = request.form.get("room")
    checkin = request.form.get("checkin")
    checkout = request.form.get("checkout")
    guests = request.form.get("guests")
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    requests = request.form.get("requests")

    new_booking = {
        "room": room,
        "checkin": checkin,
        "checkout": checkout,
        "guests": guests,
        "fullname": fullname,
        "email": email,
        "phone": phone,
        "requests": requests
    }
    result = db.bookings.insert_one(new_booking)
    booking_id = str(result.inserted_id)

    return redirect(url_for("confirmation", booking_id=booking_id))

# Confirmation route (GET)
@app.route("/confirmation/<booking_id>")
def confirmation(booking_id):
    # Convert to ObjectId if your _id is truly an ObjectId
    booking_objid = ObjectId(booking_id)
    booking = db.bookings.find_one({"_id": booking_objid})
    return render_template("confirmation.html", booking=booking)

# =========================
# ADMIN ROUTES
# =========================

@app.route("/admin")
def admin_dashboard():
    all_bookings = list(db.bookings.find({}))
    return render_template("admin.html", bookings=all_bookings)

# -- View a single booking
@app.route("/admin/view/<booking_id>", methods=["GET"])
def admin_view_booking(booking_id):
    booking_objid = ObjectId(booking_id)
    booking = db.bookings.find_one({"_id": booking_objid})
    return render_template("admin_view.html", booking=booking)

# -- Edit a single booking
@app.route("/admin/edit/<booking_id>", methods=["GET", "POST"])
def admin_edit_booking(booking_id):
    booking_objid = ObjectId(booking_id)

    if request.method == "POST":
        new_fullname = request.form.get("fullname")
        new_room = request.form.get("room")
        new_checkin = request.form.get("checkin")
        new_checkout = request.form.get("checkout")
        new_guests = request.form.get("guests")
        new_phone = request.form.get("phone")
        new_email = request.form.get("email")
        new_requests = request.form.get("requests")

        db.bookings.update_one(
            {"_id": booking_objid},
            {
                "$set": {
                    "fullname": new_fullname,
                    "room": new_room,
                    "checkin": new_checkin,
                    "checkout": new_checkout,
                    "guests": new_guests,
                    "phone": new_phone,
                    "email": new_email,
                    "requests": new_requests,
                }
            },
        )
        return redirect(url_for("admin_dashboard"))

    # GET case: fetch booking and show edit form
    booking = db.bookings.find_one({"_id": booking_objid})
    return render_template("admin_edit.html", booking=booking)

# -- Delete a single booking
@app.route("/admin/delete/<booking_id>", methods=["POST"])
def admin_delete_booking(booking_id):
    booking_objid = ObjectId(booking_id)
    db.bookings.delete_one({"_id": booking_objid})
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=config.DEBUG)
