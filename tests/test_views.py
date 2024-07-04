import json
from unittest.mock import patch

from pandas import DataFrame

from src.views import main_page_info


def test_main_page_info() -> None:
    with patch("builtins.open") as mock_open:
        with patch("pandas.read_excel") as mock_read:
            with patch("src.views.exchange_rate") as mock_exchange:
                with patch("src.views.get_sp500_price") as mock_sp500:
                    data = [
                        {
                            "Дата операции": "01.01.2018 12:49:53",
                            "Дата платежа": "01.01.2018",
                            "Номер карты": "",
                            "Статус": "OK",
                            "Сумма операции": -3000.0,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -3000.0,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "",
                            "Категория": "Переводы",
                            "MCC": "",
                            "Описание": "Линзомат ТЦ Юность",
                            "Бонусы (включая кэшбэк)": 0,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 3000.0,
                        },
                        {
                            "Дата операции": "26.07.2018 09:18:00",
                            "Дата платежа": "27.07.2018",
                            "Номер карты": "*7197",
                            "Статус": "OK",
                            "Сумма операции": -32.92,
                            "Валюта операции": "RUB",
                            "Сумма платежа": -32.92,
                            "Валюта платежа": "RUB",
                            "Кэшбэк": "",
                            "Категория": "Транспорт",
                            "MCC": 4131.0,
                            "Описание": "Московский транспорт",
                            "Бонусы (включая кэшбэк)": 0,
                            "Округление на инвесткопилку": 0,
                            "Сумма операции с округлением": 32.92,
                        },
                    ]

                    mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(
                        {
                            "user_currencies": ["USD", "EUR"],
                            "user_stocks": [
                                "AAPL",
                                "AMZN",
                                "GOOGL",
                                "MSFT",
                                "TSLA",
                            ],
                        }
                    )

                    mock_read.return_value = DataFrame(data)
                    mock_exchange.return_value = [
                        {"currency": "USD", "rate": 1},
                        {"currency": "EUR", "rate": 1},
                    ]
                    mock_sp500.return_value = [
                        {"price": "173.0000", "stock": "AAPL"},
                        {"price": "173.0000", "stock": "AMZN"},
                        {"price": "173.0000", "stock": "GOOGL"},
                        {"price": "173.0000", "stock": "MSFT"},
                        {"price": "173.0000", "stock": "TSLA"},
                    ]
                    assert main_page_info("2018-07-26 09:18:00") == {
                        "cards": [
                            {
                                "cashback": 0.3292,
                                "last_digits": "7197",
                                "total_spent": 32.92,
                            }
                        ],
                        "currency_rates": [
                            {"currency": "USD", "rate": 1},
                            {"currency": "EUR", "rate": 1},
                        ],
                        "greeting": "Доброе утро",
                        "stock_prices": [
                            {"price": "173.0000", "stock": "AAPL"},
                            {"price": "173.0000", "stock": "AMZN"},
                            {"price": "173.0000", "stock": "GOOGL"},
                            {"price": "173.0000", "stock": "MSFT"},
                            {"price": "173.0000", "stock": "TSLA"},
                        ],
                        "top_transactions": [
                            {
                                "amount": 32.92,
                                "category": "Транспорт",
                                "date": "27.07.2018",
                                "description": "Московский транспорт",
                            }
                        ],
                    }
