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
    team1 = db.Column(db.String(64), nullable = False)
    team2 = db.Column(db.String(64), nullable = False)
    date = db.Column(db.DateTime, nullable = True)
    team1_points = db.Column(db.Integer, nullable = True)
    team2_points = db.Column(db.Integer, nullable = True)
    
    throws = db.relationship("Throw", back_populates="current_match")
    
class Throw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.String(64), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable = False)
    
    current_match = db.relationship("Match", back_populates="throws")
    
    
    
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