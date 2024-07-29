from http import HTTPStatus

# from jarvas.schemas import UserPublic

def test_create_app(client):
    
    response = client.post(
        '/apps/',
        json={
            'name': 'projeto 3',
            'description': 'this is a new project',
            'status': 'started',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    # assert response.json() == {
    #     'name': 'projeto 3',
    #     'description': 'this is a new project',
    #     'status': 'started',
    #     'id': 1,
    # }


def test_read_apps(client):
    response = client.get('/apps/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'apps': []}

def test_update_app(client):
    nomeApp = 'projeto 3'
    response = client.put(
        f'/apps/{nomeApp}',
        json={
        "name": "second app",
        "description": "kodsako",
        "status": "in progress"
        },
    )
    app = response.json()
    # assert response.status_code == HTTPStatus.OK
    # assert app['name'] == 'second app'