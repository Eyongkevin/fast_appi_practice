import datetime
import os
from struct import pack_into
from typing import Any, List, Dict, Optional, Tuple

import logging
from fastapi import APIRouter, Depends, HTTPException, Header, Query, Request, status, Response
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse


import app.schemas.user as userSchemas
from app.config.database import SessionLocal, engine
from app.core.uow.uow import SqlAlchemyUnitOfWork
from app.core.services import user_service
from app.config.settings import Settings
from app.core.dependencies.user import (
    get_user_or_404,
    pagination,
    Pagination,
    get_user_id_or_404

)
from app.core.dependencies import security

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings: Settings = Settings()
pagination2 = Pagination(int(settings.MAX_LIMIT))

router = APIRouter()


@router.get('/me', dependencies=[Depends(security.secret_header)])
async def get_me():
    img_dir = settings.IMAGE_DIR
    pic_path = os.path.join(img_dir, '45.JPG')
    return FileResponse(pic_path)

@router.get('/xml')
async def get_xml():
    content = """
            <?xml version="1.0" encoding="UTF-8"?>
            <Hello>World</Hello>
    """
    return Response(content=content, media_type="application/xml")

@router.post("", response_model=userSchemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: userSchemas.UserCreate):
    del user.password_confirmation
    db_user = user_service.get_user_by_email(email=user.email, uow=SqlAlchemyUnitOfWork())
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail= {
                "message": "Email already registered",
                "hints": [
                    "Change your email",
                    "Your email should be unique to our platform"
                ]
            })
    return user_service.create_user(user=user, uow=SqlAlchemyUnitOfWork())


@router.get("", response_model=List[userSchemas.User])
def read_users(response: Response, p: Tuple[int, int] = Depends(pagination2)):
    response.headers["Developer-name"] = "Eyong Kevin Enowanyo"
    skip, limit  = p
    # response.set_cookie("user-token", "slhghelsh445lsh#s", max_age=60)
    users: List[userSchemas.User] = user_service.get_users(skip=skip, limit=limit, uow=SqlAlchemyUnitOfWork())
    import pdb; pdb.set_trace()
    
    return users


@router.get("/{user_id}", response_model=userSchemas.User, status_code=status.HTTP_301_MOVED_PERMANENTLY)
def read_user(user: userSchemas.User = Depends(get_user_or_404)):
    
    return RedirectResponse(f"/api/v1/users/user_detail/{user.id}/{user.email}/{user.gender}/{user.is_active}/{user.disable_date}/{user.created_at}/{user.updated_at}", status_code=status.HTTP_301_MOVED_PERMANENTLY)

@router.patch("/disable",response_class=PlainTextResponse)
def disable_user_account(user_id: str = Depends(get_user_id_or_404)):  
    field = 'disable_date'
    Value = datetime.date.today() #+ datetime.timedelta(days=2)
    user_service.update_user(user_id, user_info={field: Value}, uow=SqlAlchemyUnitOfWork())

    return "User will be disabled in 2 days"

@router.patch("/{user_id}", response_model=userSchemas.User)
def update_user(user_update: userSchemas.UserUpdate, user: userSchemas.User = Depends(get_user_or_404)):
    user_update_dict = user_update.dict(exclude_unset=True)
    user_service.update_user(user_id=user.id, user_info=user_update_dict, uow=SqlAlchemyUnitOfWork())




@router.get("/user_detail/{user_id}/{user_email}/{user_gender}/{user_is_active}/{user_disable_date}/{user_created_at}/{user_updated_at}", response_class=HTMLResponse)
def user_detail(
            user_id: str, 
            user_email: str, 
            user_gender: str, 
            user_is_active: str, 
            user_disable_date:Optional[str],
            user_created_at: datetime.datetime,
            user_updated_at: datetime.datetime
            ):
    return f"""
        <html>
            <head>
                <title>Welcome to User portal</title>
            </head>
            <body>
                <h2>Details for User: {user_id}</h2>
                <p>Email: {user_email}</p>
                <p>Gender: {user_gender}</p>
                <p>Is Active: {user_is_active}</p>
                <p>Disable Date: {user_disable_date}</p>
                <p>Created Date: {user_created_at}</p>
                <p>Updated Date: {user_updated_at}</p>
            </body>
        </html>
    """

# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items



# @app.patch("/user/disable_all/")
# def run_disable_user_account(db: Session = Depends(get_db)):
#     run_now = datetime.date.today()
#     users_to_disable: List[schemas.User] = crud.get_all_users_to_disable(db, run_now)
#     for user in users_to_disable:
#         crud.update_user(db, user.id, user_info={'is_active': False})

