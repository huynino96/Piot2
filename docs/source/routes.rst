Routes
==============

@app.route("/auth", methods=["POST"])
----------------------------------------------------
* function auth():
    function: post username and password to login

@app.route("/cars/add", methods=["POST"])
----------------------------------------------------

* function add_cars():
    function: add car to database using post method

@app.route("/cars/delete/<int:id>", methods=["DELETE"])
------------------------------------------------------------------

* function delete_car(id)
    params: id (car id)
    function: delete car using params car id

@app.route("/analytics/daily")
----------------------------------------------------

function daily_analytics()
    function: return data from get_daily_analytics() as json type

@app.route("/analytics/monthly")
----------------------------------------------------

function monthly_analytics()
    function: return data from get_monthly_analytics() as json type
