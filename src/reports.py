import json
import logging
from datetime import datetime, timedelta
from typing import Any, Optional

import pandas as pd

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Any:
    """
    Функция, которая возвращает траты по заданной категории за последние три месяца (от переданной даты).
    """
    logger.info(f"spending_by_category {transactions}, {category}, {date}")
    if date is None:
        new_date = datetime.now()
    else:
        new_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    date_3_months = new_date - timedelta(days=91)

    sorted_date = transactions[pd.to_datetime(transactions["Дата операции"], dayfirst=True) > date_3_months]
    sorted_date = sorted_date[pd.to_datetime(sorted_date["Дата операции"], dayfirst=True) <= new_date]
    sorted_date = sorted_date[sorted_date["Категория"] == category]

    transaction_list = sorted_date.to_dict(orient="records")
    result = sorted_date.to_json(orient="records")
    json_response = json.dumps(transaction_list, indent=4, ensure_ascii=False)
    with open("spending_by_category.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    logger.info(f"the resulting DataFrame {result}")

    return json_response
