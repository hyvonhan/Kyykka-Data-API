import json
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_restful import Api, Resource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    team1 = db.Column(db.String(64), nullable = True) #muista muuttaa falseksi
    team2 = db.Column(db.String(64), nullable = True) #muista muuttaa falseksi
    date = db.Column(db.String(64), nullable = True)  #muista muuttaa falseksi
    team1_points = db.Column(db.Integer, nullable = True) #muista muuttaa falseksi
    team2_points = db.Column(db.Integer, nullable = True) #muista muuttaa falseksi

    matches_throws = db.relationship("Throw", back_populates="current_match")

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["team1", "team2", "id", "team1_points", "team2_points"]
        }
        props = schema["properties"] = {}
        props ["team1"] = {
            "description": "Name of team1",
            "type": "string"
        }
        props ["team2"] = {
            "description": "Name of team2",
            "type": "string"
        }
        props ["id"] = {
            "description": "ID of match",
            "type": "number"
        }
        props ["team1_points"] = {
            "description": "Points of team1",
            "type": "number"
        }
        props ["team2_points"] = {
            "description": "Points of team2",
            "type": "number"
        }
        return schema

class Throw(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable = False)
    points = db.Column(db.Integer, nullable = False)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable = False)

    current_match = db.relationship("Match", back_populates="matches_throws")
    individual_throw = db.relationship("Player", back_populates="player_throws")

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["id", "player_id", "points", "match_id"]
        }
        props = schema["properties"] = {}
        props ["id"] = {
            "description": "ID of the throw",
            "type": "number"
        }
        props = schema["properties"] = {}
        props ["player_id"] = {
            "description": "ID of the player",
            "type": "number"
        }
        props ["points"] = {
            "description": "Points of the throw",
            "type": "number"
        }
        props ["match_id"] = {
            "description": "ID of the game",
            "type": "number"
        }
        return schema

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique=True)
    team = db.Column(db.String(64), nullable = False)

    player_throws = db.relationship("Throw", back_populates="individual_throw")

    @staticmethod
    def get_schema():
        schema = {
            "type": "object",
            "required": ["name", "team"]
        }
        props = schema["properties"] = {}
        props ["name"] = {
            "description": "Name of the player",
            "type": "string"
        }
        props ["team"] = {
            "description": "Team of the player",
            "type": "string"
        }
        return schema
