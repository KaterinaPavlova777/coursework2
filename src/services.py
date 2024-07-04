import json
import logging
from typing import Any

import pandas as pd

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_transactions_by_keyword(user_keyword: str) -> Any:
    """
    Функция, которая возвращает транзакцию по ключевлму слову.
    """
    logger.info(f"get_transactions_by_keyword {user_keyword}")
    path = "../data/operations.xls"
    data = pd.read_excel(path)
    data["Описание"] = data["Описание"].astype(str)
    data["Категория"] = data["Категория"].astype(str)

    filtered_data = data[
        data["Описание"].str.contains(user_keyword, case=False)
        | data["Категория"].str.contains(user_keyword, case=False)
    ]

    transaction_list = filtered_data.to_dict(orient="records")
    json_response = json.dumps(transaction_list, indent=4, ensure_ascii=False)
    with open("transactions_by_keyword.json", "w", encoding="utf-8") as f:
        json.dump(transaction_list, f, indent=4, ensure_ascii=False)

    logger.info("Результаты поиска записаны в файл transactions_search_result.json")
    return json_response
