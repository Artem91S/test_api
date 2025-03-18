from data_base.local_db import get_session
from data_base.user import User
from data_base.credits import Credit
from data_base.dictionary import Dictionary
from data_base.plan import Plan
from data_base.payment import Payment
import csv


def reade_csv_file(file_name: str) -> list[dict]:
    with open(file_name, encoding='utf-8') as file:
        data = csv.DictReader(file, delimiter='\t')
        data = [i for i in data]
    return data


def create_user_from_file():
    ...
    # session = next(get_session())
    # data = session.query(Credit).all()
    # print(data)
    # data = reade_csv_file('mock_data/payments.csv')
    # print(data)
    # data_list = []
    # for row in data:
    #     inst = Payment(
    #         id=row['id'],
    #         sum=row['sum'],
    #         payment_date=row['payment_date'],
    #         credit_id=row['credit_id'],
    #         type_id=row['type_id']
    #
    #     )
    #     data_list.append(inst)

    # for row in data:
    #     inst = User(
    #         id=row['id'],
    #         login=row['login'],
    #         registration_date=row['registration_date']
    #     )
    #     data_list.append(inst)
    #
    # session.add_all(data_list)
    # session.commit()

data = [
    {"Місяць плану": "2008-01-01", "Назва категорії плану": "Збір", "Сума": 200},
    {"Місяць плану": "2025-03-01", "Назва категорії плану": "Збір", "Сума": 500},
    {"Місяць плану": "2025-04-01", "Назва категорії плану": "Видача", "Сума": 2000},
    {"Місяць плану": "2025-04-01", "Назва категорії плану": "Збір", "Сума": 0},
    {"Місяць плану": "2025-05-01", "Назва категорії плану": "Видача", "Сума": 1500},
    {"Місяць плану": "2025-06-01", "Назва категорії плану": "Збір", "Сума": 700},
]
import pandas as pd

def create_file():
    df = pd.DataFrame(data)
    file_path = 'plans_test.xlsx'
    df.to_excel(file_path, index=False)


if __name__ == '__main__':
    create_file()
    # create_user_from_file()

