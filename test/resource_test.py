import json
import os
import pytest
import tempfile
import time
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from app import app #the tested code needs to be in the same file
from models import Match, Throw, Player, db
import utils

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    db.create_all()
    _populate_db()

    yield app.test_client()

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
    
def _populate_db():
    """
    Pre-populate database with 2 matches, 2 players and 2 throws
    """
    match1 = Match(
        team1 = "Bears",
        team2 = "Wolves",
        date = "24.2.2019",
        team1_points = -100,
        team2_points = 20
    )

    match2 = Match (
        team1 = "Hawks",
        team2 = "Buffalos",
        date = "24.2.2019",
        team1_points = -60,
        team2_points = 0
    )
    
    throw1 = Throw(
        player_id = 1,
        points = 2,
        match_id = 1
    )
    
    throw2 = Throw(
        player_id = 2,
        points = 3,
        match_id = 1
    )
    
    player1 = Player(
        name = "John",
        team = "Bears"
    )
    
    player2 = Player(
        name = "Bill",
        team = "Wolves"
    )

    
    match1.matches_throws.append(throw1) #mita tassa tapahtuu?
    match1.matches_throws.append(throw2)
    player1.player_throws.append(throw1)
    player2.player_throws.append(throw2)
    
    db.session.add(match1)
    db.session.add(match2)
    
    db.session.add(throw1)
    db.session.add(throw2)
    
    db.session.add(player1)
    db.session.add(player2)
    db.session.commit()

def _get_match_json():
    return {
            "id":3,
            "team1":"Foxes",
            "team2":"Rabbits",
            "date":"10.5.2019",
            "team1_points":40,
            "team2_points":10
}

def _check_namespace(client, response):
    """
    Checks that the "kyykka" namespace is found from the response body, and
    that its "name" attribute is a URL that can be accessed.
    """

    ns_href = response["@namespaces"]["kyykka"]["name"]
    resp = client.get(ns_href)
    assert resp.status_code == 200
    
def _check_control_get_method(ctrl, client, obj):
    """
    Checks a GET type control from a JSON object be it root document or an item
    in a collection. Also checks that the URL of the control can be accessed.
    """
    
    href = obj["@controls"][ctrl]["href"]
    resp = client.get(href)
    assert resp.status_code == 200

def _check_control_post_method(ctrl, client, obj):
    """
    Checks a POST type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 201.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "post"
    assert encoding == "json"
    body = _get_match_json()
    validate(body, schema)
    resp = client.post(href, json=body)
    assert resp.status_code == 201    

def _check_control_delete_method(ctrl, client, obj):
    """
    Checks a DELETE type control from a JSON object be it root document or an
    item in a collection. Checks the contrl's method in addition to its "href".
    Also checks that using the control results in the correct status code of 204.
    """
    
    href = obj["@controls"][ctrl]["href"]
    method = obj["@controls"][ctrl]["method"].lower()
    assert method == "delete"
    resp = client.delete(href)
    assert resp.status_code == 204

def _check_control_put_method(ctrl, client, obj):
    """
    Checks a PUT type control from a JSON object be it root document or an item
    in a collection. In addition to checking the "href" attribute, also checks
    that method, encoding and schema can be found from the control. Also
    validates a valid sensor against the schema of the control to ensure that
    they match. Finally checks that using the control results in the correct
    status code of 204.
    """
    
    ctrl_obj = obj["@controls"][ctrl]
    href = ctrl_obj["href"]
    method = ctrl_obj["method"].lower()
    encoding = ctrl_obj["encoding"].lower()
    schema = ctrl_obj["schema"]
    assert method == "put"
    assert encoding == "json"
    body = _get_match_json()
    body["id"] = obj["id"]
    validate(body, schema)
    resp = client.put(href, json=body)
    assert resp.status_code == 204

class TestMatchCollection(object):

    RESOURCE_URL = "/api/matches/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        _check_control_post_method("kyykka:add-match", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            assert "id" in item
            assert "team1" in item
            assert "team2" in item
            assert "date" in item
            assert "team1_points" in item
            assert "team2_points" in item

    def test_post(self, client):
        """
        Tests the POST method. Checks all of the possible error codes, and 
        also checks that a valid request receives a 201 response with a 
        location header that leads into the newly created resource.
        """
        valid = _get_match_json()

        # test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        body = json.loads(client.get(self.RESOURCE_URL).data)
        id = body["items"][-1]["id"] 
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + str(id) + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["id"] == 3
        assert body["team1"] == "Foxes"
        assert body["team2"] == "Rabbits"
        assert body["date"] == "10.5.2019"
        assert body["team1_points"] == 40
        assert body["team2_points"] == 10

        # test with wrong content type(must be json)
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        # remove title field for 400
        valid.pop("id")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
class TestMatchItem(object):
    RESOURCE_URL = "/api/matches/1/"
    INVALID_URL = "/api/matches/x/"
    MODIFIED_URL = "/api/matches/3/"
    
    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["team1"] == "Bears"
        assert body["team2"] == "Wolves"
        assert body["date"] == "24.2.2019"
        assert body["team1_points"] == -100
        assert body["team2_points"] == 20
        _check_namespace(client, body)
        _check_control_get_method("profile", client, body)
        _check_control_get_method("collection", client, body)
        _check_control_put_method("edit", client, body)
        _check_control_delete_method("kyykka:delete", client, body)
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
       
    def test_put(self, client):
        """
        Tests the PUT method. Checks all of the possible error codes, and also
        checks that a valid request receives a 204 response. Also tests that
        when name is changed, the match can be found from a its new URI. 
        """
        
        valid = _get_match_json()
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 415
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with another matche's id
        valid["id"] = 2
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # test with valid (only change model)
        valid["id"] = 1
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("team1")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        valid = _get_match_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["team1"] == valid["team1"]
               
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks that a valid request reveives 204
        response and that trying to GET the match afterwards results in 404.
        Also checks that trying to delete a match that doesn't exist results
        in 404.
        """
        
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404

#class TestThrowCollection(object):

class TestPlayerCollection(object):

    RESOURCE_URL = "/api/players/"

    def test_get(self, client):
        """
        Tests the GET method. Checks that the response status code is 200, and
        then checks that all of the expected attributes and controls are
        present, and the controls work. Also checks that all of the items from
        the DB popluation are present, and their controls.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        _check_namespace(client, body)
        #_check_control_post_method("kyykka:add-match", client, body)
        assert len(body["items"]) == 2
        for item in body["items"]:
            assert "name" in item
            assert "team" in item
