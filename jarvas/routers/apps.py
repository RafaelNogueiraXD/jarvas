from http import HTTPStatus
from typing import Annotated
import json, requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from jarvas.database import get_session
from jarvas.models.database import App, User
from jarvas.schemas import Message, AppSchema, AppList, AppPublic, AppMessage
from jarvas.security import get_current_user


router  = APIRouter(prefix='/apps', tags=['apps'])
Session = Annotated[Session, Depends(get_session)]

CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', status_code=HTTPStatus.CREATED, response_model=AppPublic)
def create_app(app: AppSchema, session: Session, user: CurrentUser):
    db_app = session.scalar(
        select(App).where(
            (App.name == app.name)
        )
    )
    if db_app:
        if db_app.name == app.name:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='name already exists',
            )
    db_app = App(
        name=app.name,
        description= app.description,
        status = app.status
    )
    session.add(db_app)
    session.commit()
    session.refresh(db_app)
    return db_app

@router.get('/', response_model=AppList)
def read_apps(session: Session, skip: int = 0, limit: int = 100):
    apps = session.scalars(select(App).offset(skip).limit(limit)).all()
    return {'apps': apps}

@router.put('/{name_app}', response_model=AppPublic)
def update_app(name_app: str,new_app: AppSchema,session: Session, user: CurrentUser):
    # sistema de autenticação que vai ser implementado
    app = session.scalar(select(App).where(App.name == name_app))

    if not app:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="App not found")
    
    app.name = new_app.name
    app.password = new_app.description
    app.status = new_app.status
    session.commit()
    session.refresh(app)

    return app


@router.delete('/{name_app}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    name_app: str,  # altere 'name' para 'name_app'
    session: Session,
    user: CurrentUser
):
    app = session.scalar(select(App).where(App.name == name_app))
    if not app:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="App not found")

    session.delete(app)
    session.commit()

    return {'message': 'app deleted'}


@router.post('/send_message/',status_code=HTTPStatus.OK, response_model=Message)
def send_message(
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
    # print(response)
    return {'message': f"the status is {app.status}"}