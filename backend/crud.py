from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
import random

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token : Annotated[str,Depends(oauth2_schema)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}   
    )
    pass


def get_active_user(current_user : Annotated[str, Depends(get_current_user)]):
    pass


def generate_12_digit_number():
    range_start = 10**11
    range_end = (10**12) - 1
    return random.randint(range_start, range_end)
    
