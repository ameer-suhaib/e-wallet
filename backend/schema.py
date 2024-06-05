from datetime import datetime
from typing import Union
from pydantic import BaseModel, Field
from uuid import UUID

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
    
class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserAuth(BaseModel):
    username : str
    password: str = Field(..., min_length=5, max_length=24, description="user password")
    email: str = Field(..., description="user email")
    phone : str
    

class UserResponse(BaseModel):
    id : int
    username : str
    email: str
    phone : str
    

class UserInDB(UserResponse):
    password : str

    

class GetAllUser(BaseModel):
    id : int
    username : str
    email: str
    phone : str



class UserOut(BaseModel):
    id : int
    email : str


class AccountDetails(BaseModel):
    account_id : int
    random_id : int
    balance : int
    created_at : datetime


class DepositResponse(BaseModel):
    owner_account_id : int
    user_id : int
    balance : int

class GetTransaction(BaseModel):
    start_date : str