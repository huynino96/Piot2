Main
===============

function handleLogin(data)
----------------------------------------------------
* function handleLogin(data)
    params: data
    function: if can not login, run displayMessage; if login success, run getCars() and  getAnalytics()

function displayMessage(data)
----------------------------------------------------
* function displayMessage(data)
    params: data
    function: display message with alert

function successfulLogin()
----------------------------------------------------
* function successfulLogin()
    function: hide login form and display the main section

function getCars()
----------------------------------------------------
* function getCars()
    function: request car data and display it using function displayCars().

function displayCars()
----------------------------------------------------
* function displayCars()
    function: display all cars in page.

function deleteCar(id)
----------------------------------------------------
* function deleteCar(id)
    params: id as carId
    function: delete the car data with params id

function getAnalytics()
----------------------------------------------------
* function getAnalytics()
    function: get and use data to draw daily and monthly graph

function initMain()
----------------------------------------------------
* function initMain()
    function: get cars data and display; draw graph about the amount of cars borrowed and returned.

