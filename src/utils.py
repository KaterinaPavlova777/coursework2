import datetime
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

load_dotenv()
api_key = os.getenv("API_KEY")
headers = {"apikey": api_key}

api_key_2 = os.getenv("VANTAGE_API_KEY")


def read_from_xlsx_file(path: str) -> list:
    """
    Реализовывает считывание финансовых операций с XLSX-файлов.
    """
    logger.info(f"read_from_xlsx_file {path}")
    reviews = pd.read_excel(path)
    dict_filepath = reviews.to_dict(orient="records")
    logger.info(f"the resulting list {dict_filepath}")
    return dict_filepath


def select_range_by_date(user_data: str) -> list:
    """
    Функция, которая фильтрует данные с начала месяца, на который выпадает входящая дата, по входящую дату.
    """
    logger.info(f"select_range_by_date {user_data}")
    new_json = []
    data = read_from_xlsx_file("../data/operations.xls")
    for transaction in data:
        if (
            user_data[3:5] == transaction["Дата операции"][3:5]
            and user_data[0:2] >= transaction["Дата операции"][0:2]
        ):
            new_json.append(transaction)
    logger.info(f"the resulting list {new_json}")
    return new_json


def user_greeting(user_date: str) -> str:
    """
    Функция, которая принимает на вход строку с датой и временем,
    и возврвщвет приветствие в зависимости от текущего времени.
    """
    logger.info(f"user_greeting {user_date}")
    date_time = datetime.datetime.strptime(user_date, "%Y-%m-%d %H:%M:%S")

    hour = date_time.hour

    if 5 <= hour < 12:
        result_1 = "Доброе утро"
        logger.info(f"the resulting message {result_1}")
        return result_1
    elif 12 <= hour < 18:
        result_2 = "Добрый день"
        logger.info(f"the resulting message {result_2}")
        return result_2
    elif 18 <= hour < 23:
        result_3 = "Добрый вечер"
        logger.info(f"the resulting message {result_3}")
        return result_3
    else:
        result_4 = "Доброй ночи"
        logger.info(f"the resulting message {result_4}")
        return result_4


def card_from_xlsx_file(user_data: str) -> list:
    """
    Реализовывает считывание последних 4-х цифр карты с XLSX-файла по дате.
    """
    logger.info(f"card_from_xlsx_file {user_data}")
    data = select_range_by_date(user_data)

    user_cards = []

    for transaction in data:
        try:
            user_cards.append(transaction["Номер карты"][-4:])
        except TypeError:
            continue

    user_cards_set = set(user_cards)
    result = list(user_cards_set)
    logger.info(f"the resulting list {result}")
    return result


def total_amount_expences(user_data: str) -> dict:
    """
    Функция, которая принимает дату и возращает словарь с картами,
    и тратами с начала месяца, на который выпадает входящая дата, по входящую дату.
    """
    logger.info(f"total_amount_expences {user_data}")
    data = select_range_by_date(user_data)
    cards = card_from_xlsx_file(user_data)
    result = {}
    for card in cards:
        result[card] = 0
    for transaction in data:
        try:
            if transaction["Номер карты"][1:] in result.keys():
                result[transaction["Номер карты"][1:]] += transaction[
                    "Сумма операции с округлением"
                ]
        except TypeError:
            continue
    logger.info(f"the resulting dict {result}")
    return result


def calculation_cashback(user_data: str) -> list:
    """
    Функция, которая возвращает карты с расходами и кэшбеком.
    """
    logger.info(f"calculation_cashback {user_data}")
    data = total_amount_expences(user_data)
    result = []

    for k, v in data.items():
        result.append({k: v, "cashback": v / 100})
    logger.info(f"the resulting list {result}")
    return result


def top_five_transactions(user_data: str) -> list:
    """
    Функция, которая выводит топ-5 транзакций по сумме платежа.
    """
    logger.info(f"top_five_transactions {user_data}")
    data = select_range_by_date(user_data)
    result = sorted(
        data, key=lambda x: x["Сумма операции с округлением"], reverse=True
    )[0:5]
    logger.info(f"the resulting list {result}")
    return result


def exchange_rate(currency: str) -> float:
    """
    Функция, которая выводит курс валют.
    """
    logger.info(f"exchange_rate {currency}")
    url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
    response = requests.get(url, headers=headers).json()
    result = response["result"]
    logger.info(f"the resulting currency {result}")
    return result


def get_sp500_price(stock: str) -> float:
    """
    Функция, которая возращает стоимость акций S&P500.
    """
    logger.info(f"get_sp500_price {stock}")
    api = api_key_2
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey={api}"

    response = requests.get(url)
    data = response.json()

    latest_data = data["Time Series (1min)"]
    latest_timestamp = sorted(latest_data.keys())[0]
    latest_price = latest_data[latest_timestamp]["4. close"]

    logger.info(f"the resulting stock {latest_price}")
    return latest_price
