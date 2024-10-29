from http import HTTPStatus
from jarvas.models.database import App



def test_send_message(client, session, token):
    new_app = App(name="second app", description='uma desc', status='in progress')
    session.add(new_app)
    session.commit()

    response = client.post(
        '/sendMessage/discord/',  # Corrigido o endpoint
        json={
            "name": new_app.name,
            "id_channel": 1300029095920537681
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': f"the status is {new_app.status}"}


