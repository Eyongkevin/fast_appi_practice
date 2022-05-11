import logging
from typing import Any, List, Optional 
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
from app.core.uow.uow import SqlAlchemyUnitOfWork
from app.models.user import User
from app.schemas import user as userSchemas

logger = logging.getLogger(__name__)

def get_user(user_id: int, uow: SqlAlchemyUnitOfWork) -> Optional[userSchemas.User]:
    with uow:
        user = uow.users.get_user(user_id)
        return user

def get_user_by_email(email: str, uow: SqlAlchemyUnitOfWork) -> userSchemas.User:
    with uow:
        user = uow.users.get_user_by_email(email)
        return user

def create_user(user: userSchemas.UserCreate, uow: SqlAlchemyUnitOfWork) -> userSchemas.User:
    fake_hashed_password = user.password + 'notreallyhashed'
    is_active = True
    # address = jsonable_encoder(user.address)

    user_dict = user.dict(exclude={'password'})
    user_dict['hashed_password'] = fake_hashed_password

    user = User(
        **user_dict,
        is_active=is_active
    )
    with uow:
        try: 
            uow.users.add(user)
            uow.commit()
            uow.users.refresh(user)
            return user
        except SQLAlchemyError as error:
            logger.error(f"Failed to update user: {error}")
            raise error

def get_users(skip: int, limit: int, uow:SqlAlchemyUnitOfWork) -> List[userSchemas.User]:
    with uow:
        users = uow.users.get_users(skip, limit)
        return [user._serialize for user in users]

def update_user(user_id: int, user_info: dict, uow:SqlAlchemyUnitOfWork):
    with uow:
        uow.users.update_user(user_id, user_info)

def get_all_users_to_disable(run_now: Any, uow:SqlAlchemyUnitOfWork) -> List[userSchemas.User]:
    with uow:
        users = uow.users.get_all_users_to_disable(run_now)
        return users