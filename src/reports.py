from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = None
) -> pd.DataFrame:
    """
    Функция, которая возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    if date is None:
        new_date = datetime.now()
    else:
        new_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    date_3_months = new_date - timedelta(days=90)

    sorted_date = transactions[
        pd.to_datetime(transactions["Дата операции"], dayfirst=True) > date_3_months
    ]
    sorted_date = sorted_date[
        pd.to_datetime(sorted_date["Дата операции"], dayfirst=True) <= new_date
    ]
    sorted_date = sorted_date[sorted_date["Категория"] == category]

    return pd.DataFrame(sorted_date)
