from app import app, basic_auth, db
from app.models import Car, User, getMonthlyAnalytics, getDailyAnalytics, carsSchema, usersSchema
from flask import jsonify, request, render_template, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
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


@app.route("/auth/login", methods=["POST"])
def login():
    userName = request.json["userName"]
    password = request.json["password"]

    # Validation
    if not userName:
        raise BadRequest("Username must be provided", 300)
    if not password:
        raise BadRequest("Password must be provided", 300)

    # Get user information
    user = User.query.filter_by(userName=userName).first()

    # Check user is valid or not
    if (not user):
        raise BadRequest("User is not existed in database");

    # Check password is match into database or not
    if (not check_password_hash(user.password, password)):
        raise BadRequest("Password is not matched")

    # Put user information into jwt
    access_token = jwt.encode({'userName': userName}, 'secret')

    # Return jwt
    return jsonify({ "success": True, "access_token": access_token.decode('utf-8') })

@app.route("/auth/register", methods=["POST"])
def register():
    firstName = request.json["firstName"]
    lastName = request.json["lastName"]
    email = request.json["email"]
    userName = request.json["userName"]
    password = request.json["password"]

    # Validation
    if not firstName:
        raise BadRequest("First Name must be provided", 300)
    if not lastName:
        raise BadRequest("Last Name must be provided", 300)
    if not email:
        raise BadRequest("Email must be provided", 300)
    if not userName:
        raise BadRequest("Username must be provided", 300)
    if not password:
        raise BadRequest("Password must be provided", 300)


    # Check user is valid or not
    if (User.query.filter_by(userName=userName).first()):
        raise BadRequest("User is already existed");

    # Create ser
    user = User(firstName=firstName, lastName=lastName, userName=userName, email=email, password=generate_password_hash(password))

    # Try to save to db
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)})

    # Put user information into jwt
    access_token = jwt.encode({ 'userName': userName }, 'secret')

    # Return jwt
    return jsonify({ "success": True, "access_token": access_token.decode('utf-8') })

@app.route("/cars")
@app.route("/cars/<int:page>")
def cars(page=1):
    allCars = Car.query.paginate(page, per_page=5)
    return jsonify({
        "cars": carsSchema.dump(allCars.items),
        "has_next": allCars.has_next,
        "has_prev": allCars.has_prev
    })


@app.route("/cars", methods=["POST"])
def add_cars():
    # Create car object
    plateNumber = request.json["plateNumber"]
    make = request.json["make"]
    bodyType = request.json["bodyType"]
    color = request.json["color"]
    seats = request.json["seats"]
    location = request.json["location"]
    costPerHour = request.json["costPerHour"]

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
    car = Car(plateNumber=plateNumber, make=make, bodyType=bodyType, color=color, seats=seats, location=location, costPerHour=costPerHour)

    # Try to save to db
    try:
        db.session.add(car)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"success": True, "id": car.carId})

@app.route("/cars/<int:id>", methods=["PUT"])
def update_cars(id):
    # Create car object
    plateNumber = request.json["plateNumber"]
    make = request.json["make"]
    bodyType = request.json["bodyType"]
    color = request.json["color"]
    seats = request.json["seats"]
    location = request.json["location"]
    costPerHour = request.json["costPerHour"]

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
    car = Car.query.get(id)
    car.plateNumber = plateNumber
    car.make = make
    car.color = color
    car.seats = seats
    car.location = location
    car.costPerHour = costPerHour

    # Try to save to db
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"success": True, "id": car.carId})

@app.route("/cars/<int:id>", methods=["DELETE"])
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

@app.route("/users")
@app.route("/users/<int:page>")
def users(page=1):
    allUsers = User.query.paginate(page, per_page=5)
    return jsonify({
        "users": usersSchema.dump(allUsers.items),
        "has_next": allUsers.has_next,
        "has_prev": allUsers.has_prev
    })


@app.route("/users", methods=["POST"])
def add_users():
    # Create user object
    firstName = request.json["firstName"]
    lastName = request.json["lastName"]
    userName = request.json["userName"]
    email = request.json["email"]
    password = request.json["password"]

    # Catch error
    if not firstName:
        raise BadRequest("First Name can not be empty", 40002)
    if not lastName:
        raise BadRequest("Last Name can not be empty", 40002)
    if not userName:
        raise BadRequest("User Name can not be empty", 40002)
    if not email:
        raise BadRequest("Email of seats can not be empty", 40002)
    if not password:
        raise BadRequest("Password can not be empty", 40002)

    # Create date
    user = User(firstName=firstName, lastName=lastName, userName=userName, email=email, password=generate_password_hash(password))

    # Try to save to db
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"success": True, "id": user.userId})

@app.route("/users/<int:id>", methods=["PUT"])
def update_users(id):
    # Create user object
    firstName = request.json["firstName"]
    lastName = request.json["lastName"]
    email = request.json["email"]
    userName = request.json["userName"]
    password = request.json["password"]

    # Catch error
    if not firstName:
        raise BadRequest("First Name can not be empty", 40002)
    if not lastName:
        raise BadRequest("Last Name can not be empty", 40002)
    if not userName:
        raise BadRequest("User Name can not be empty", 40002)
    if not email:
        raise BadRequest("Email of seats can not be empty", 40002)
    if not password:
        raise BadRequest("Password can not be empty", 40002)

    # Create date
    user = User.query.get(id)
    user.firstName = firstName
    user.lastName = lastName
    user.email = email
    user.userName = userName
    user.password = generate_password_hash(password)

    # Try to save to db
    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)})
    return jsonify({"success": True, "id": user.userId})

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    if User.query.filter(User.userId == id).count() == 0:
        raise BadRequest("user does not exist", 404)
    else:
        try:
            User.query.filter(User.userId == id).delete()
            db.session.commit()
        except Exception as e:
            return jsonify({"error": str(e)})
        return jsonify({"success": True, "id": id})


@app.route("/analytics/daily")
def dailyAnalytics():
    result = getDailyAnalytics()
    return jsonify(result)


@app.route("/analytics/monthly")
def monthlyAnalytics():
    result = getMonthlyAnalytics()
    return jsonify(result)



