import pytest
from app.database import Base, engine, SessionLocal
from app.user_manager import UserManager

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def manager(db_session, monkeypatch):
    # override manager's db with test session
    m = UserManager()
    m.db = db_session
    return m
