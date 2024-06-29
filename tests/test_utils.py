from unittest.mock import Mock, patch

import pytest
from pandas import DataFrame

from src.utils import (
    calculation_cashback,
    card_from_xlsx_file,
    exchange_rate,
    get_sp500_price,
    read_from_xlsx_file,
    select_range_by_date,
    top_five_transactions,
    total_amount_expences,
    user_greeting,
)


@pytest.fixture
def data() -> list:
    return [
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


@patch("pandas.read_excel")
def test_read_from_xlsx_file(mock_read: Mock) -> None:
    data1 = {1: ["a"], 2: ["b"]}
    mock_read.return_value = DataFrame(data1)
    assert read_from_xlsx_file("../data/operations.xls") == [{1: "a", 2: "b"}]


@patch("pandas.read_excel")
def test_select_range_by_date(mock_read: Mock, data: list) -> None:
    mock_read.return_value = DataFrame(data)
    assert select_range_by_date("2018-01-01 08:00:00") == [
        {
            "MCC": "",
            "Бонусы (включая кэшбэк)": 0,
            "Валюта операции": "RUB",
            "Валюта платежа": "RUB",
            "Дата операции": "01.01.2018 12:49:53",
            "Дата платежа": "01.01.2018",
            "Категория": "Переводы",
            "Кэшбэк": "",
            "Номер карты": "",
            "Округление на инвесткопилку": 0,
            "Описание": "Линзомат ТЦ Юность",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Сумма операции с округлением": 3000.0,
            "Сумма платежа": -3000.0,
        }
    ]


@pytest.mark.parametrize(
    "time, greeting",
    (
        ["2023-01-02 08:00:00", "Доброе утро"],
        ["2023-01-02 13:00:00", "Добрый день"],
        ["2023-01-02 19:00:00", "Добрый вечер"],
        ["2023-01-02 02:00:00", "Доброй ночи"],
    ),
)
def test_user_greeting(time: str, greeting: str) -> None:
    assert user_greeting(time) == greeting


@patch("pandas.read_excel")
def test_card_from_xlsx_file(mock_read: Mock, data: list) -> None:
    mock_read.return_value = DataFrame(data)
    assert card_from_xlsx_file("2018-07-26 08:00:00") == ["7197"]


@patch("pandas.read_excel")
def test_total_amount_expences(mock_read: Mock, data: list) -> None:
    mock_read.return_value = DataFrame(data)
    assert total_amount_expences("2018-07-26 08:00:00") == {"7197": 32.92}


@patch("pandas.read_excel")
def test_calculation_cashback(mock_read: Mock, data: list) -> None:
    mock_read.return_value = DataFrame(data)
    assert calculation_cashback("2018-07-26 08:00:00") == [
        {"cashback": 0.3292, "last_digits": "7197", "total_spent": 32.92}
    ]


@patch("pandas.read_excel")
def test_top_five_transactions(mock_read: Mock, data: list) -> None:
    mock_read.return_value = DataFrame(data)
    assert top_five_transactions("2018-07-26 08:00:00") == [
        {
            "amount": 32.92,
            "category": "Транспорт",
            "date": "27.07.2018",
            "description": "Московский транспорт",
        }
    ]


@patch("requests.get")
def test_exchange_rate(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {"result": 1}
    assert exchange_rate(["USD", "EUR"]) == [
        {"currency": "USD", "rate": 1},
        {"currency": "EUR", "rate": 1},
    ]


@patch("requests.get")
def test_get_sp500_price(mock_get: Mock) -> None:
    mock_get.return_value.json.return_value = {
        "Time Series (1min)": {
            "2024-06-28 19:40:00": {
                "1. open": "173.0000",
                "2. high": "173.0000",
                "3. low": "173.0000",
                "4. close": "173.0000",
                "5. volume": "14",
            }
        }
    }
    assert get_sp500_price(["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]) == [
        {"price": "173.0000", "stock": "AAPL"},
        {"price": "173.0000", "stock": "AMZN"},
        {"price": "173.0000", "stock": "GOOGL"},
        {"price": "173.0000", "stock": "MSFT"},
        {"price": "173.0000", "stock": "TSLA"},
    ]
