from datetime import datetime
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError, jwt
from crud import generate_12_digit_number
from routes.crud import get_current_account, get_withdraw_amount, transaction_detail
from schema import (
    AccountDetails,
    GetTransaction,
    TokenData,
    TokenSchema,
    UserAuth,
    UserResponse,
)
from fastapi_sqlalchemy import db
from fastapi.security import OAuth2PasswordBearer
import model.models as models
from utils import (
    create_access_token,
    create_refresh_token,
    get_hashed_password,
    verify_password,
    ALGORITHM,
    JWT_SECRET_KEY,
)

router = APIRouter()

aouth2_schema = OAuth2PasswordBearer(tokenUrl="token")


async def decode_jwt_token(token: Annotated[str, Depends(aouth2_schema)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        payload_user = payload.get("logged_user_id")
        user = db.session.query(models.User).filter(models.User.id == payload_user).first()
        if user:
            return dict(status=200, message=payload)
    except:
        raise credential_exception


@router.get("/decode_jwt")
async def decode_jwt(request: Request):
    data = await request.json()
    token = data.get("token")
    payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return payload


async def get_current_user(token: Annotated[str, Depends(aouth2_schema)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = (
        db.session.query(models.User)
        .filter(models.User.username == token_data.username)
        .first()
    )
    return user


############################################## user ################################################
@router.get('/testapi')
async def test():
    user = db.session.query(models.User).all()
    val=generate_12_digit_number()
    return user

@router.post("/signup",response_model=UserResponse)
async def create_user(data: UserAuth):
    user = db.session.query(models.User).filter(models.User.email == data.email).first()
    if user is not None:
        raise HTTPException(status_code=400, detail="username or email already exist")
    new_user = models.User(
        username=data.username,
        password=get_hashed_password(data.password),
        email=data.email,
        phone=data.phone,
    )
    db.session.add(new_user)
    db.session.commit()
    if new_user:
        random_num=generate_12_digit_number()
        user_id = new_user.id
        user_account = models.BankAccount(user_id=user_id,random_id=random_num)
        db.session.add(user_account)
        db.session.commit()
        return new_user


@router.post("/login", response_model=TokenSchema)
async def login_user(request: Request):
    data = await request.json()
    req_email = data.get("email", None)
    password = data.get("password", None)
    db_user = db.session.query(models.User).filter(models.User.email == req_email).first()
    print(db_user,"db_user::")
    if db_user is None:
        raise HTTPException(status_code=400, detail="Unable to login, Email not found")
    db_password = verify_password(password, db_user.password)
    if db_password:
        return {
            "access_token": create_access_token(db_user.email, id=db_user.id),
            "refresh_token": create_refresh_token(db_user.email, id=db_user.id),
        }
    else:
        raise HTTPException(
            status_code=400, detail="Unable to login, Incorrect password"
        )


@router.get("/test")
async def get_account(token: str = Depends(get_current_user)):
    user = await get_current_user(token)
    print(token.id, "yooo")


############################################## Account ################################################


@router.get("/account_details", response_model=AccountDetails)
async def accout_details(token: dict = Depends(decode_jwt_token)):
    if token['status'] == 200:
        logged_id = token["message"]["logged_user_id"]
    try:
        account = (
            db.session.query(models.BankAccount)
            .filter(models.BankAccount.account_id == logged_id)
            .first()
        )
        return account
    except Exception as err:
        print(err)
        raise HTTPException(status_code=400, detail="failed to fetch accout details")


@router.post("/deposit")
async def deposit_amount(request: Request, token: dict = Depends(decode_jwt_token)):
    data = await request.json()
    amount = data.get("amount")
    token_id = token["message"]["logged_user_id"]
    account,balance = await get_current_account(token_id, amount)
    return {"message":f"Amount {amount} added success, Balence:{balance}"}



@router.post("/withdraw")
async def withdraw_amount(request: Request, token: dict = Depends(decode_jwt_token)):
    if token['status'] == 200:
        data = await request.json()
        amount = data.get("amount")
        logged_id = token["message"]["logged_user_id"]
    try:
        account = await get_withdraw_amount(amount, logged_id)
        return {
            "message": f"{amount} withdrawed successfully",
            "New balance": f"{account.balance}",
        }
    except Exception as err:
        raise HTTPException(status_code=400, detail="Failed to withdraw amount")



@router.post("/transfer_amount")
async def transfer_amount(request: Request, token: dict = Depends(decode_jwt_token)):
    data = await request.json()
    to_account_id = data.get("to_account_id")
    transfer_amount = data.get("amount")
    logged_id = token["message"]["logged_user_id"]
    if transfer_amount <= 0:
        raise HTTPException(status_code=400, detail="Amount should be greater than 0 ")
    source_account = (
        db.session.query(models.BankAccount)
        .filter(models.BankAccount.user_id == logged_id)
        .first()
    )
    if not source_account:
        raise HTTPException(status_code=400, detail="Account not found")
    if source_account.balance < transfer_amount:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough amount,Blance : {source_account.balance}",
        )
    destination_account = (
        db.session.query(models.BankAccount)
        .filter(models.BankAccount.user_id == to_account_id)
        .first()
    )
    if not destination_account:
        raise HTTPException(status_code=400, detail="No Destination account found")
    try:
        source_account.balance -= transfer_amount
        destination_account.balance += transfer_amount

        transaction_debit = models.Transaction(
            owner_account_id=logged_id,
            from_account_id=source_account.account_id,
            to_account_id=destination_account.account_id,
            amount=transfer_amount,
            description = f"Amount {transfer_amount} has bee debited. from account id: {destination_account.account_id}",
            transaction_type="debit",
            timestamp = datetime.now()
        )
        transaction_credit = models.Transaction(
            owner_account_id=destination_account.account_id,
            from_account_id=destination_account.account_id,
            to_account_id=source_account.account_id,
            description = f"Amount {transfer_amount} has beed credited. from account id: {source_account.account_id}",
            amount=transfer_amount,
            transaction_type="credit",
            timestamp = datetime.now()
        )
        db.session.add(transaction_debit)
        db.session.add(transaction_credit)
        db.session.commit()

        return {"message": "Transaction successful"}
    except:
        db.session.rollback()
        raise HTTPException(status_code=400, detail="Transaction failed")


@router.post("/get_transaction_detail")
async def get_transaction_detail(data : GetTransaction, token: dict = Depends(decode_jwt_token)):
    request_date=data.start_date
    logged_id = token["message"]["logged_user_id"]
    try:
        transaction = transaction_detail(logged_id,request_date)
        if not transaction:
            return {"message": "No transaction details found"}
        return transaction
    except:
        raise HTTPException(status_code=400, detail="receiving transaction detail failed")
