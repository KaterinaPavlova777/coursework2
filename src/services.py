import json
import logging

from src.utils import read_from_xlsx_file

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_transactions_by_keyword(user_keyword: str) -> list:
    """
    Функция, которая возвращает транзакцию по ключевлму слову.
    """
    logger.info(f"get_transactions_by_keyword {user_keyword}")
    result = []
    data = read_from_xlsx_file("../data/operations.xls")

    for transaction in data:
        try:
            if (user_keyword in transaction["Описание"]) or (user_keyword in transaction["Категория"]):
                result.append(transaction)
        except TypeError:
            continue
    json.dumps(result)
    logger.info(f"the resulting list {result}")
    return result
