import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from jarvas.main import app
from jarvas.database import get_session
from jarvas.models.database import User, table_registry,App
from jarvas.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user

@pytest.fixture
def app_external(session):
    app_external = AppFactory()

    session.add(app_external)
    session.commit()
    session.refresh(app_external)


    return app_external



@pytest.fixture
def other_user(session):
    password = 'testtest'
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

class AppFactory(factory.Factory):
    class Meta:
        model = App

    name = factory.Sequence(lambda n: f'test{n}')
    description = factory.LazyAttribute(lambda obj: f'this is a description of{obj.name}')
    status = factory.LazyAttribute(lambda obj: f'in progress')