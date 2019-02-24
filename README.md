# PWP SPRING 2019
# Kyykka-Data-API
# Group information
* Student 1. Hannu Hyvönen  hannu.hyvonen@student.oulu.fi
* Student 2. Oona Kivelä    oona.kivela@student.oulu.fi
* Student 3. Satu Hyle      satu.hyle@student.oulu.fi

# Getting Started

It is recommended to use virtual environment to use and test the code. You should use Python 3.3 or newer for following instructions. Use use pip to install your virtual environment. Instructions to pip can be found from https://pip.pypa.io/en/stable/installing/.

In order to create your virtual environment, first create a file in your computer where you want to create the virtual environment. Next, type in your command prompt,
```
python -m venv /path/to/the/virtualenv
```
where ```/path/to/the/virtualenv``` is the path to your file you just created. You will see the name of your virtualenv in parenthesis in front of your command prompt. Next, you need to download requirements.txt file, which can be found inside the source_code file. Place it in the file of your virtual environment. Type in your command prompt:
```
> "file name"\Scripts\activate.bat
```
replace ```"file name"``` with the file name you used to create the environment. This will activate the virtual environment. Next, type in the command prompt:
```
pip install -r requirements.txt
```
This will install all the required libraries in your virtual environment in order to use this code. Libraries inside the requirements.txt can be found below

## Requirements.txt details

External Python libraries used in this project are json, datetime, flask, flask_sqlalchemy, sqlalchemy.exc, sqlalchemy.engine and sqlalchemy. The json library needed to be imported in order to use json-files. The datetime library is going to be used to fetch a date of the game. The flask library is used to let it use request calls from json and abort a mission when an exception is noticed. Flask is used as a database framework. From flask_sqlalchemy a SQLAlchemy is imported in order to build ORM. To be noticed with IntegrityError it needed to be imported from sqlalchemy.exc. To enable a foreign key support Engine needs to be imported from sqlalchemy.engine and event from sqlalchemy. 

# Instructions on how to setup and populate the database.

# Instruction on how to run the tests of your database.

# 6.If you are using python a `requirements.txt` with the dependencies
