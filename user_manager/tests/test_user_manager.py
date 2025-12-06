from app.models import User
import pytest


def test_user_registration(db_session,manager):
    """testing registration"""
    username = "testuser"
    email = "tarunkmr566@gmail.com"
    lastname="Doe"
    firstname="John"    
    role : str = "user"
    password = "securepassword"
    manager.register(firstname,lastname,username, email, password, role)
    # User = manager.register(firstname,lastname,username, email, "securepassword", role)
    user = db_session.query(User).filter_by(username=username).first()
    assert user is not None
    assert user.email == email
    assert user.firstname == firstname
    assert user.lastname == lastname
    assert user.role == role

def test_password_hashing_test(db_session,manager):
    """testing password hashing and verification"""
    username = "john"
    password = "123"
    manager.register("John", "Doe", username, "john@example.com", password, "user")
    user = db_session.query(User).filter_by(username=username).first()
    assert user is not None
    # assert user is None
    assert user.password_hash != password  # Ensure password is hashed
    assert len(user.password_hash) > 40

def test_duplicate_username(db_session,manager):
    """testing duplicate username registration"""
    username = "jane1"
    email1 = "email@gmail.com"
    manager.register("Jane", "Doe", username, email1, "password1", "user")
    #check 1
    assert db_session.query(User).filter_by(username=username).count() == 1

    with pytest.raises(ValueError) as excinfo:
        manager.register("Janey", "Doe", username, "jane2@gmail,com", "password1", "user")

    assert "Username exists" in str(excinfo.value)

    assert db_session.query(User).filter_by(username=username).count() == 1
    print(str(excinfo.value))

def test_fixture_debug(db_session, manager):
    print("db_session:", db_session)
    print("manager.db:", manager.db)
    assert db_session is manager.db

    # create first user and show DB contents
    manager.register("Jane", "Doe", "jane1", "email@gmail.com", "pw", "user")
    users = [u.username for u in db_session.query(User).all()]
    print("users after register:", users)
    assert "jane1" in users

    