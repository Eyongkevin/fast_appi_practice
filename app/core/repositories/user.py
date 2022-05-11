from typing import Union, Any, List
from fastapi import Query
from sqlalchemy.orm import Session
from app.schemas import user as userSchemas
from app.models import user


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, model: userSchemas.User) -> None:
        self.session.add(model)

    def refresh(self, data: userSchemas.User) -> None:
        self.session.refresh(data)

    def get_user(self, user_id: int) -> Union[userSchemas.User, None]:
        return self.session.query(user.User).filter(user.User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Union[Any, None]:
        return self.session.query(user.User).filter(user.User.email == email).first()

    def get_users(self, skip: int=0, limit: int=100):
        return self.session.query(user.User).offset(skip).limit(limit).all()

    def create_user(self, user: userSchemas.UserCreate) -> userSchemas.User:
        db_user = user.User(**user)
        return db_user

    def get_items(self, skip: int=0, limit: int=100) -> list:
        return self.session.query(user.Item).offset(skip).limit(limit).all()

    def create_user_item(self, item: userSchemas.ItemCreate, user_id: int) -> userSchemas.Item:
        db_item = user.Item(**item.dict(), owner_id=user_id)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def update_user(self, user_id: int, user_info: dict) -> None:
            self.session.query(user.User).filter(user.User.id==user_id).update(user_info)
            self.session.commit()

    def get_all_users_to_disable(self, run_now: Any) -> List[userSchemas.User]:

        users = list(self.session.query(user.User).filter(
            user.User.is_active == True,
            user.User.disable_date <= run_now
        ))
        return users
