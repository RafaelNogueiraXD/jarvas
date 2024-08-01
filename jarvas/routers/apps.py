from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from jarvas.database import get_session
from jarvas.models.database import App, User
from jarvas.schemas import Message, AppSchema, AppList, AppPublic
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