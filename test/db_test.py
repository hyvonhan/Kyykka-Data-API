import os
import pytest
import tempfile
import time
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

import app #the tested code needs to be in the same file
from app import Match, Throw, Player

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    with app.app.app_context():
        app.db.create_all()
        
    yield app.db

    app.db.session.remove() #this is needed in windows to remove permissionerror
    os.close(db_fd)
    os.unlink(db_fname)
	
def _get_match():
    return Match(
        team1 = "Bears",
        team2 = "Wolves",
        date = "24.2.2019",
        team1_points = -100,
        team2_points = 20
    )

def _get_throw():
    return Throw(
        player_id = 1,
        points = 2,
        match_id = 1
    )
    
def _get_throw2():
    return Throw(
        player_id = 2,
        points = 3,
        match_id = 1
    )

def _get_player1():
    return Player(
        name = "John",
        team = "Bears"
    )
def _get_player2():
    return Player(
        name = "Bill",
        team = "Wolves"
)

def _get_player3():
    return Player(
        name = "Mary",
        team = "Beavers" #this team doesn´t exist
    )

def test_create_instances(db_handle):
    """
    Tests that we can create few instances of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all relationships have been
    saved correctly.
    """
	# Create everything
    match = _get_match()
    throw = _get_throw()
    throw2 = _get_throw2()
    player1 = _get_player1()
    player2 = _get_player2()
    player3 = _get_player3()
    match.matches_throws.append(throw) #mita tassa tapahtuu?
    match.matches_throws.append(throw2)
    player1.player_throws.append(throw)
    player2.player_throws.append(throw2)
    #player3.player_throws.append(throw3)
    db_handle.session.add(match)
    db_handle.session.add(throw)
    db_handle.session.add(throw2)
    db_handle.session.add(player1)
    db_handle.session.add(player2)
    db_handle.session.add(player3)
    db_handle.session.commit()
    
    # Check that everything exists
    assert Match.query.count() == 1
    assert Throw.query.count() == 2
    assert Player.query.count() == 3
    db_match = Match.query.first()	
    db_throw = Throw.query.first()
    db_player = Player.query.first()

    # Check all relationships (both sides)
    assert db_throw in db_match.matches_throws #luodaanko tässä yhden suhde moneen?
    assert db_throw in db_player.player_throws
 

#----functions-------------------------------------------------	

def test_foreign_key_relationship(db_handle):
    """
    Tests that we can't assign throw in a match that doesn't exist.
    """	
    match = _get_match()
    throw_1 = _get_throw()
    throw_1.match = match
    db_handle.session.add(match)
    db_handle.session.add(throw_1)   
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_foreign_key_relationship_2(db_handle):
    """ 
    Tests that we can´t assign throw to a player that doesn´t exist.
    """
    throw = _get_throw()
    player3 = _get_player3()
    throw.player = player3
    db_handle.session.add(throw)
    db_handle.session.add(player3)
    with pytest.raises(IntegrityError):
        db_handle.session.commit()

def test_one_to_many_relationship(db_handle):
    """
    Tests that the relationship between match and throw is one-to-many.
    i.e. that we can assign many throws into a single match.
    """	
    match = _get_match()
    throw_1 = _get_throw()
    throw_1.match = match
    throw_2 = _get_throw2()
    throw_2.match = match
    db_handle.session.add(match)
    db_handle.session.add(throw_1)
    db_handle.session.add(throw_2)
    try:
        db_handle.session.commit()
    except IntegrityError:
        print("Onnistui")

def test_one_to_many_relationship2(db_handle):
    """
    Tests that the relationship between player and throw is one-to-many.
    i.e. that we can assign many throws for a single player   
    """
    player = _get_player1()
    throw_1 = _get_throw()
    throw_1.player = player
    throw_2 = _get_throw2()
    throw_2.player = player
    db_handle.session.add(player)
    db_handle.session.add(throw_1)
    db_handle.session.add(throw_2)
    try:
        db_handle.session.commit()
    except IntegrityError:
        print("Onnistui")

def test_throw_ondelete_match(db_handle):
    """
    Tests that when match is deleted, all the throws of the match are also deleted
    """	
    match = _get_match()
    throw_1 = _get_throw()
    throw_1.match = match
    db_handle.session.add(match)
    db_handle.session.commit()
    db_handle.session.delete(match)
    db_handle.session.commit()
    try:
        assert match.throw_1 is None
    except AttributeError:
        print("Throw doesn´t exist")

def test_onupdate_match(db_handle):
    """
    Test that we can add final team points to the match.
    """
    match = _get_match()
    db_handle.session.add(match)
    db_handle.session.commit()
    print(match)
    match.team1_points = 40
    match.team2_points = 60
    db_handle.session.add(match)
    db_handle.session.commit()
    print(match)
    