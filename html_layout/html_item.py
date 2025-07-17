from typing import Union, Optional, List, Callable
from html_layout.html_formatters import (formatter_digit,
                                         formatter_percent,
                                         formatter_timestamp,
                                         formatter_times,
                                         formatter_date)
from html_layout.html_config import TRANSPARENT_COLOR
from dataclasses import dataclass


def make_stat_unit(class_name:  str,
                   value: Union[int, float, str],
                   formatter: Callable[[Union[int, float, str]], str]):
    return f'\t<div class="{class_name}">{formatter(value)}</div>'


@dataclass
class StatText:
    value: Union[Union[int, float, str]]
    formatter: Callable[[Union[int, float, str]], str]

    @property
    def html(self):
        return make_stat_unit('stat-text', self.value, self.formatter)


@dataclass
class StatDigit:
    value: Union[int, float]

    @property
    def html(self):
        return make_stat_unit('stat-digit', self.value, formatter_digit)


@dataclass
class StatNullDigit:
    @property
    def html(self):
        return f'\t<div class="stat-digit"></div>'


@dataclass
class StatPercent:
    value: Union[int, float]
    total: Union[int, float]

    @property
    def html(self):
        return make_stat_unit('stat-digit', self.value / self.total * 100, formatter_percent)


@dataclass
class StatDate:
    value: str

    @property
    def html(self):
        return make_stat_unit('stat-text', self.value, formatter_date)


@dataclass
class StatTimestamp:
    value: Union[int, float]

    @property
    def html(self):
        return make_stat_unit('stat-text', self.value, formatter_timestamp)


@dataclass
class StatTimes:
    value: int

    @property
    def html(self):
        return make_stat_unit('stat-digit', self.value, formatter_times)


@dataclass
class StatBar:
    values: List[Union[int, float]]
    colors: List[str]
    total: Union[int, float]

    @property
    def html(self):
        bar = ''

        bar += f'<div class="stat-bar-block">'
        for value, color in zip(self.values, self.colors):
            bar += f'\t<div class="stat-bar" style="width: {value / self.total * 100}%; background: {color};"></div>'
        bar += f'</div>'

        return bar


@dataclass
class StatPie:
    values: List[Union[int, float]]
    colors: List[str]
    total: Union[int, float]

    @property
    def html(self):
        start_angle = 0
        gradients = []
        for value, color in zip(self.values, self.colors):
            end_angle = start_angle + (value / self.total * 360)
            gradients.append(f'{color} {start_angle}deg {end_angle}deg')
            start_angle = end_angle
        gradients.append(f'{TRANSPARENT_COLOR} {start_angle}deg')

        return f'<div class="stat-pie" style="background: conic-gradient({", ".join(gradients)});"></div>'


@dataclass
class StatLongMessages:
    messages: List[str]

    @property
    def html(self):
        long_message = ''

        for message in self.messages:
            long_message += f'<div class="stat-long-message">{message}</div>'

        return long_message


@dataclass
class StatRow:
    title: str
    items: List[Union[StatText, StatDigit, StatNullDigit, StatPercent, StatDate, StatTimestamp, StatTimes, StatBar]]
    color: str = ''

    @property
    def html(self):
        stat_row = ''

        if self.color != '':
            stat_row += f'\n<div class="stat-row" style="color: {self.color};">' \
                        f'\n\t<div class="stat-title">{self.title}</div>'
        else:
            stat_row += f'\n<div class="stat-row">\n\t<div class="stat-title">{self.title}</div>'

        for item in self.items:
            stat_row += item.html
        stat_row += f'</div>'

        return stat_row


@dataclass
class WordMap:
    title: str
    wordmap: List[tuple]

    @staticmethod
    def __make_word_card(word: str, count: str):
        return f'<div class="word-card"><div class="word">{word}</div><div class="count">{count}</div></div>'

    @property
    def html(self):
        word_map = ''
        word_map += f'<div class="toggle-block collapsed"><div class="toggle-header stat-row">' \
                    f'<div class="stat-title">{self.title}</div><div class="toggle-icon">›' \
                    f'</div></div><div class="word-map">'
        for word, count in self.wordmap:
            word_map += self.__make_word_card(word, count)
        word_map += f'</div></div>'
        return word_map


@dataclass
class StatBlock:
    title: str
    rows: List[Union[StatRow, StatLongMessages, WordMap]]

    @property
    def html(self):
        block = ''
        block += f'<div class="stat-block"><div class="stat-header"><h3>{self.title}</h3></div>'
        for row in self.rows:
            block += row.html
        block += f'</div>'
        return block
