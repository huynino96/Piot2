from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
from marshmallow_sqlalchemy import ModelSchema

db.metadata.clear()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    passwordHashed = db.Column(db.String(128))

    def setPassword(self, password):
        self.passwordHashed = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.passwordHashed, password)


db.create_all()


class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    userName = db.Column(db.String(100), unique=True, nullable=False)


class Car(db.Model):
    carId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plateNumber = db.Column(db.String(100), nullable=False)
    make = db.Column(db.String(100), nullable=False)
    bodyType = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    costPerHour = db.Column(db.Integer, nullable=False)

class CarSchema(ModelSchema):
    class Meta:
        model = Car


class BorrowedCar(db.Model):
    borrowedId = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    carId = db.Column(db.Integer, db.ForeignKey('Car.carId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('User.userId'), nullable=False)
    status = db.Column(db.Enum('borrowed', 'returned'), nullable=True)
    borrowedDate = db.Column(db.DateTime, nullable=False)
    returnedDate = db.Column(db.DateTime, nullable=True)


# This function will generate data for creating graph about borrowed and returned books
def getDailyAnalytics():
    # Group the number of borrowed books per day
    totalBorrowed = db.session.query(sa.func.date_format(BorrowedCar.borrowed_date, '%d-%m-%Y'),
                                      sa.func.count(BorrowedCar.borrowed_date)) \
        .group_by(sa.func.date_format(BorrowedCar.borrowed_date, '%d-%m-%Y')).all()

    # Group the number of returned books per day
    totalReturned = db.session.query(sa.func.date_format(BorrowedCar.returned_date, '%d-%m-%Y'),
                                      sa.func.count(BorrowedCar.borrowed_date),
                                      sa.func.count(BorrowedCar.returned_date)) \
        .filter(BorrowedCar.returned_date != None) \
        .group_by(sa.func.date_format(BorrowedCar.returned_date, '%d-%m-%Y')).all()

    # Convert to dictionary instead of tuples
    totalBorrowed = [{"date": item[0], "count": item[1]} for item in totalBorrowed]
    totalReturned = [{"date": item[0], "count": item[1]} for item in totalReturned]
    totalData = dict()

    # Join two dataset to create an array containing
    # the number of borrow and returned book in a day
    for item in totalBorrowed:
        totalData[item["date"]] = {"borrowCount": item["count"], "returnCount": 0}

    for item in totalReturned:
        if item["date"] in totalData:
            totalData[item["date"]]["returnCount"] = item["count"]
        else:
            totalData[item["date"]] = {"borrowCount": 0, "returnCount": item["count"]}
    result = []
    for key in totalData.keys():
        result.append({"date": key, "borrowCount": totalData[key]["borrowCount"],
                       "returnCount": totalData[key]["returnCount"]})

    # Return the data as an array of dictionary object
    return result


# The same as above, but for monthly data
def getMonthlyAnalytics():
    # Get total returns and borrows per day
    totalBorrowed = db.session.query(sa.func.date_format(BorrowedCar.borrowed_date, '%m-%Y'),
                                      sa.func.count(BorrowedCar.borrowed_date)) \
        .group_by(sa.func.date_format(BorrowedCar.borrowed_date, '%m-%Y')).all()
    totalReturned = db.session.query(sa.func.date_format(BorrowedCar.returned_date, '%m-%Y'),
                                      sa.func.count(BorrowedCar.borrowed_date),
                                      sa.func.count(BorrowedCar.returned_date)) \
        .filter(BorrowedCar.returned_date != None) \
        .group_by(sa.func.date_format(BorrowedCar.returned_date, '%m-%Y')).all()

    # Send it to front end as json
    totalBorrowed = [{"month": item[0], "count": item[1]} for item in totalBorrowed]
    totalReturned = [{"month": item[0], "count": item[1]} for item in totalReturned]
    totalData = dict()

    # Join two dataset
    for item in totalBorrowed:
        totalData[item["month"]] = {"borrowCount": item["count"], "returnCount": 0}

    for item in totalReturned:
        if item["month"] in totalData:
            totalData[item["month"]]["returnCount"] = item["count"]
        else:
            totalData[item["month"]] = {"borrowCount": 0, "returnCount": item["count"]}

    # Change back to array
    result = []
    for key in totalData.keys():
        result.append({"month": key, "borrowCount": totalData[key]["borrowCount"],
                       "returnCount": totalData[key]["returnCount"]})

    return result


carsSchema = CarSchema(many=True)
carSchema = CarSchema()