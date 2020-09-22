Web App
=============


class Admin(db.Model)
----------------------------------------------------
    * function set_password(self, password):
        params: password
        function: set Admin password

    * function check_password(self, password):
        params: password
        function: hash params password and check if it matches hashed password in database

getDailyAnalytics()
----------------------------------------------------
* Method: getDailyAnalytics()
function: return the car borrowed and returned in a day.

def getMonthlyAnalytics():
----------------------------------------------------
* Method: getMonthlyAnalytics():
function: return the car borrowed and returned in a month.

Pages
----------------------------------------------------
* Admin
- Admin can browse histories of borrow, can add, delete and modify users and cars info
- Admin can view the report issue

* User
Normal users and managers:
- Normal users have page to book car and return car. Normal user also send reports issues to Admin
- Managers can view the statistic of book and return car

Authentication Web app
----------------------------------------------------
helper.js:
- Helper is created to define role for each users. 

register.js:
- Create register to create account for each users. Define if user is user, admin or manager to swicth the path to the correct page

login.js:
- Create login to autheticate user. Login page is connected with helpers. Helpers will recoded hashed password.

Header
----------------------------------------------------
Header is a NavBar to navigate users to the right path when clicked on.

