from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi_sqlalchemy import db
import jwt

from datetime import datetime
from typing import Any, Union

from pydantic import ValidationError

from schema import SystemUser, TokenPayload
import model.models as models
from utils import ALGORITHM, JWT_SECRET_KEY


reusable_auth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def get_current_user(token: str = Depends(reusable_auth)):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expires",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.session.query(models.User).filter(models.User.id == token_data.sub).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return SystemUser(**user)
