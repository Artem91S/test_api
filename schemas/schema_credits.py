from pydantic import BaseModel
from datetime import date
from typing import List, Union


class ClosedCredit(BaseModel):
    issued_date: date
    is_closed: bool
    body: float
    actual_return_date: date
    total_payments: float


class OpenCredit(BaseModel):
    issued_date: date
    is_closed: bool
    body: float
    return_date: date
    overdue_days: int
    body_payments: float
    percent_payments: float


class UserCreditsResponse(BaseModel):
    credit: Union[List[Union[ClosedCredit, OpenCredit]], str]
