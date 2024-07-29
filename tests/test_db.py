from sqlalchemy import select

from jarvas.models.database import User, App


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'

def test_create_app(session):
    new_app = App(name='projeto 2', description='this project is to learn sorts algorithm', status='in progress')
    session.add(new_app)
    session.commit()

    user = session.scalar(select(App).where(App.name == 'projeto 2'))

    assert user.name == 'projeto 2'
