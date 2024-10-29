from http import HTTPStatus
from typing import Annotated
import json, requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from jarvas.database import get_session

from jarvas.schemas import AppMessage, Message, DiscordMessage
from jarvas.models.database import App

router  = APIRouter(prefix='/sendMessage', tags=['sendMessage'])
Session = Annotated[Session, Depends(get_session)]



# @router.post('/discord/',status_code=HTTPStatus.OK, response_model=Message)
# def send_discord_message(session: Session,app_message: AppMessage):
#     url = "http://127.0.0.1:8000/"
#     app = session.scalar(select(App).where(App.name == app_message.name))
#     if not app:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="App not found")
#     response = requests.request("POST",url=url, json={app.status})
#     return {'message' : f"the status is {app.status}"}

@router.post('/discord/', status_code=HTTPStatus.OK, response_model=Message)
def send_discord_message(session: Session, app_message: DiscordMessage):
    url = "http://127.0.0.1:8001/"
    app = session.scalar(select(App).where(App.name == app_message.name))
    if not app:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="App not found")
    response = requests.post(url, json={"status": app.status})  # Corrigido o json
    return {'message': f"the status is {app.status}"}
