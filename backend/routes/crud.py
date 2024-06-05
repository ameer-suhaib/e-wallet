from fastapi import HTTPException
from fastapi_sqlalchemy import db
from datetime import datetime

from sqlalchemy import func

from model import models


async def get_current_account(token_id, amount):
    account = (
        db.session.query(models.BankAccount)
        .filter(models.BankAccount.user_id == token_id)
        .first()
    )
    if not account:
        raise HTTPException(status_code=400, detail="No Account Found")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount should be positive number")
    account.balance += amount
    transaction = models.Transaction(
        owner_account_id=token_id,
        to_account_id=account.account_id,
        description = f'Amount {amount} has been deposite to your bank account',
        amount=amount,
        transaction_type="deposit",
        timestamp = datetime.now()
    )
    db.session.add(transaction)
    db.session.commit()
    return account, account.balance


async def get_withdraw_amount(amount, logged_id):
    account = (
        db.session.query(models.BankAccount)
        .filter(models.BankAccount.account_id == logged_id)
        .first()
    )
    if account.balance < amount:
        return {
            "message": f"Not enough balance",
            "current balance": f"{account.balance}",
        }
    else:
        try:
            account.balance -= amount
            transaction = models.Transaction(
                owner_account_id=logged_id,
                from_account_id=account.account_id,
                amount=amount,
                transaction_type="withdraw",
                description = f'Amout {amount} has been withdraw from your account',
                timestamp = datetime.now()
            )
            db.session.add(transaction)
            db.session.commit()
            return account
        except:
            raise HTTPException(status_code=400, detail="withdraw amount failed")


def transaction_detail(logged_id,request_date):
    print("hoooo")
    if request_date is not None:
        print("entereeddd")
        transaction = db.session.query(models.Transaction).filter(models.Transaction.owner_account_id == logged_id)
        print(transaction,":::transaction")
        date=datetime.strptime(request_date,"%Y-%m-%d").date()
        query = transaction.filter(func.date(models.Transaction.timestamp) >= date).all()
        return query
