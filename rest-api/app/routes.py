from app import app, basic_auth, db
from app.carModels import Car, getMonthlyAnalytics, getDailyAnalytics, carsSchema
from flask import jsonify, request, render_template
import re


class BadRequest(Exception):
    """Custom exception class to be thrown when local error occurs."""
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(BadRequest)
def handleBadRequest(error):
    """Catch BadRequest exception globally, serialize into JSON, and respond with 400."""
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400


@app.route("/admin", methods=["GET"])
def admin():
    return render_template("index.html")


@app.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        raise BadRequest("Username must be provided", 300)
    if not password:
        raise BadRequest("Password must be provided", 300)
    if username != app.config.get("BASIC_AUTH_USERNAME") or password != app.config.get("BASIC_AUTH_PASSWORD"):
        raise BadRequest("Invalid username and password", 301)
    else:
        return jsonify({"success": True})


@app.route("/cars")
@app.route("/cars/<int:page>")
@basic_auth.required
def cars(page=1):
    allCars = Car.query.paginate(page, per_page=5)
    return jsonify({
        "cars": carsSchema.dump(allCars.items).data,
        "has_next": allCars.has_next,
        "has_prev": allCars.has_prev
    })


@app.route("/cars/add", methods=["POST"])
def add_cars():
    # Create car object
    plateNumber = request.form["plateNumber"]
    make = request.form["make"]
    bodyType = request.form["bodyType"]
    color = request.form["color"]
    seats = request.form["seats"]
    location = request.form["location"]
    costPerHour = request.form["costPerHour"]

    # Catch error
    if not plateNumber:
        raise BadRequest("Plate Number can not be empty", 40002)
    if not make:
        raise BadRequest("Brand can not be empty", 40002)
    if not color:
        raise BadRequest("Color can not be empty", 40002)
    if not seats:
        raise BadRequest("Numeber of seats can not be empty", 40002)
    if not location:
        raise BadRequest("Car's Location can not be empty", 40002)
    if not costPerHour:
        raise BadRequest("Cost Per Hour can not be empty", 40002)

    # Create date
    car = Car(PlateNumber=plateNumber, Make=make, BodyType=bodyType, Color=color, Seats=seats, Location=location, CostPerHour=costPerHour)

    # Try to save to db
    try:
        db.session.add(car)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"success": True, "id": Car.carId})


@app.route("/cars/delete/<int:id>", methods=["DELETE"])
def delete_car(id):
    if Car.query.filter(Car.carId == id).count() == 0:
        raise BadRequest("car does not exist", 404)
    else:
        try:
            Car.query.filter(Car.carId == id).delete()
            db.session.commit()
        except Exception as e:
            return jsonify({"error": str(e)})
        return jsonify({"success": True, "id": id})


@app.route("/analytics/daily")
@basic_auth.required
def dailyAnalytics():
    result = getDailyAnalytics()
    return jsonify(result)


@app.route("/analytics/monthly")
@basic_auth.required
def monthlyAnalytics():
    result = getMonthlyAnalytics()
    return jsonify(result)



