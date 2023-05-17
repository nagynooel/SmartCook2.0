# SmartCook 2.0

**⚠️️ Work In Progress ⚠️**

**DISCLAIMER: This project is created exclusively for CS50x WEB course and any sort of commercial use is unauthorized!**

SmartCook is an online cookbook, foodplanner and macronutrient tracker. It can help you make cooking and eating healthier easier than ever. It uses the USDA FoodData Central API for the macronutrients and also makes it easier to import recipes from anywhere.
This is an updated and rethought version of my older SmartCook project with some amazing new features.

## Features

🔴 - Planned
🟡 - In Progress

* User authentication system
* 🟡 Profile customization
* 🔴 Custom recipe creation  
* 🔴 Macronutrient tracking
* 🔴 Food planning on daily basis
* 🔴 Importing recipes from (almost) any website
* 🔴 Importing recipes from files
* 🔴 Exporting recipes to files

## Set Up

1. Install [python 3](https://www.python.org/downloads/).
2. Clone this repository. (I recommend you to do this in a virtual python environment. [Here](https://docs.python.org/3/library/venv.html) is a guide on creating a venv.)
3. Open your command line and navigate to the directory you cloned this repository to and install the required python modules. `pip install -r requirements.txt`
4. Create a file named ".env" in the root folder of this project and set up all the environmental variables below.
5. You will need a running MySQL server and a separate table for this application. If you don't have one I recommend you to use XAMPP. [Here](https://hevodata.com/learn/xampp-mysql/) is a guid to setting up XAMPP and creating a table.
6. When you followed all the instructions above, you should be able to start the application with the `python manage.py runserver` command.

## Environmental variables

In order to run the application you **have to** set up some environ variables. You can do this however you'd like.
I recommend using a ".env" file. You can just simply create it in the root folder of the project and it will automatically use it. Here are all of the variables you need with some examples.

I used the gmail SMTP server in the below example.

Strings inside "<>" are sensitive and unique data and you need to fill them in.

```
# Virtual environmental variables
# Django Variables
SECRET_KEY=<application secret key>

# Database Variables
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=smartcook2
DB_USERNAME=root
DB_PASSWORD=<database password>

# Email variables
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USER=<email username>
EMAIL_PASSWORD=<email password>
EMAIL_FROM=noreply@smartcook.com
```

## Credits/Sources

This project uses some images or vectors that have not been created by myself. Here are all of the images/vectors used with there creators and links.

* [No profile picture vector by OpenClipart](https://freesvg.org/users-profile-icon)