import json
import logging

from src.utils import (
    calculation_cashback,
    exchange_rate,
    get_sp500_price,
    top_five_transactions,
    user_greeting,
)

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def main_page_info(user_date: str) -> dict:
    """
    Функция, которая возвращает json-ответ с данными для главной страницы.
    """
    logger.info(f'main_page_info {user_date}')
    with open("../user_settings.json", encoding="utf-8") as file:
        user_settings = json.load(file)
    list_currencies = user_settings["user_currencies"]
    list_stocks = user_settings["user_stocks"]
    info_for_main_page = {
        "greeting": user_greeting(user_date),
        "cards": calculation_cashback(user_date),
        "top_transactions": top_five_transactions(user_date),
        "currency_rates": exchange_rate(list_currencies),
        "stock_prices": get_sp500_price(list_stocks),
    }
    logger.info(f'the resulting dict {info_for_main_page}')
    return info_for_main_page
