import json
import utils
from datetime import datetime
from flask import Flask, request, abort
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

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@app.route("/api/")
def entry_point():
    body = MasonBuilder()
    body.add_namespace("kyykka", "/api/")
    body.add_control("kyykka:matches-all", "/api/matches/")
    return Response(json.dumps(body), mimetype=MASON)

class GameBuilder(MasonBuilder):

    def add_control_all_matches(self):
        self.add_control(
            "kyykka:matches-all",
            "/api/matches/",
            method="GET",
            encoding="json",
            title="Add control to all matches",
            schema=Match.get_schema()
            )

    def add_control_add_match(self):
        self.add_control(
            "kyykka:add-match",
            api.url_for(MatchCollection),
            method="POST",
            encoding="json",
            title="Add a new match",
            schema=Match.get_schema()
        )

    def add_control_add_throw(self):
        self.add_control(
            "kyykka:add-throw",
            api.url_for(ThrowCollection),
            method="POST",
            encoding="json",
            title="Add new throw",
            schema=Throw.get_schema()
        )

    def add_control_add_player(self):
        self.add_control(
            "kyykka:add-player",
            api.url_for(PlayerCollection),
            method="POST",
            encoding="json",
            title="Add new player",
            schema=Player.get_schema()
        )

    def add_control_delete_match(self, id):
        self.add_control(
            "kyykka:delete",
            api.url_for(MatchItem, id=id),
            method="DELETE",
            title="Delete this match"
        )

    def add_control_delete_throw(self, id):
        self.add_control(
            "kyykka:delete",
            api.url_for(ThrowItem, id=id),
            method="DELETE",
            title="Delete this throw"
        )

    def add_control_delete_player(self, name):
        self.add_control(
            "kyykka:delete",
            api.url_for(PlayerItem, name=name),
            method="DELETE",
            title="Delete player"
        )

    def add_control_edit_match(self, id):
        self.add_control(
            "edit",
            api.url_for(MatchItem, id=id),
            method="PUT",
            encoding="json",
            title="Edit this match",
            schema=Match.get_schema()
        )

    def add_control_edit_throw(self, id):
        self.add_control(
            "edit",
            api.url_for(ThrowItem, id=id),
            method="PUT",
            encoding="json",
            title="Edit this throw",
            schema=Throw.get_schema()
        )

    def add_control_edit_player(self, name):
        self.add_control(
            "edit",
            api.url_for(PlayerItem, name=name),
            method="PUT",
            encoding="json",
            title="Edit player",
            schema=Player.get_schema()
        )

class MatchCollection (Resource):

    def get(self):
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
                team1_points=db_matchid.team1_points,
                team2_points=db_matchid.team2_points
            )
            item.add_control("self", api.url_for(MatchItem, id=db_matchid.id))
            item.add_control("profile", THROW_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(415,"Unsupported media type", "Request must be JSON")

        try:
            validate(request.json, Match.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        new_match = Match(
            id=request.json["id"],
            team1=request.json["team1"],
            team2=request.json["team2"],
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

    def get(self, id):
        db_matchid = Match.query.filter_by(id=id),first()
        if db_matchid is None:
            return create_error_response(404, "Not found", "No match was found with id {}".format(id))

        body = GameBuilder(
            id=db_matchid.id,
            team1=db_matchid.team1,
            team2=db_matchid.team2,
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
        db_matchid = Match.query.filter_by(id=id).first()
        if db_matchid is None:
            return create_error_response(404, "Not found", "No match was found with id {}".format(id))

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, Match.get_schema())
        except ValidationError as e:
            return create_error_response(400, "Invalid JSON document", str(e))

        db_matchid.id = request.json["id"]
        db_matchid.team1 = request.json["team1"]
        db_matchid.team2 = request.json["team2"]
        db_matchid.team1_points = request.json["team1_points"]
        db_matchid.team2_points = request.json["team2_points"]

        try:
            db.session.commit()
        except IntegrityError:
            return create_error_response(409, "Already exists", "Match with id '{}' already exists".format(request.json["id"]))

        return Response(status=204)

    def delete(self, id):
        db_matchid = Match.query.filter_by(id=id).first()
        if db_matchid is None:
            return create_error_response(404, "Not found", "No match was found with id {}".format(id))

        db.session.delete(db_matchid)
        db.session.commit()

        return Response(status=204)

class ThrowCollection (Resource):

    def get(self):
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
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, Throw.get_schema())
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

    def get(self, id):
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
        db_throwid = Throw.query.filter_by(id=id).first()
        if db_throwid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, Throw.get_schema())
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
        db_throwid = Throw.query.filter_by(id=id).first()
        if db_throwid is None:
            return create_error_response(404, "Not found", "No throw was found with id {}".format(id))

        db.session.delete(db_throwid)
        db.session.commit()

        return Response(status=204)

class PlayerCollection (Resource):

    def get(self):
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
            item.add_control("self", api.url_for(PlayerItem, name=db_player.name))
            item.add_control("profile", PLAYER_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), status=200, mimetype=MASON)

    def post(self):
        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, Player.get_schema())
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

    def get(self, name):
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
        db_player = Player.query.filter_by(name=name).first()
        if db_player is None:
            return create_error_response(404, "Not found", "No player was found with name {}".format(name))

        if not request.json:
            return create_error_response(415, "Unsupported media type", "Requests must be JSON")

        try:
            validate(request.json, Player.get_schema())
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
        db_player = Player.query.filter_by(name=name).first()
        if db_player is None:
            return create_error_response(404, "Not found", "No player was found with name {}".format(name))

        db.session.delete(db_player)
        db.session.commit()

        return Response(status=204)

api.add_resource(MatchCollection, "/api/matches/")
api.add_resource(MatchItem, "/api/matches/<match_id>/")
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
