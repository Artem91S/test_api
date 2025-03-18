from fastapi import APIRouter, HTTPException
from data_base.local_db import get_session
from typing import List, Union
from pydantic import BaseModel
from data_base.user import User
from data_base.credits import Credit
from data_base.dictionary import Dictionary
from data_base.payment import Payment
from sqlalchemy import func
from datetime import datetime, date

router = APIRouter()


class ClosedCredit(BaseModel):
    issued_date: date
    is_closed: bool
    body: float
    return_date: date
    percent: float
    total_payments: float


class OpenCredit(BaseModel):
    issued_date: date
    is_closed: bool
    body: float
    return_date: date
    percent: float
    overdue_days: int
    body_payments: float
    percent_payments: float


class UserCreditsResponse(BaseModel):
    credit: Union[List[Union[ClosedCredit, OpenCredit]], str]


@router.get("/user_credits/{user_id}")
def get_user_credits(user_id: int):
    session = next(get_session())
    credits_ = session.query(Credit).filter_by(user_id=user_id).all()
    result = []
    if credits_ is None:
        raise HTTPException(status_code=404, detail="User has no credit")

    today = datetime.now().date()

    for credit in credits_:
        is_closed = credit.return_date is not None

        body_payments = session.query(func.sum(Payment.sum)).filter(
            Payment.credit_id == credit.id,
            Payment.type_id == 1
        ).scalar() or 0.0
        percent_payments = session.query(func.sum(Payment.sum)).filter(
            Payment.credit_id == credit.id,
            Payment.type_id == 2
        ).scalar() or 0.0
        credit_data = {"issued_date": credit.issuance_date,
                       "is_closed": is_closed,
                       'body': credit.body,
                       'return_date': credit.return_date,
                       }
        if is_closed:
            credit_data.update({
                'total_payments': body_payments + percent_payments
            })
        else:
            overdue_days = 0

            if today > credits.return_date:
                overdue_days = (today - credit.return_date).days

            credit_data.update({
                'overdue_days': overdue_days,
                'body_payments': body_payments,
                'percent_payments': percent_payments
            })

        result.append(credit_data)
    if len(result) == 0:
        result = 'User has no credit'

    return {'credit': result}
