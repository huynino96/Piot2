from flask import Flask, Blueprint, request, jsonify, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, requests, json
from userForm import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required

site = Blueprint("site", __name__)


class Site:
    """
    Site class
    """
    Make = ''
    BodyType = ''
    Color = ''
    Seats = ''
    Location = ''
    CostPerHour = ''
    data = {}
    headers = {}

    @staticmethod
    def getCarInfo(request):
        global Make
        global BodyType
        global Color
        global Seats
        global Location
        global CostPerHour
        global data
        global headers
        Make = request.form["Make"]
        BodyType = request.form["BodyType"]
        Color = request.form["Color"]
        Seats = request.form["Seats"]
        Location = request.form["Location"]
        CostPerHour = request.form["CostPerHour"]
        data = {
            "Make": Make,
            "BodyType": BodyType,
            "Color": Color,
            "Seats": Seats,
            "Location": Location,
            "CostPerHour": CostPerHour
        }
        # Has to be in json
        headers = {
            "Content-type": "application/json"
        }

    @staticmethod
    def isLogin():
        # Check login Status
        if session.get('username') == 'huynino96' and session.get('password') == '123456':
            userInfo = 'huynino96'
        else:
            userInfo = None
        return userInfo

    @staticmethod
    @site.route("/update", methods=['POST'])
    def update():
        userInfo = Site.isLogin()
        if userInfo is None:
            return render_template("home.html", userInfo=userInfo)

        methodPut = request.form['put']
        Site.getCarInfo(request)
        # check if update method
        if methodPut == "PUT":
            if len(Make) > 100 or len(BodyType) > 50 or len(Color) > 100:
                flash(
                    'The Brand or BodyType or Color is may be too long! Please change your input or Contact us for further supports.',
                    'warning')
                return redirect(url_for('site.index'))

            carId = request.form['CarId']
            requests.put("http://127.0.0.1:5000/car/" + carId, data=json.dumps(data), headers=headers)
            flash('Car has been updated successfully', 'success')
            return redirect(url_for('site.index'))

    @staticmethod
    @site.route("/delete", methods=['POST'])
    def delete():
        userInfo = Site.isLogin()
        if userInfo is None:
            return render_template("home.html", userInfo=userInfo)

        methodDelete = request.form['delete']
        # Check delete and send notify
        if methodDelete == 'DELETE':
            carId = request.form['CarId']
            requests.delete("http://127.0.0.1:5000/car/" + carId)

            flash('Car has been deleted successfully', 'success')
            return redirect(url_for('site.index'))

    @staticmethod
    @site.route("/index", methods=['POST', 'GET'])
    def index():
        userInfo = Site.isLogin()
        if userInfo is None:
            return render_template("home.html", userInfo=userInfo)
        # Check Login status
        if request.method == 'GET':
            response = requests.get("http://127.0.0.1:5000/car")
            data1 = json.loads(response.text)
            return render_template("home.html", car=data1, userInfo=userInfo)

    @staticmethod
    @site.route("/add", methods=['POST', 'GET'])
    def add():
        userInfo = Site.isLogin()
        if userInfo is None:
            flash("Login first to add new Car", 'warning')
            return redirect(url_for('site.login'))
        # Check for Update method and send notify
        if request.method == 'POST':
            Site.getCarInfo(request)

            if len(Make) > 100 or len(BodyType) > 50 or len(Color) > 50:
                flash(
                    'The Brand or BodyType or Color is may be too long! Please change your input or Contact us for further supports.',
                    'danger')
                return render_template("add.html")

            response = requests.post("http://127.0.0.1:5000/car", data=json.dumps(data), headers=headers)
            res = json.loads(response.text)
            if len(res) == 1:
                flash('Car has been existed!', 'warning')
                return render_template("add.html")
            else:
                flash('Successfully Added new Car', 'success')
                return render_template("add.html")

        return render_template("add.html", userInfo=userInfo)

    @staticmethod
    @site.route("/report", methods=['POST', 'GET'])
    def report():
        userInfo = Site.isLogin()
        if userInfo is None:
            flash("Login first to view the report", 'warning')
            return redirect(url_for('site.login'))
        # get the report
        response = requests.get("http://127.0.0.1:5000/car")
        data = json.loads(response.text)
        return render_template("report.html", people=data, userInfo=userInfo)

    @staticmethod
    @site.route("/login/", methods=['GET', 'POST'])
    def login():
        # Creating a web page form
        form = LoginForm()
        # Collecting submitted info
        if form.validate_on_submit():
            if form.username.data == 'huynino96' and form.password.data == '123456':
                session['username'] = form.username.data
                session['password'] = form.password.data
                flash('You have been logged in!', 'success')
                response = requests.get("http://127.0.0.1:5000/car")
                data1 = json.loads(response.text)
                userInfo = form.username.data
                return render_template("home.html", car=data1, userInfo=userInfo)
            else:
                flash('Wrong username or password', 'danger')

        userInfo = Site.isLogin()
        return render_template('login.html', title='Login', form=form, userInfo=userInfo)

    @staticmethod
    @site.route("/about")
    def about():
        group = [
            {
                'name': 'Huy',
                'id': 's3756868',
                'content': 'IT student',
            },
        ]
        userInfo = Site.isLogin()
        return render_template("about.html", group=group, userInfo=userInfo)

    @staticmethod
    @site.route("/logout")
    def logout():
        # Logout
        session.pop('username', None)
        session.pop('password', None)
        return redirect(url_for('site.login'))

    @staticmethod
    @site.route("/register", methods=['GET', 'POST'])
    def register():
        userInfo = Site.isLogin()
        form = RegistrationForm()
        # Check registration and send notify
        if form.validate_on_submit():
            flash('Account has been created successfully!', 'success')
            return render_template('login.html', title='Login', form=form, userInfo=userInfo)
        return render_template('register.html', title='Register', form=form, userInfo=userInfo)
