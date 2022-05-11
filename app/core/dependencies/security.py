from http.client import HTTPException
from typing import Optional
from fastapi import Header, status


def secret_header(secret_header: Optional[str] = Header(None)):
    if not secret_header or secret_header != 'SECRET_VALUE':
        raise HTTPException(status.HTTP_403_FORBIDDEN)