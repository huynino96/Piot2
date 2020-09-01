import flask_sqlalchemy
import flask_marshmallow

db = flask_sqlalchemy.SQLAlchemy()
marsh = flask_marshmallow.Marshmallow()


class Car(db.Model):
    __tablename__ = "Car"
    CarId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PlateNumber = db.Column(db.String(256))
    Make = db.Column(db.Text)
    BodyType = db.Column(db.Text)
    Color = db.Column(db.Text)
    Seats = db.Column(db.Integer)
    Location = db.Column(db.Text)
    CostPerHour = db.Column(db.Integer)

    def __init__(self, plateNumber, make, bodyType, color, seats, location, costPerHour, carId=None):
        self.carId = carId
        self.plateNumber = plateNumber
        self.make = make
        self.bodyType = bodyType
        self.color = color
        self.seats = seats
        self.location = location
        self.costPerHour = costPerHour


class CarSchema(marsh.Schema):

    def __init__(self, strict=True, **kwargs):
        super().__init__(strict=strict, **kwargs)

    class Meta:
        # Fields to expose.
        fields = ("CarId", "PlateNumber", "Make", "BodyType", "Color", "Seats", "Location", "CostPerHour")
