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

    info_for_main_page = {
        "greeting": user_greeting(user_date),
        "cards": calculation_cashback(user_date),
        "top_transactions": top_five_transactions(user_date),
        "currency_rates": exchange_rate(),
        "stock_prices": get_sp500_price(),
    }

    return info_for_main_page
