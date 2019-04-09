import json
from datetime import datetime
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

MASON = "application/vnd.mason+json"
LINK_RELATIONS_URL = "/kyykka/link-relations/"
ERROR_PROFILE = "/profiles/error/"
THROW_PROFILE = "/profiles/throw/"

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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
        schema = {}
        props = schema["properties"] = {}
        #props [] = {}
        return get_schema

class Throw(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable = False)
    points = db.Column(db.Integer, nullable = False)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id"), nullable = False)

    current_match = db.relationship("Match", back_populates="matches_throws")
    individual_throw = db.relationship("Player", back_populates="player_throws")

    @staticmethod
    def get_schema():
        schema = {}
        props = schema["properties"] = {}
        #props [] = {}
        return get_schema

class Player(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique=True)
    team = db.Column(db.String(64), nullable = False)

    player_throws = db.relationship("Throw", back_populates="individual_throw")

    @staticmethod
    def get_schema():
        schema = {}
        props = schema["properties"] = {}
        #props [] = {}
        return get_schema

@app.route("/match/add/", methods=["POST"])     #this function inserts a new match entry to the Match-table
def add_match():
    # This branch happens when client submits the JSON document
    try:
        game_id = int(request.json["id"])       #reads the id from Json
        game = Match.query.filter_by(id=game_id).first()        #takes all the data from Match-table and filters it by game_id and orders it descending from the first
        if game:        #if the match is already in the table abort the session
            abort(409)
        if not game:        #if there is no existing match, execute this
            team1 = str(request.json["team1"])      #read all the needed data from Json
            team2 = str(request.json["team2"])
            date = str(request.json["date"])
            team1_points = int(request.json["team1_points"])
            team2_points = int(request.json["team2_points"])
            new_game = Match(       #make entry for new match insert to the table
                id=game_id,
                team1=team1,
                team2=team2,
                date=date,
                team1_points=team1_points,
                team2_points=team2_points
            )
            db.session.add(new_game)        #this will be commited to the database
            db.session.commit()     #make the commit to the database
            return "succesful", 201
        else:
             abort(404)
    except (KeyError, ValueError, IntegrityError):
        abort(400)
    except TypeError:
        abort(415)

@app.route("/throw/add/", methods=["POST"])     #this function inserts a new throw entry to the Match-table
def add_throw():
    # This branch happens when client submits the JSON document
    try:
        throw_id = int(request.json["id"])      #reads data from Json
        throw = Throw.query.filter_by(id=throw_id).first()      #takes all the data from Throw-table and filters it by throw_id and orders it descending from the first
        if throw:       #if the throw is already in the table abort the session
            abort(409)
        if not throw:       #if there is no existing throw, execute this
            player = str(request.json["player"])        #read all the needed data from Json
            points = int(request.json["points"])
            match_id = int(request.json["match_id"])
            new_throw = Throw(      #make entry for new throw insert to the table
                id=throw_id,
                player=player,
                points=points,
                match_id=match_id,
            )
            db.session.add(new_throw)       #this will be commited to the database
            db.session.commit()     #make the commit to the database
            return "succesful", 201
        else:
             abort(404)
    except (KeyError, ValueError, IntegrityError):
        abort(400)
    except TypeError:
        abort(415)


@app.route("/match/")       #This function retrieves all the player data from the Throw table
def get_throws():       #It takes all the data from Throw table and prints them in to a key/value pairs for the user
    response_data = []
    throws = Throw.query.all()
    for throw in throws:
        _throw = {}
        _throw["player"] = throw.player
        _throw["points"] = throw.points
        _throw["match_id"] = throw.match_id
        response_data.append(_throw)
    return json.dumps(response_data)

class MatchCollection (Resource):
    pass

class MatchItem (Resource):
    pass

class ThrowCollection (Resource):
    pass

class ThrowItem (Resource):
    pass

class PlayerCollection (Resource):
    pass

class PlayerItem (Resource):
    pass

#do not touch
class MasonBuilder(dict):
    """
    A convenience class for managing dictionaries that represent Mason
    objects. It provides nice shorthands for inserting some of the more
    elements into the object but mostly is just a parent for the much more
    useful subclass defined next. This class is generic in the sense that it
    does not contain any application specific implementation details.
    """

    def add_error(self, title, details):
        """
        Adds an error element to the object. Should only be used for the root
        object, and only in error scenarios.

        Note: Mason allows more than one string in the @messages property (it's
        in fact an array). However we are being lazy and supporting just one
        message.

        : param str title: Short title for the error
        : param str details: Longer human-readable description
        """

        self["@error"] = {
            "@message": title,
            "@messages": [details],
        }

    def add_namespace(self, ns, uri):
        """
        Adds a namespace element to the object. A namespace defines where our
        link relations are coming from. The URI can be an address where
        developers can find information about our link relations.

        : param str ns: the namespace prefix
        : param str uri: the identifier URI of the namespace
        """

        if "@namespaces" not in self:
            self["@namespaces"] = {}

        self["@namespaces"][ns] = {
            "name": uri
        }

    def add_control(self, ctrl_name, href, **kwargs):
        """
        Adds a control property to an object. Also adds the @controls property
        if it doesn't exist on the object yet. Technically only certain
        properties are allowed for kwargs but again we're being lazy and don't
        perform any checking.

        The allowed properties can be found from here
        https://github.com/JornWildt/Mason/blob/master/Documentation/Mason-draft-2.md

        : param str ctrl_name: name of the control (including namespace if any)
        : param str href: target URI for the control
        """

        if "@controls" not in self:
            self["@controls"] = {}

        self["@controls"][ctrl_name] = kwargs
        self["@controls"][ctrl_name]["href"] = href

class GameBuilder(MasonBuilder):
    pass

def create_error_response(status_code, title, message=None):
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)

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
