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

get_daily_analytics()
----------------------------------------------------
* Method: get_daily_analytics()
function: return the car borrowed and returned in a day.

def get_monthly_analytics():
----------------------------------------------------
* Method: get_monthly_analytics()
function: return the car borrowed and returned in a month.


