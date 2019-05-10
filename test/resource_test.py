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
    '''
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
'''
    '''
    match1.matches_throws.append(throw1) #mita tassa tapahtuu?
    match1.matches_throws.append(throw2)
    player1.player_throws.append(throw1)
    player2.player_throws.append(throw2)
    '''
    db.session.add(match1)
    '''
    db.session.add(match2)
    db.session.add(throw1)
    db.session.add(throw2)
    db.session.add(player1)
    db.session.add(player2)
    '''
    db.session.commit()
'''
def _check_namespace(client, response):
    """
    Checks that the "kyykka" namespace is found from the response body, and
    that its "matches" attribute is a URL that can be accessed.
    """

    ns_href = response["@namespaces"]["kyykka"]["matches"]
    resp = client.get(ns_href)
    assert resp.status_code == 200
    '''

class TestMatchCollection(object):

    RESOURCE_URL = "/api/matches/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        #_check_namespace(client, body)
        #_check_control_post_method("kyykka:add-match", client, body)
        assert len(body["items"]) == 1
        for item in body["items"]:
            assert "team1" in item
            assert "team2" in item
            assert "date" in item
            assert "team1_points" in item
            assert "team2_points" in item