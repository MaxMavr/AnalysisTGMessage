from typing import Union
from datetime import datetime
from locale import setlocale, LC_TIME

setlocale(LC_TIME, 'russian')


def formatter_date(date: str):
    return datetime.strptime(date, "%Y-%m-%d").strftime("%d %B %Y").lower()


def formatter_timestamp(timestamp: int):
    return datetime.fromtimestamp(timestamp).strftime("%d %B %Y, %H:%M<small>:%S</small>").lower()


def formatter_times(seconds: int):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}<small>:{seconds:02d}</small>"


def formatter_digit(digit: Union[int, float]):
    return f'{digit:,}'.replace(",", "&thinsp;").replace(".", ",")


def formatter_percent(percent: Union[int, float]):
    return f'<i>{percent * 100:,.2f}%</i>'.replace(".", ",")
