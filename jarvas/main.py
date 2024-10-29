from http import HTTPStatus

from fastapi import FastAPI

from jarvas.routers import auth, users, apps , sendMessage
from jarvas.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(apps.router)
app.include_router(auth.router)
app.include_router(sendMessage.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
