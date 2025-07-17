from user import User
from typing import Union, Optional, List, Dict, Callable
from html_layout.html_formatters import (formatter_timestamp, formatter_times,
                                         formatter_digit, formatter_percent, formatter_date)


DEFAULT_COLOR: str = '#1A1A1A'
TRANSPARENT_COLOR: str = '#FFFFFF'

SENSIBLE_COLOR: str = '#f72585'
FORWARDED_COLOR: str = ''
PIN_COLOR: str = ''
VOICES_COLOR: str = '#7209b7'
VIDEOS_COLOR: str = '#480ca8'
PHONE_CALL_COLOR: str = ''
STICKERS_COLOR: str = '#3f37c9'

SENSIBLE_LIGHT_COLOR: str = SENSIBLE_COLOR + 'AA'
FORWARDED_LIGHT_COLOR: str = FORWARDED_COLOR + 'AA'
PIN_LIGHT_COLOR: str = PIN_COLOR + 'AA'
VOICES_LIGHT_COLOR: str = VOICES_COLOR + 'AA'
VIDEOS_LIGHT_COLOR: str = VIDEOS_COLOR + 'AA'
PHONE_CALL_LIGHT_COLOR: str = PHONE_CALL_COLOR + 'AA'
STICKERS_LIGHT_COLOR: str = STICKERS_COLOR + 'AA'

HTML: str = \
    '''<!DOCTYPE html>
    <html lang="ru-RU">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Анализ сообщений</title>
        <link rel="icon" type="image/png" sizes="16x16" href="https://web.telegram.org/k/assets/img/favicon-16x16.png?v=jw3mK7G9Ry">
        <link rel="stylesheet" type="text/css" href="style.css">
      </head>
    </head>
    <body>'''


class StatDigit:
    def __init__(self, digit: Union[int, float],
                 formatter: Optional[Callable[[Union[int, float]], str]] = None):
        self.digit = digit
        self.formatter = formatter

    def insert_to_html(self):
        global HTML
        if self.formatter:
            HTML += f'\t<div class="stat-digit">{self.formatter(self.digit)}</div>'
        else:
            HTML += f'\t<div class="stat-digit">{formatter_digit(self.digit)}</div>'


NULL_STATDIGIT = StatDigit(0, lambda i: '')


class StatText:
    def __init__(self, text: Union[int, float, str],
                 formatter: Optional[Callable[[Union[int, float, str]], str]] = None):
        self.text = text
        self.formatter = formatter

    def insert_to_html(self):
        global HTML
        if self.formatter:
            HTML += f'\t<div class="stat-text">{self.formatter(self.text)}</div>'
        else:
            HTML += f'\t<div class="stat-text">{self.text}</div>'


class StatBar:
    def __init__(self, values: List[Union[int, float]], colors: List[str], total: Union[int, float] = None):
        self.colors = colors
        self.values = []
        if total:
            for value in values:
                self.values.append(value / total * 100)
        else:
            self.values = values

    def insert_to_html(self):
        global HTML
        HTML += f'<div class="stat-bar-block">'
        for value, color in zip(self.values, self.colors):
            HTML += f'\t<div class="stat-bar" style="width: {value}%; background: {color};"></div>'
        HTML += f'</div>'


class StatPie:
    def __init__(self, values: List[Union[int, float]], colors: List[str], total: Union[int, float]):
        start_angle = 0
        self.gradients = []
        for value, color in zip(values, colors):
            end_angle = start_angle + (value / total * 360)
            self.gradients.append(f'{color} {start_angle}deg {end_angle}deg')
            start_angle = end_angle
        self.gradients.append(f'{TRANSPARENT_COLOR} {start_angle}deg')

    def insert_to_html(self):
        global HTML
        HTML += f'<div class="stat-pie" style="background: conic-gradient({", ".join(self.gradients)});"></div>'


# class StatPlot:
#     def __init__(self, x: List[Union[int, float, str]], y: List[Union[int, float]],
#                  x_labels: List[Union[str]] = None, y_labels: List[Union[str]] = None):
#
#         x_min, x_max = min(x), max(x)
#         y_min, y_max = min(y), max(y)
#
#         # Рассчитаем масштабные коэффициенты
#         plot_width = width - 2 * padding
#         plot_height = height - 2 * padding
#
#         def scale_x(val):
#             return padding + (val - x_min) * plot_width / (x_max - x_min or 1)
#
#         def scale_y(val):
#             return height - padding - (val - y_min) * plot_height / (y_max - y_min or 1)
#
#         # Генерация SVG-пути для графика
#         path_points = []
#         for i, (x_val, y_val) in enumerate(zip(x, y)):
#             x_scaled = scale_x(x_val)
#             y_scaled = scale_y(y_val)
#             if i == 0:
#                 path_points.append(f"M{x_scaled},{y_scaled}")
#             else:
#                 path_points.append(f"L{x_scaled},{y_scaled}")
#
#     def insert_to_html(self):
#         global HTML
#         HTML += f'<div class="stat-pie" style="background: conic-gradient({", ".join(self.gradients)});"></div>'


class StatLongMsg:
    def __init__(self, messages: List[str]):
        self.messages = messages

    def insert_to_html(self):
        global HTML
        for message in self.messages:
            HTML += f'<div class="stat-long-message">{message}</div>'


class StatRow:
    def __init__(self, title: str, *values: Union[StatDigit, StatBar, StatText, StatLongMsg], color: str = ''):
        self.title = title
        self.values = values
        self.color = color

    def insert_to_html(self):
        global HTML
        if self.color != '':
            HTML += f'\n<div class="stat-row" style="color: {self.color};">\n\t<div class="stat-title">{self.title}</div>'
        else:
            HTML += f'\n<div class="stat-row">\n\t<div class="stat-title">{self.title}</div>'
        for value in self.values:
            value.insert_to_html()
        HTML += f'</div>'


class WordMap:
    def __init__(self, title: str, wordmap: List[tuple]):
        self.title = title
        self.wordmap = wordmap

    @staticmethod
    def __make_word_card(word: str, count: str):
        return f'<div class="word-card"><div class="word">{word}</div><div class="count">{count}</div></div>'

    def insert_to_html(self):
        global HTML
        HTML += f'<div class="toggle-block collapsed"><div class="toggle-header stat-row">' \
                f'<div class="stat-title">{self.title}</div><div class="toggle-icon">›' \
                f'</div></div><div class="word-map">'
        for word, count in self.wordmap:
            HTML += self.__make_word_card(word, count)
        HTML += f'</div></div>'


class StatBlock:
    def __init__(self, title: str, *rows: Union[StatRow, StatLongMsg, WordMap]):
        self.title = title
        self.rows = rows

    def insert_to_html(self):
        global HTML
        HTML += f'<div class="stat-block"><div class="stat-header"><h3>{self.title}</h3></div>'
        for row in self.rows:
            row.insert_to_html()
        HTML += f'</div>'


def make_html(users: List[User], chat: User, output_name: str = 'report'):
    global HTML
    HTML += f'<header><h1>Анализ сообщений чата <i>«{chat.name}»</i></h1></header>' \
            '<main>'

    HTML += '<div class="two-sides">' \
            '<div>'

    chat_count_unique_chars = len(chat.chars_map) + len(chat.punctuation_map)
    chat_count_unique_words = len(chat.words_map)

    chat_max_day_count_messages = max(chat.days_count_messages.values())
    chat_max_days_count_messages = [StatText(day, formatter_date)
                                    for day, count in chat.days_count_messages.items()
                                    if count == chat_max_day_count_messages]

    StatBlock('Даты',
              StatRow('Первое',
                      StatText(chat.first_messages_timestamp, formatter_timestamp)
                      ),
              StatRow('Последнее',
                      StatText(chat.last_messages_timestamp, formatter_timestamp)
                      ),
              StatRow('Максимальный',
                      *chat_max_days_count_messages,
                      StatText(chat_max_day_count_messages, lambda i: f'{i} сообщ.')
                      ),
              ).insert_to_html()

    StatBlock('Сообщения',
              StatRow('Количество',
                      StatDigit(chat.count_messages)
                      ),
              StatRow('Осмысленных',
                      StatDigit(chat.count_sensible_messages),
                      NULL_STATDIGIT,
                      StatDigit(chat.count_sensible_messages / chat.count_messages, formatter_percent),
                      color=SENSIBLE_COLOR
                      ),
              StatRow('Пересланных',
                      StatDigit(chat.count_forwarded_messages),
                      NULL_STATDIGIT,
                      StatDigit(chat.count_forwarded_messages / chat.count_messages, formatter_percent),
                      color=FORWARDED_COLOR
                      ),
              StatRow('Закреплённых',
                      StatDigit(chat.count_pin_messages),
                      NULL_STATDIGIT,
                      StatDigit(chat.count_pin_messages / chat.count_messages, formatter_percent),
                      color=PIN_COLOR
                      ),
              StatRow('Голосовых',
                      StatDigit(chat.count_voices),
                      StatDigit(chat.duration_voices, formatter_times),
                      StatDigit(chat.count_voices / chat.count_messages, formatter_percent),
                      color=VOICES_COLOR
                      ),
              StatRow('Кружков',
                      StatDigit(chat.count_videos),
                      StatDigit(chat.duration_videos, formatter_times),
                      StatDigit(chat.count_videos / chat.count_messages, formatter_percent),
                      color=VIDEOS_COLOR
                      ),
              StatRow('Стикеров',
                      StatDigit(chat.count_stickers),
                      NULL_STATDIGIT,
                      StatDigit(chat.count_stickers / chat.count_messages, formatter_percent),
                      color=STICKERS_COLOR
                      ),
              StatRow('Звонков',
                      StatDigit(chat.count_phone_call),
                      StatDigit(chat.duration_phone_call, formatter_times),
                      StatDigit(chat.count_phone_call / chat.count_messages, formatter_percent),
                      color=PHONE_CALL_COLOR
                      ),
              StatRow('Средняя длина',
                      StatText(chat.count_chars / chat.count_messages, lambda i: f'~{round(i)} симв.')
                      )
              ).insert_to_html()

    HTML += '<div class="two-sides">'

    StatBlock('Слова',
              StatRow('Количество',
                      StatDigit(chat.count_words)
                      ),
              StatRow('Уникальных',
                      StatDigit(chat_count_unique_words)
                      )
              ).insert_to_html()

    StatBlock('Символы',
              StatRow('Количество',
                      StatDigit(chat.count_chars)
                      ),
              StatRow('Уникальных',
                      StatDigit(chat_count_unique_chars)
                      )
              ).insert_to_html()

    HTML += '</div>'
    HTML += '</div>'

    count_others_messages = chat.count_pin_messages + chat.count_phone_call

    StatPie([chat.count_sensible_messages, chat.count_voices, chat.count_videos,
             chat.count_stickers, count_others_messages],
            [SENSIBLE_COLOR, VOICES_COLOR, VIDEOS_COLOR,
             STICKERS_COLOR, DEFAULT_COLOR],
            chat.count_messages
            ).insert_to_html()

    HTML += '</div>'

    for user in users:
        HTML += f'<section class="user"><div class="user-header"><h2>{user.name}</h2></div>'

        count_unique_chars = len(user.chars_map) + len(user.punctuation_map)
        count_unique_words = len(user.words_map)

        max_day_count_messages = max(user.days_count_messages.values())
        max_days_count_messages = [StatText(day, formatter_date)
                                   for day, count in user.days_count_messages.items()
                                   if count == max_day_count_messages]

        StatBlock('Даты',
                  StatRow('Первое',
                          StatText(user.first_messages_timestamp, formatter_timestamp)
                          ),
                  StatRow('Последнее',
                          StatText(user.last_messages_timestamp, formatter_timestamp)
                          ),
                  StatRow('Максимальный',
                          *max_days_count_messages,
                          StatText(max_day_count_messages, lambda i: f'{i} сообщ.')
                          ),
                  ).insert_to_html()

        StatBlock('Сообщения',
                  StatRow('Количество',
                          StatDigit(user.count_messages),
                          StatDigit(user.count_messages / chat.count_messages, formatter_percent),
                          NULL_STATDIGIT,
                          StatBar([user.count_messages], [''], chat.count_messages),
                          StatBar([user.count_messages], [''], user.count_messages),
                          ),
                  StatRow('Осмысленных',
                          StatDigit(user.count_sensible_messages),
                          StatDigit(user.count_sensible_messages / chat.count_sensible_messages, formatter_percent),
                          StatDigit(user.count_sensible_messages / user.count_messages, formatter_percent),
                          StatBar([user.count_sensible_messages], [SENSIBLE_COLOR], chat.count_sensible_messages),
                          StatBar([user.count_sensible_messages], [SENSIBLE_COLOR], user.count_messages),
                          color=SENSIBLE_COLOR
                          ),
                  StatRow('Пересланных',
                          StatDigit(user.count_forwarded_messages),
                          StatDigit(user.count_forwarded_messages / chat.count_forwarded_messages, formatter_percent),
                          StatDigit(user.count_forwarded_messages / user.count_messages, formatter_percent),
                          StatBar([user.count_forwarded_messages], [FORWARDED_COLOR], chat.count_forwarded_messages),
                          StatBar([user.count_forwarded_messages], [FORWARDED_COLOR], user.count_messages),
                          color=FORWARDED_COLOR
                          ),
                  StatRow('Закреплённых',
                          StatDigit(user.count_pin_messages),
                          StatDigit(user.count_pin_messages / chat.count_pin_messages, formatter_percent),
                          StatDigit(user.count_pin_messages / user.count_messages, formatter_percent),
                          StatBar([user.count_pin_messages], [PIN_COLOR], chat.count_pin_messages),
                          StatBar([user.count_pin_messages], [PIN_COLOR], user.count_messages),
                          color=PIN_COLOR
                          ),
                  StatRow('Стикеров',
                          StatDigit(user.count_stickers),
                          StatDigit(user.count_stickers / chat.count_stickers, formatter_percent),
                          StatDigit(user.count_stickers / user.count_messages, formatter_percent),
                          StatBar([user.count_stickers], [STICKERS_COLOR], chat.count_stickers),
                          StatBar([user.count_stickers], [STICKERS_COLOR], user.count_messages),
                          color=STICKERS_COLOR
                          )
                  ).insert_to_html()

        StatBlock('Голосовых',
                  StatRow('Количество',
                          StatDigit(user.count_voices),
                          StatDigit(user.count_voices / chat.count_voices, formatter_percent),
                          StatDigit(user.count_voices / user.count_messages, formatter_percent),
                          StatBar([user.count_voices], [VOICES_COLOR], chat.count_voices),
                          StatBar([user.count_voices], [VOICES_COLOR], user.count_messages),
                          color=VOICES_COLOR
                          ),
                  StatRow('Время',
                          StatDigit(user.duration_voices, formatter_times),
                          StatDigit(user.duration_voices / chat.duration_voices, formatter_percent)
                          ),
                  StatRow('Средняя длина',
                          StatText(int(user.duration_voices / user.count_voices), formatter_times)
                          )
                  ).insert_to_html()

        StatBlock('Кружков',
                  StatRow('Количество',
                          StatDigit(user.count_videos),
                          StatDigit(user.count_videos / chat.count_videos, formatter_percent),
                          StatDigit(user.count_videos / user.count_messages, formatter_percent),
                          StatBar([user.count_videos], [VIDEOS_COLOR], chat.count_videos),
                          StatBar([user.count_videos], [VIDEOS_COLOR], user.count_messages),
                          color=VIDEOS_COLOR
                          ),
                  StatRow('Время',
                          StatDigit(user.duration_videos, formatter_times),
                          StatDigit(user.duration_videos / chat.duration_videos, formatter_percent)
                          ),
                  StatRow('Средняя длина',
                          StatText(int(chat.duration_videos / chat.count_videos), formatter_times)
                          )
                  ).insert_to_html()

        StatBlock('Звонков',
                  StatRow('Количество',
                          StatDigit(user.count_phone_call),
                          StatDigit(user.count_phone_call / chat.count_phone_call, formatter_percent),
                          StatDigit(user.count_phone_call / user.count_messages, formatter_percent),
                          StatBar([user.count_phone_call], [PHONE_CALL_COLOR], chat.count_phone_call),
                          StatBar([user.count_phone_call], [PHONE_CALL_COLOR], user.count_messages),
                          color=PHONE_CALL_COLOR
                          ),
                  StatRow('Время',
                          StatDigit(user.duration_phone_call, formatter_times),
                          StatDigit(user.duration_phone_call / chat.duration_phone_call, formatter_percent)
                          ),
                  StatRow('Средняя длина',
                          StatText(int(chat.duration_phone_call / chat.count_phone_call), formatter_times)
                          )
                  ).insert_to_html()

        HTML += '<div class="two-sides">'

        StatPie([user.count_sensible_messages, user.count_voices, user.count_videos, user.count_stickers],
                [SENSIBLE_COLOR, VOICES_COLOR, VIDEOS_COLOR, STICKERS_COLOR],
                chat.count_messages
                ).insert_to_html()

        StatPie([user.count_sensible_messages, user.count_voices, user.count_videos, user.count_stickers],
                [SENSIBLE_COLOR, VOICES_COLOR, VIDEOS_COLOR, STICKERS_COLOR],
                user.count_messages
                ).insert_to_html()

        HTML += '</div>'

        StatBlock('Длинны сообщений',
                  StatRow('Средняя',
                          StatText(user.count_chars / user.count_messages, lambda i: f'~{round(i)} симв.')
                          ),
                  StatRow('Максимальная',
                          StatText(user.len_longest_message, lambda i: f'{i} симв.'),
                          ),
                  StatLongMsg(user.longest_messages)
                  ).insert_to_html()

        StatBlock('Слова',
                  StatRow('Количество',
                          StatDigit(user.count_words),
                          StatDigit(user.count_words / chat.count_words, formatter_percent)
                          ),
                  StatRow('Уникальных',
                          StatDigit(count_unique_words),
                          StatDigit(count_unique_words / chat_count_unique_words, formatter_percent)
                          ),
                  WordMap('Карта <i>по количеству</i>',
                          sorted(user.words_map.items(), key=lambda item: item[1], reverse=True)),
                  WordMap('Карта <i>по алфавиту</i>',
                          sorted(user.words_map.items(), key=lambda item: item[0].lower()))
                  ).insert_to_html()

        StatBlock('Символы',
                  StatRow('Количество',
                          StatDigit(user.count_chars),
                          StatDigit(user.count_chars / chat.count_chars, formatter_percent)
                          ),
                  StatRow('Уникальных',
                          StatDigit(count_unique_chars),
                          StatDigit(count_unique_chars / chat_count_unique_chars, formatter_percent)
                          ),
                  WordMap('Карта <i>букв</i>',
                          sorted(user.chars_map.items(), key=lambda item: item[1], reverse=True)),
                  WordMap('Карта <i>символов</i>',
                          sorted(user.punctuation_map.items(), key=lambda item: item[1], reverse=True))
                  ).insert_to_html()

        HTML += '</section>'

    HTML += '</main><script src="script.js"></script></body>'

    with open(f'result/{output_name}.html', 'w', encoding='utf-8') as file:
        file.write(HTML)
