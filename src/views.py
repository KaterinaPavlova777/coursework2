import json

from src.utils import (
    calculation_cashback,
    exchange_rate,
    get_sp500_price,
    top_five_transactions,
    user_greeting,
)


def main_page_info(user_date: str) -> dict:
    """
    Функция, которая возвращает json-ответ с данными для главной страницы.
    """
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

    return info_for_main_page
