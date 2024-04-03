import pytest
import jwt
import os
from sqlalchemy.orm import sessionmaker

from connect_database import create_db_connection
from auth_permissions import authenticate

password_test = os.environ.get('TEST_PASSWORD')

@pytest.fixture(scope='session')
def db_session():
    engine = create_db_connection()
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_bad_email(db_session, capfd):
    """
    Test de l'authentification avec un mauvais email
    """
    token = authenticate('test@email.com', '1234')
    assert token is None
    captured = capfd.readouterr()
    assert 'Utilisateur inconnu' in captured.out


def test_good_email_bad_password(db_session, capfd):
    """
    Test de l'authentification avec un bon email mais un mauvais mot de passe
    """
    token = authenticate('emma.carena@example.com', '1234')
    assert token is None
    captured = capfd.readouterr()
    assert 'Mot de passe incorrect' in captured.out


def test_good_login(db_session, capfd):
    """
    Test de l'authentification avec un bon email mais un mauvais mot de passe
    """
    authenticate('emma.carena@example.com', password_test)
    captured = capfd.readouterr()
    assert 'Authentification réussie' in captured.out