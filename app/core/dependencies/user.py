from typing import Tuple, Optional 

from fastapi import Header, Query, HTTPException, Request

from app.schemas import user as userSchemas
from app.core.services import user_service
from app.core.uow.uow import SqlAlchemyUnitOfWork


class Pagination:
    """Pagination dependency as a class"""
    def __init__(self, max_limit = 100) -> None:
        self.max_limit = max_limit

    def __call__(self, skip: int=Query(0, ge=0), limit: int=Query(10, ge=0)) -> Tuple[int, int]:
        capped_limit = max(limit, self.max_limit)
        return (skip, capped_limit)

async def pagination(
    skip: int=Query(0, ge=0),
    limit: int=Query(10, ge=0)
) -> Tuple[int, int]:
    """Pagination dependency as a func"""
    capped_limit = max(limit, 100)
    return (skip, capped_limit)

async def get_user_or_404(user_id: int) -> userSchemas.User:
    db_user: Optional[userSchemas.User] = user_service.get_user(user_id=user_id, uow=SqlAlchemyUnitOfWork())
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

async def get_user_id_or_404(request: Request) -> int:
    user_id = request.headers.get('x-cognito-user-id')
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found")
    return int(user_id)