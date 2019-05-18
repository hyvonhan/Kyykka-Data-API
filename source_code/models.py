#import json
#from flask import Flask, request, abort
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event

from app import db
#from flask_restful import Api, Resource

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#db = SQLAlchemy(app)
#api = Api(app)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    team1 = db.Column(db.String(64), nullable = False) #muista muuttaa falseksi
    team2 = db.Column(db.String(64), nullable = True) #muista muuttaa falseksi
    date = db.Column(db.String(64), nullable = True)  #muista muuttaa falseksi
    team1_points = db.Column(db.Integer, nullable = True) #muista muuttaa falseksi
    team2_points = db.Column(db.Integer, nullable = True) #muista muuttaa falseksi
    db.UniqueConstraint('team1', 'team2', 'date', name="date_match_constraint")

    matches_throws = db.relationship("Throw", back_populates="current_match")

class Throw(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id", onupdate="CASCADE", ondelete="CASCADE"),nullable = True)
    points = db.Column(db.Integer, nullable = False)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id", onupdate="CASCADE", ondelete="CASCADE"),nullable = True)

    current_match = db.relationship("Match", back_populates="matches_throws")
    individual_throw = db.relationship("Player", back_populates="player_throws")

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique=True)
    team = db.Column(db.String(64), nullable = False)

    player_throws = db.relationship("Throw", back_populates="individual_throw")
