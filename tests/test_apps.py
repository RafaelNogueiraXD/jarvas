from http import HTTPStatus
from jarvas.models.database import App

# from jarvas.schemas import UserPublic

def test_create_app(client,token):
    
    response = client.post(
        '/apps/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'projeto 3',
            'description': 'this is a new project',
            'status': 'started',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'name': 'projeto 3',
        'description': 'this is a new project',
        'status': 'started',
        'id': 1,
    }

def test_read_apps(client):
    response = client.get('/apps/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'apps': []}

def test_update_app(client, session, token):
    new_app = App(name="second app",description='uma desc',status='in progress')
    session.add(new_app)
    session.commit()

    name_app = 'second app'
    response = client.put(
        f'/apps/{name_app}',
        headers={'Authorization': f'Bearer {token}'},
        json={
        "name": "teste app",
        "description": "kodsako",
        "status": "in progress"
        },
    )
    app_response= response.json()
    assert response.status_code == HTTPStatus.OK
    assert app_response['name'] == 'teste app'

def test_delete_app(client, session, token):
    new_app = App(name="second app",description='uma desc',status='in progress')
    session.add(new_app)
    session.commit()

    name = "second app"
    response = client.delete(
        f'/apps/{name}',
        headers={'Authorization': f'Bearer {token}'}
                             )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'app deleted'}

def test_send_message(client, session,token):
    new_app = App(name="second app",description='uma desc',status='in progress')
    session.add(new_app)
    session.commit()

    phone = "5555996852212"

    response = client.post(
        f'/apps/send_message/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            "name": new_app.name,
            "phone": phone
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': f"the status is {new_app.status}"}