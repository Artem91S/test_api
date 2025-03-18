from db.local_db import get_session
from models.user import User
from models.credits import Credit
from models.dictionary import Dictionary
from models.plan import Plan
from models.payment import Payment
import csv
import pandas as pd


def reade_csv_file(file_name: str) -> list[dict]:
    with open(file_name, encoding='utf-8') as file:
        data = csv.DictReader(file, delimiter='\t')
        data = [i for i in data]
    return data

def create_credits_from_file():
    session = next(get_session())
    data = reade_csv_file('mock_data/credits.csv')
    data_list = []
    for row in data:
        inst = Credit(
            id=row['id'],
            user_id=row['user_id'],
            issuance_date=row['issuance_date'],
            return_date=row['return_date'],
            actual_return_date=row['actual_return_date'],
            body=row['body'],
            percent=row['percent']

        )
        data_list.append(inst)

    session.add_all(data_list)
    session.commit()

def create_dictionary_from_file():
    session = next(get_session())
    data = reade_csv_file('mock_data/dictionary.csv')
    data_list = []
    for row in data:
        inst = Dictionary(
            id=row['id'],
            name=row['name'],
        )
        data_list.append(inst)
    session.add_all(data_list)
    session.commit()

def create_payments_from_file():
    session = next(get_session())
    data = reade_csv_file('mock_data/payments.csv')
    data_list = []
    for row in data:
        inst = Payment(
            id=row['id'],
            sum=row['sum'],
            payment_date=row['payment_date'],
            credit_id=row['credit_id'],
            type_id=row['type_id']
        )
        data_list.append(inst)
    session.add_all(data_list)
    session.commit()


def create_plans_from_file():
    session = next(get_session())
    data = reade_csv_file('mock_data/plans.csv')
    data_list = []
    for row in data:
        inst = Plan(
            id=row['id'],
            period=row['period'],
            sum=row['sum'],
            category_id=row['category_id'],
        )
        data_list.append(inst)
    session.add_all(data_list)
    session.commit()

def create_user_from_file():
    session = next(get_session())
    data = reade_csv_file('mock_data/users.csv')
    data_list = []
    for row in data:
        inst = User(
            id=row['id'],
            login=row['login'],
            registration_date=row['registration_date']
        )
        data_list.append(inst)

    session.add_all(data_list)
    session.commit()

mock_data_for_xlsx = [
    {"Місяць плану": "2009-01-01", "Назва категорії плану": "Збір", "Сума": 200},
    {"Місяць плану": "2026-03-01", "Назва категорії плану": "Збір", "Сума": 500},
    {"Місяць плану": "2026-04-01", "Назва категорії плану": "Видача", "Сума": 2000},
    {"Місяць плану": "2027-04-01", "Назва категорії плану": "Збір", "Сума": 0},
    {"Місяць плану": "2028-05-01", "Назва категорії плану": "Видача", "Сума": 1500},
    {"Місяць плану": "2029-06-01", "Назва категорії плану": "Збір", "Сума": 700},
]


def create_file():
    df = pd.DataFrame(mock_data_for_xlsx)
    file_path = 'plans_test.xlsx'
    df.to_excel(file_path, index=False)


if __name__ == '__main__':
    create_file()
    create_user_from_file()
    create_plans_from_file()
    create_payments_from_file()
    create_dictionary_from_file()
    create_credits_from_file()

