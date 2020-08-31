from carModel import db, Car, CarSchema
from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

carSchema = CarSchema()
carsSchema = CarSchema(many=True)


class RestApi:
    # Get all Cars
    @staticmethod
    @api.route("/car", methods=["GET"])
    def getCar():
        car = Car.query.all()
        result = carsSchema.dump(car)
        return jsonify(result.data)

    @staticmethod
    # Get one car by ID.
    @api.route("/car/<id>", methods=["GET"])
    def getCar(id):
        car = Car.query.get(id)
        return carSchema.jsonify(car)

    @staticmethod
    # Create New Car
    @api.route("/car", methods=["POST"])
    def addBook():
        make = request.json["Make"]
        bodyType = request.json["BodyType"]
        color = request.json["Color"]
        seats = request.json["Seats"]
        location = request.json["Location"]
        costPerHour = request.json["CostPerHour"]

        newCar = Car(make=make, bodyType=bodyType, color=color, seats=seats, location=location, costPerHour=costPerHour)
        db.session.add(newCar)
        db.session.commit()
        return carSchema.jsonify(newCar)

    @staticmethod
    # Update one Car
    @api.route("/car/<id>", methods=["PUT"])
    def bookUpdate(id):
        car = Car.query.get(id)
        make = request.json["Make"]
        bodyType = request.json["BodyType"]
        color = request.json["Color"]
        seats = request.json["Seats"]
        location = request.json["Location"]
        costPerHour = request.json["CostPerHour"]

        # Update Car
        car.make = make
        car.bodyType = bodyType
        car.color = color
        car.seats = seats
        car.location = location
        car.costPerHour = costPerHour
        db.session.commit()
        return carSchema.jsonify(car)

    @staticmethod
    # Delete Car by ID
    @api.route("/car/<id>", methods=["DELETE"])
    def bookDelete(id):
        car = Car.query.get(id)
        db.session.delete(car)
        db.session.commit()
        return carSchema.jsonify(car)
