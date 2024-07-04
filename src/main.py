import pandas as pd

from src.reports import spending_by_category
from src.services import get_transactions_by_keyword
from src.views import main_page_info


def main() -> None:
    """
    Основная функция программы для взаимодействия с пользователем.
    """
    user_data_1 = input("Введите текущую дату и время в формате YYYY-MM-DD HH:MM:SS ")
    print(main_page_info(user_date=user_data_1))
    print("---------- ---------- ----------")

    user_data_2 = input("Введите ключевое слово для поиска ")
    print(get_transactions_by_keyword(user_keyword=user_data_2))
    print("---------- ---------- ----------")

    transactions_df = pd.read_excel("../data/operations.xls")
    user_data_category = input("Введите категорию ")
    date = input("Введите дату и время в формате YYYY-MM-DD HH:MM:SS ")
    print(spending_by_category(transactions=transactions_df, category=user_data_category, date=date))
    print("---------- ---------- ----------")


if __name__ == "__main__":
    main()
