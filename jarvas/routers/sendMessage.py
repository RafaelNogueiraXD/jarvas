from http import HTTPStatus
from typing import Annotated
import json, requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from jarvas.database import get_session

from jarvas.schemas import AppMessage, Message, DiscordMessage
from jarvas.models.database import App, User
from jarvas.security import get_current_user

router  = APIRouter(prefix='/sendMessage', tags=['sendMessage'])
Session = Annotated[Session, Depends(get_session)]

CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/whatsapp/',status_code=HTTPStatus.OK, response_model=Message)
def send_whatsapp_message(
    app_message: AppMessage,
    session: Session,
    user: CurrentUser
):
    app = session.scalar(select(App).where(App.name == app_message.name))
    if not app:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="App not found")
    
    url = "http://localhost:8083/message/sendText/labLea"

    payload = json.dumps({
    "number": app_message.phone,
    # "number": "5555996852212",
    "options": {
        "delay": 100,
        "presence": "composing"
    },
    "textMessage": {
        "text": app.status
    }
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbnN0YW5jZU5hbWUiOiJjb2RlZHJvcCIsImFwaU5hbWUiOiJ3aGF0c2FwcC1hcGkiLCJ0b2tlbklkIjoiMmU2NjkyYWQtMGEzZi00NzU2LTgyY2YtYTQxNmQ1NGVjMzhiIiwiaWF0IjoxNjg4NDc5MzM3LCJleHAiOjE2ODg0ODI5MzcsInN1YiI6ImctdCJ9.3bwxn92a3-xWKDnC9PYPQ4BvK20fRls4lFVofCZPfRk'
   }

    response = requests.request("POST", url, headers=headers, data=payload)
    return {'message' : f"the status is {app.status}"}

@router.post('/discord/', status_code=HTTPStatus.OK, response_model=Message)
def send_discord_message(session: Session, app_message: DiscordMessage):
    url = "http://127.0.0.1:8001/"
    app = session.scalar(select(App).where(App.name == app_message.name))
    if not app:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="App not found")
    response = requests.post(url, json={
            "name": app_message.name,
            "message": f"The {app_message.name} is {app.status}",
            "id_channel": app_message.id_channel
        })  # Corrigido o json
    return {'message': f"the status is {app.status}"}
