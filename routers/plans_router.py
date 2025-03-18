import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pydantic import BaseModel
from data_base.local_db import get_session
from io import BytesIO
from sqlalchemy.orm import joinedload
from datetime import datetime
from data_base.plan import Plan
from data_base.dictionary import Dictionary

router = APIRouter()


class PlanInsertResponse(BaseModel):
    message: str


def convert_data(str):
    date_object = datetime.strptime(str, "%Y-%m-%d").date()
    return date_object


@router.post("/plans_insert", response_model=PlanInsertResponse)
async def plans_insert(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='We can get only Excel files in format xlsx or .xls'
        )

    content = await file.read()
    df = pd.read_excel(BytesIO(content))
    session = next(get_session())
    db_plan = session.query(Plan).options(joinedload(Plan.category)).all()
    dictionary_ = session.query(Dictionary).all()

    plans = []
    for index, row in df.iterrows():
        if pd.isna(row['Сума']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'The sum {row["Сума"]} incorrect.It can not be None.'
            )

        day_of_plan = pd.to_datetime(row['Місяць плану']).date()
        if day_of_plan.day != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'The date {day_of_plan} incorrect.It needs to be first day of month.'
            )
        result = [None for i in db_plan if
                  row['Назва категорії плану'].lower() == i.category.name and day_of_plan == i.period]
        if None in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'We had same plans for {day_of_plan}(s) '
            )
        category_id = [i for i in dictionary_ if i.name == row['Назва категорії плану'].lower()]
        if category_id:
            inst = Plan(
                period=day_of_plan,
                sum=float(row['Сума']),
                category_id=category_id[0].id
            )
            plans.append(inst)

    if len(plans) > 0:
        session.add_all(plans)
        session.commit()

    return {'msq': 'Plans successfully inserted into database!'}
