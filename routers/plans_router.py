import pandas as pd
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from io import BytesIO
from sqlalchemy import tuple_
from schemas.schema_plan import PlanInsertResponse

from db.local_db import get_session
from models.plan import Plan
from models.dictionary import Dictionary

router = APIRouter()


def return_id_in_colum(col: str, dic: List[Dictionary]) -> int:
    res = list(filter(lambda y: y if col.lower() == y.name else None, dic))
    if res:
        return res[0].id


@router.post("/plans_insert", response_model=PlanInsertResponse)
async def plans_insert(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='We can get only Excel files in format xlsx or .xls'
        )

    content = await file.read()
    session = next(get_session())

    df = pd.read_excel(BytesIO(content))
    dictionary_ = session.query(Dictionary).all()
    df['category_id'] = df['Назва категорії плану'].apply(lambda x: return_id_in_colum(x, dictionary_), )
    df['Місяць плану'] = pd.to_datetime(df['Місяць плану'])

    df_lst_data = list(zip(df['Місяць плану'], df['category_id']))

    db_plan = (session.query(Plan).filter(tuple_(Plan.period, Plan.category_id).in_(df_lst_data))
               .with_entities(Plan.period, Plan.category_id).all())
    if db_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'We had plan(s) with such category and date'
        )

    non_first_days = df['Місяць плану'].dt.day != 1
    if non_first_days.any():
        not_first_days = df.loc[df['Місяць плану'].dt.day != 1, 'Місяць плану'].dt.strftime('%Y-%m-%d').tolist()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'The date {not_first_days} incorrect.It needs to be first day of month.'
        )

    plans = []

    if df['Сума'].isna().any():
        na_rows = df.index[df['Сума'].isna()].tolist()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sum value found in rows {na_rows}. Sum cannot be None."
        )

    for index, row in df.iterrows():
        inst = Plan(
            period=row['Місяць плану'],
            sum=float(row['Сума']),
            category_id=row['category_id']
        )
        plans.append(inst)

    if plans:
        session.add_all(plans)
        session.commit()

    return {'msq': 'Plans successfully inserted into database!'}
