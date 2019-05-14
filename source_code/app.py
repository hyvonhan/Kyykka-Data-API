"""Resources"""

import json
import utils
from datetime import datetime
from flask import Flask, request, abort, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_restful import Api, Resource
from jsonschema import validate, ValidationError
from utils import MasonBuilder, create_error_response
from utils import MASON, LINK_RELATIONS_URL, ERROR_PROFILE
from utils import THROW_PROFILE, MATCH_PROFILE, PLAYER_PROFILE

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

from models import Match, Throw, Player

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@app.route("/api/")
def entry_point():
    """
    Entry point
    """
    body = MasonBuilder()
    body.add_namespace("kyykka", "/api/")
    body.add_control("kyykka:matches-all", "/api/matches/")
    return Response(json.dumps(body), mimetype=MASON)


class GameBuilder(MasonBuilder):
    """
    GameBuilder created from MasonBuilder
    """
    @staticmethod
    def match_schema():
        schema = {
            "type": "object",
            "required": ["id","team1", "team2", "date", "team1_points", "team2_points"]
        }
        props = schema["properties"] = {}
        props ["id"] = {
            "description": "ID of match",
            "type": "number"
        }
        props ["team1"] = {
            "description": "Name of team1",
            "type": "string"
        }
        props ["team2"] = {
            "description": "Name of team2",
            "type": "string"
        }
        props ["date"] = {
            "description": "Date of the match",
            "type": "string"
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

    @staticmethod
    def throw_schema():
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

    @staticmethod
    def player_schema():
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

    def add_control_all_matches(self):
        """
        Control to all matches
        """
        self.add_control(
            "kyykka:matches-all",
            "/api/matches/",
            method="GET",
            encoding="json",
            title="Add control to all matches",
            schema=self.match_schema()
            )

    def add_control_add_match(self):
        """
        Control to add match
        """
        self.add_control(
            "kyykka:add-match",
            api.url_for(MatchCollection),
            method="POST",
            encoding="json",
            title="Add a new match",
            schema=self.match_schema()
        )

    def add_control_add_throw(self):
        """
        Control to add throw
        """
        self.add_control(
            "kyykka:add-throw",
            api.url_for(ThrowCollection),
            method="POST",
            encoding="json",
            title="Add new throw",
            schema=self.throw_schema()
        )

    def add_control_add_player(self):
        """
        Control to add player
        """
        self.add_control(
            "kyykka:add-player",
            api.url_for(PlayerCollection),
            method="POST",
            encoding="json",
            title="Add new player",
            schema=self.player_schema()
        )

    def add_control_delete_match(self, id):
        """
        Control to delete match
        """
        self.add_control(
            "kyykka:delete",
            api.url_for(MatchItem, id=id),
            method="DELETE",
            title="Delete this match"
        )

    def add_control_delete_throw(self, id):
        """
        Control to delete throw
        """
        self.add_control(
            "kyykka:delete",
            api.url_for(ThrowItem, id=id),
            method="DELETE",
            title="Delete this throw"
        )

    def add_control_delete_player(self, name):
        """
        Control to delete player
        """
        self.add_control(
            "kyykka:delete",
            api.url_for(PlayerItem, name=name),
            method="DELETE",
            title="Delete player"
        )

    def add_control_edit_match(self, id):
        """
        Control to edit match
        """
        self.add_control(
            "edit",
            api.url_for(MatchItem, id=id),
            method="PUT",
            encoding="json",
            title="Edit this match",
            schema=self.match_schema()
        )

    def add_control_edit_throw(self, id):
        """
        Control to edit throw
        """
        self.add_control(
            "edit",
            api.url_for(ThrowItem, id=id),
            method="PUT",
            encoding="json",
            title="Edit this throw",
            schema=self.throw_schema()
        )

    def add_control_edit_player(self, name):
        """
        Control to edit player
        """
        self.add_control(
            "edit",
            api.url_for(PlayerItem, name=name),
            method="PUT",
            encoding="json",
            title="Edit player",
            schema=self.player_schema()
        )

class MatchCollection (Resource):
    """
    Resource for all matches in collection. Function GET gets all matches in collection
    and POST adds a new match to collection
    """
    def get(self):
        """
        GET method to get all matches from the collection
        """
        body = GameBuilder()

        body.add_namespace("kyykka", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(MatchCollection))
        body.add_control_add_match()
        body["items"] = []
        for db_matchid in Match.query.all():
            item = GameBuilder(
                id=db_matchid.id,
                team1=db_matchid.team1, 
                team2=db_matchid.team2,
                date=db_matchid.date, #added date. seems to work now
                team1_points=db_matchid.team1_points,
                team2_points=db_matchid.team2_points
            )
            item.add_control("self", api.url_for(MatchItem, id=db_matchid.id)) #should work now
            item.add_control("profile", THROW_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        """
        POST method adds new match to collection
        """
        if not request.json:
            return create_error_response(415,"Unsupported media type", "Request must be JSON")

        try:
            validate(request.json, GameBuilder.match_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_match = Match(
            id=request.json["id"],
            team1=request.json["team1"],
            team2=request.json["team2"],
            date=request.json["date"],
            team1_points=request.json["team1_points"],
            team2_points=request.json["team2_points"]
        )

        try:
            db.session.add(new_match)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Match with id '{}' already exists".format(request.json["id"]))

        return Response(status=201, headers={"Location": api.url_for(MatchItem, id=request.json["id"])})

class MatchItem (Resource):
    """
    Resource for single MatchItem. Function GET gets a single match, PUT edits a single match
    and DELETE deletes a match.
    """

    def get(self, id):
        """
        GET method gets a single match
        """
        db_matchid = Match.query.filter_by(id=id).first()
        if db_matchid is None:
            return create_error_response(404, "Not found", "No match was found with id {}".format(id))

        body = GameBuilder(
            id=db_matchid.id,
            team1=db_matchid.team1,
            team2=db_matchid.team2,
            date=db_matchid.date,
            team1_points=db_matchid.team1_points,
            team2_points=db_matchid.team2_points
        )

        body.add_namespace("kyykka", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(MatchItem, id=id))
        body.add_control("profile", MATCH_PROFILE)
        body.add_control("collection", api.url_for(MatchCollection))
        body.add_control_delete_match(id)
        body.add_control_edit_match(id)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def put(self, id):
        """
        PUT method edits a single match
        """
        db_matchid = Match.query.filter_by(id=id).first()
        if db_matchid is None:
            return create_error_response(404, "Not found", "No match was found with id {}".format(id))

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, GameBuilder.match_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_matchid.id = request.json["id"]
        db_matchid.team1 = request.json["team1"]
        db_matchid.team2 = request.json["team2"]
        db_matchid.date = request.json["date"]
        db_matchid.team1_points = request.json["team1_points"]
        db_matchid.team2_points = request.json["team2_points"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Match with id '{}' already exists".format(request.json["id"]))

        return Response(status=204)

    def delete(self, id):
        """
        DELETE method deletes a single match
        """
        db_matchid = Match.query.filter_by(id=id).first()
        if db_matchid is None:
            return create_error_response(404, "Not found", "No match was found with id {}".format(id))

        db.session.delete(db_matchid)
        db.session.commit()

        return Response(status=204)

class ThrowCollection (Resource):
    """
    Resource for ThrowCollection. Function GET gets all the throws in collection
    and POST adds a new throw to collection.
    """
    def get(self):
        """
        GET method gets all the throws from ThrowCollection
        """
        body = GameBuilder()

        body.add_namespace("kyykka", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(ThrowCollection))
        body.add_control_add_throw()
        body["items"] = []
        for db_throwid in Throw.query.all():
            item = GameBuilder(
                id=db_throwid.id,
                points=db_throwid.points,
                player_id=db_throwid.player_id,
                match_id=db_throwid.match_id
            )
            item.add_control("self", api.url_for(ThrowItem, id=db_throwid.id))
            item.add_control("profile", THROW_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def post(self):
        """
        POST method adds a new throw to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, GameBuilder.throw_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_throw = Throw(
            id=request.json["id"],
            points=request.json["points"],
            player_id=request.json["player_id"],
            match_id=request.json["match_id"]
        )

        try:
            db.session.add(new_throw)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Throw with id '{}' already exists".format(request.json["id"]))

        return Response(status=201, headers={"Location": api.url_for(ThrowItem, id=request.json["id"])})

class ThrowItem (Resource):
    """
    Resource for ThrowItem. Function GET gets a single throw, PUT edits a throw
    and DELETE deletes a throw.
    """
    def get(self, id):
        """
        GET method gets a single throw
        """
        db_throwid = Throw.query.filter_by(id=id),first()
        if db_throwid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        body = GameBuilder(
            id=db_throwid.id,
            points=db_throwid.points,
            player_id=db_throwid.player_id,
            match_id=db_throwid.match_id
        )

        body.add_namespace("kyykka", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(ThrowItem, id=id))
        body.add_control("profile", THROW_PROFILE)
        body.add_control("collection", api.url_for(ThrowCollection))
        body.add_control_delete_throw(id)
        body.add_control_edit_throw(id)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def put(self, id):
        """
        PUT method edits a single throw 
        """
        db_throwid = Throw.query.filter_by(id=id).first()
        if db_throwid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, GameBuilder.throw_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_throwid.id = request.json["id"]
        db_throwid.points = request.json["points"]
        db_throwid.player_id = request.json["player_id"]
        db_throwid.match_id = request.json["match_id"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Throw with id '{}' already exists".format(request.json["id"]))

        return Response(status=204)

    def delete(self, id):
        """
        DELETE method deletes a single throw
        """
        db_throwid = Throw.query.filter_by(id=id).first()
        if db_throwid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        db.session.delete(db_throwid)
        db.session.commit()

        return Response(status=204)

class PlayerCollection (Resource):
    """
    Resource for PlayerCollection. Function GET gets all the players in collection
    and POST adds a new player to collection.
    """
    def get(self):
        """
        GET method gets all the players from collection
        """
        body = GameBuilder()

        body.add_namespace("kyykka", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(PlayerCollection))
        body.add_control_add_player()
        body["items"] = []
        for db_player in Player.query.all():
            item = GameBuilder(
                name=db_player.name,
                team=db_player.team
            )
            item.add_control("self", api.url_for(PlayerCollection))
            item.add_control("profile", PLAYER_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def post(self):
        """
        POST method adds a new player to collection
        """
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, GameBuilder.player_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_player = Player(
            name=request.json["name"],
            team=request.json["team"]
        )

        try:
            db.session.add(new_player)
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Player with name '{}' already exists".format(request.json["name"]))

        return Response(status=201, headers={"Location": api.url_for(PlayerItem, name=request.json["name"])})

class PlayerItem (Resource):
    """
    Resource for single PlayerItem. Function GET gets a player, PUT edits a player
    and DELETE deletes a player.
    """
    def get(self, name):
        """
        GET method gets a single player
        """
        db_player = Player.query.filter_by(name=name),first()
        if db_player is None:
            return create_error_response(404, "Not found", "No player was found with name {}".format(name))

        body = GameBuilder(
            name=db_player.name,
            team=db_player.team
        )

        body.add_namespace("kyykka", LINK_RELATIONS_URL)
        body.add_control("self", api.url_for(PlayerItem, name=name))
        body.add_control("profile", PLAYER_PROFILE)
        body.add_control("collection", api.url_for(PlayerCollection))
        body.add_control_delete_player(name)
        body.add_control_edit_player(name)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def put(self, name):
        """
        PUT method edits a player
        """
        db_player = Player.query.filter_by(name=name).first()
        if db_player is None:
            return create_error_response(404, "Not found", "No player was found with name {}".format(name))

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, GameBuilder.player_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_player.name = request.json["name"]
        db_player.team = request.json["team"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Player with name '{}' already exists".format(request.json["name"]))

        return Response(status=204)

    def delete(self, name):
        """
        DELETE method deletes a player
        """
        db_player = Player.query.filter_by(name=name).first()
        if db_player is None:
            return create_error_response(404, "Not found", "No player was found with name {}".format(name))

        db.session.delete(db_player)
        db.session.commit()

        return Response(status=204)

api.add_resource(MatchCollection, "/api/matches/")
api.add_resource(MatchItem, "/api/matches/<id>/") #this was match_id
api.add_resource(ThrowCollection, "/api/matches/<match_id>/throws/")
api.add_resource(ThrowItem, "/api/matches/<match_id>/throws/<throw_id>")
api.add_resource(PlayerCollection, "/api/players/")
api.add_resource(PlayerItem, "/players/<player_id>/")

@app.route(LINK_RELATIONS_URL)
def send_link_relations():
    return "link relations"

@app.route("/profiles/<profile>/")
def send_profile(profile):
    return "you requests {} profile".format(profile)
