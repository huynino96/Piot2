Installation
=======================

Installation all packages
----------------------------------
* Using command bellow to install all packages to use the project. 
    pip3 install -r requirements.txt
    
All the verison of libararies have been provided and tested in the file to avoid bugs during the insatllation

Agent Pi
----------------------------------
* For using Agent Pi
1. Navigate the Terminal to the Piot2 directory
2. Run file "client-menu" to start using the system by using:
    python3 client-menu.py
3. There are option to use the Agent PI.
4. Use can register their account by providing normal username and password
5. Use can use face ID to detect their face

REST API Endpoint
----------------------------------
* For using the endpoint running, go to rest-api directory in Piot2 and use:
    python3 rest.py

Web app localhost
----------------------------------
* The web app is built with Next.js (Server side rendering of ReactJS) and can be run in localhost:
1. Navigate to "rest-api" directory.
2. Navigate to "web" directory
3. Use "yarn install" to install all the dependencies from "package.json"
4. Use "yarn dev" to start the web locally via "localhost:5000/<user-type>"

User Type
----------------------------------
There are 3 types of users: Admin, Manager and User
All of them will be defined in User Model (in model.py)
The admin and manager are created as "admin" and "manager" username so no one can create admin and manager anymore.

**Admin:** 

username: admin

pass: 123456


**Manager:**

username: manager

pass: 123456


**User (more users can register to the system):**

username: huy

pass: 123456

