# PWP SPRING 2019
# Kyykka-Data-API
## Group information
* Student 1. Hannu Hyvönen  hannu.hyvonen@student.oulu.fi
* Student 2. Oona Kivelä    oona.kivela@student.oulu.fi
* Student 3. Satu Hyle      satu.hyle@student.oulu.fi

## Getting Started

It is recommended to use virtual environment to use and test the code. You should use Python 3.3 or newer for following instructions. Use use pip to install your virtual environment. Instructions to pip can be found from https://pip.pypa.io/en/stable/installing/.

In order to create your virtual environment, first create a file in your computer where you want to create the virtual environment. Next, type in your command prompt,
```
python -m venv /path/to/the/virtualenv
```
where ```/path/to/the/virtualenv``` is the path to your file you just created. You will see the name of your virtualenv in parenthesis in front of your command prompt. Next, you need to download requirements.txt file, which can be found inside the source_code file. Place it in the file of your virtual environment. Type in your command prompt:
```
"file name"\Scripts\activate.bat
```
replace ```"file name"``` with the file name you used to create the virtualenv. This will activate the virtual environment. Next, type in the command prompt:
```
pip install -r requirements.txt
```
This will install all the required libraries in your virtual environment in order to use this code. Libraries inside the requirements.txt can be found below

### requirements.txt details

* flask
* flask-sqlalchemy
* pysqlite3
* ipython
* json
* pytest

### About the libraries

External Python libraries used in this project are json, datetime, flask, flask_sqlalchemy, sqlalchemy.exc, sqlalchemy.engine and sqlalchemy. The json library needed to be imported in order to use json-files. The datetime library is going to be used to fetch a date of the game. The flask library is used to let it use request calls from json and abort a mission when an exception is noticed. Flask is used as a database framework. From flask_sqlalchemy a SQLAlchemy is imported in order to build ORM. To be noticed with IntegrityError it needed to be imported from sqlalchemy.exc. To enable a foreign key support Engine needs to be imported from sqlalchemy.engine and event from sqlalchemy.

## Running the tests

In order to test the code, the database needs to be populated. This can be done with flask library. Make sure you are in your virtualenv in the command prompt. Type ```ipython``` in the command prompt. Detailed information of ipython can be found in https://ipython.org/. Basicly, it is an interactive shell in which the code will be tested. Flask will be our framework, detailed instructions can be found at http://flask.pocoo.org/docs/1.0/

### Instructions on how to populate the database.

Now that ipython is active, you can start population the database. At minimum you will need to insert two different matches and add throws in each of them. Every match overall includes 64 throws, but for testing purposes 3 throws per match is enough. Lets start by adding the two matches in our database.
```
[1]from app import db
[2]db.create_all()
[3]from app import Match, Throw
```
These two commands will create two tables: MATCH and THROW. The db.file will be created in the same file where the actual code is in your computer. This is an SQLite database with two empty tables. If you want to view the database, you can use DB browser for SQLite https://sqlitebrowser.org/. Next, we want to add two matches in the MATCH table. If at any point you get an exception, you should use ```db.session.rollback()``` to roll the transaction back.
```
[4]game1 = Match(team1="Bears", team2="Wolves") 
[5]game2 = Match(team1="Beevers", team2="Hogs")
[6]db.session.add(game1)
[7]db.session.add(game2)
[8]db.session.commit()
```
To check your games, type ```Match.query.first()```. Next, we should add some throws for each of the games.
```
[9]throw1 = Throw(player="Tom", points=2, match_id=1)
[10]throw2 = Throw(player="Lea", points=-4, match_id=1)
[11]throw3 = Throw(player="John", points=8, match_id=1)
[12]throw65 = Throw(player="Mary", points=-6, match_id=2)
[13]throw66 = Throw(player="Alex", points=2, match_id=2)
[14]throw67 = Throw(player="Jean", points=0, match_id=2)
[15]db.session.add(throw1)
[16]db.session.add(throw2)
[17]db.session.add(throw3)
[18]db.session.add(throw65)
[19]db.session.add(throw66)
[20]db.session.add(throw67)
[21]db.session.commit()
```
Throw number 65 is the first throw of the second game. As mentioned before, each game has 64 throws. To link a certain throw to a game, you need to write a correct match_id. Here number 1 means it belongs to the first game and number 2 means it belongs to the second game. You are not able to add throws to a games that do not exist. To check your throws, type ```Throw.query.first()```

# Instruction on how to run the tests of your database.

Pytest can be used to test the database. It is included in the requirements.txt file, so it was already installed.
