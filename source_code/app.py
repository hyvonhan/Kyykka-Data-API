import json
from datetime import datetime
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
    
class Match(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    team1 = db.Column(db.String(64), nullable = True)
    team2 = db.Column(db.String(64), nullable = True)
    date = db.Column(db.String(64), nullable = True)
    team1_points = db.Column(db.Integer, nullable = True)
    team2_points = db.Column(db.Integer, nullable = True)
    
    throws = db.relationship("Throw", back_populates="current_match")
    
class Throw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(64), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable = False)
    
    current_match = db.relationship("Match", back_populates="throws")

@app.route("/match/add/", methods=["POST"])
def add_match():
    # This branch happens when client submits the JSON document
    try:
        game_id = int(request.json["id"]) #lukee Jsonista tuotteen
        game = Match.query.filter_by(id=game_id).first() #luo listan
        if game:
            abort(409)
        if not game:
            team1 = str(request.json["team1"])
            team2 = str(request.json["team2"])
            date = str(request.json["date"])
            team1_points = int(request.json["team1_points"])
            team2_points = int(request.json["team2_points"])
            new_game = Match(
                id=game_id,
                team1=team1,
                team2=team2,
                date=date,
                team1_points=team1_points,
                team2_points=team2_points
            )
            db.session.add(new_game) #komento: tullaan lisaamaan tama tuote
            db.session.commit() #lisataan tuote tietokantaan
            return "succesful", 201
        else:
             abort(404)
    except (KeyError, ValueError, IntegrityError):
        abort(400)
    except TypeError: 
        abort(415)

@app.route("/throw/add/", methods=["POST"])
def add_throw():
    # This branch happens when client submits the JSON document
    try:
        throw_id = int(request.json["id"])
        throw = Throw.query.filter_by(id=throw_id).first()
        if throw:
            abort(409)
        if not throw:
            player = str(request.json["player"])
            points = int(request.json["points"])
            match_id = int(request.json["match_id"])
            new_throw = Throw(
                id=throw_id,
                player=player,
                points=points,
                match_id=match_id,
            )
            db.session.add(new_throw)
            db.session.commit()
            return "succesful", 201
        else:
             abort(404)
    except (KeyError, ValueError, IntegrityError):
        abort(400)
    except TypeError: 
        abort(415)            
    
    
@app.route("/match/")
def get_throws():
    response_data = []
    throws = Throw.query.all()
    for throw in throws:
        _throw = {}
        _throw["player"] = throw.player
        _throw["points"] = throw.points
        _throw["match_id"] = throw.match_id
        response_data.append(_throw)
    return json.dumps(response_data)