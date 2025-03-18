from fastapi import APIRouter, HTTPException
from sqlalchemy import func, case
from datetime import datetime

from schemas.schema_credits import UserCreditsResponse
from models.user import User
from models.credits import Credit
from models.dictionary import Dictionary
from models.payment import Payment
from db.local_db import get_session


router = APIRouter()


@router.get("/user_credits/{user_id}",response_model=UserCreditsResponse)
def get_user_credits(user_id: int):
    session = next(get_session())
    credits_ = session.query(Credit).filter_by(user_id=user_id).all()
    result = []
    if credits_ is None:
        raise HTTPException(status_code=404, detail="User has no credit")

    today = datetime.now().date()

    for credit in credits_:
        is_closed = credit.actual_return_date is not None

        body_payments, percent_payments = session.query(
            func.sum(case((Payment.type_id == 1, Payment.sum), else_=0)).label('body_payments'),
            func.sum(case((Payment.type_id == 2, Payment.sum), else_=0)).label('percent_payments')
        ).filter(
            Payment.credit_id == credit.id
        ).first() or (0.0, 0.0)

        credit_data = {"issued_date": credit.issuance_date,
                       "is_closed": is_closed,
                       'body': credit.body,
                       }
        if is_closed:
            credit_data.update({
                'actual_return_date': credit.actual_return_date,
                'total_payments': round(body_payments + percent_payments, 2)
            })
        else:
            overdue_days = 0

            if today > credit.return_date:
                overdue_days = (today - credit.return_date).days

            credit_data.update({
                'return_date': credit.return_date,
                'overdue_days': overdue_days,
                'body_payments': round(body_payments, 2),
                'percent_payments': round(percent_payments,2)
            })

        result.append(credit_data)

    if len(result) == 0:
        result = 'User has no credit'

    return {'credit': result}
