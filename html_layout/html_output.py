from user import User
from typing import List, Union
from html_layout.html_config import *
from html_layout.html_item import (StatText,
                                   StatDigit,
                                   StatNullDigit,
                                   StatPercent,
                                   StatDate,
                                   StatTimestamp,
                                   StatTimes,
                                   StatBar,
                                   StatPie,
                                   StatLongMessages,
                                   StatRow,
                                   WordMap,
                                   StatBlock)


def calculate_average(values: list):
    n = len(values)
    return sum(values) / n


def calculate_median(values: List[Union[int, float]]):
    n = len(values)

    if n % 2 == 1:
        median = values[n // 2]
    else:
        median = (values[n // 2 - 1] + values[n // 2]) / 2

    return median


def make_html(users: List[User], chat: User, output_name: str = 'report'):
    html = HTML_START

    html += f'<header><h1>Анализ сообщений чата <i>«{chat.name}»</i></h1></header>' \
            '<main>'

    html += '<div class="two-sides">' \
            '<div>'

    chat_count_unique_chars = len(chat.chars_map) + len(chat.punctuation_map)
    chat_count_unique_words = len(chat.words_map)

    chat_max_day_count_messages = max(chat.days_count_messages.values())
    chat_max_days_count_messages = [StatDate(day)
                                    for day, count in chat.days_count_messages.items()
                                    if count == chat_max_day_count_messages]

    html += StatBlock('Дни',
                      [
                          StatRow('Первое сообщение',
                                  [StatTimestamp(chat.first_messages_timestamp)]
                                  ),
                          StatRow('Последнее сообщение',
                                  [StatTimestamp(chat.last_messages_timestamp)]
                                  ),
                          StatRow('Максимальное за день',
                                  [*chat_max_days_count_messages,
                                   StatText(chat_max_day_count_messages, lambda i: f'{i} сообщ.')]
                                  ),
                          StatRow('Среднее за день',
                                  [StatText(int(calculate_average(list(chat.days_count_messages.values()))), lambda i: f'~{i} сообщ.')]
                                  ),
                          StatRow('Медианное за день',
                                  [StatText(calculate_median(list(chat.days_count_messages.values())), lambda i: f'{i} сообщ.')]
                                  )
                      ]
                      ).html

    html += StatBlock('Сообщения',
                      [
                          StatRow('Количество',
                                  [StatDigit(chat.count_messages)]
                                  ),
                          StatRow('Осмысленных',
                                  [StatDigit(chat.count_sensible_messages),
                                   StatNullDigit(),
                                   StatPercent(chat.count_sensible_messages, chat.count_messages)],
                                  color=SENSIBLE_COLOR
                                  ),
                          StatRow('Пересланных',
                                  [StatDigit(chat.count_forwarded_messages),
                                   StatNullDigit(),
                                   StatPercent(chat.count_forwarded_messages, chat.count_messages)],
                                  color=FORWARDED_COLOR
                                  ),
                          StatRow('Закреплённых',
                                  [StatDigit(chat.count_pin_messages),
                                   StatNullDigit(),
                                   StatPercent(chat.count_pin_messages, chat.count_messages)],
                                  color=PIN_COLOR
                                  ),
                          StatRow('Голосовых',
                                  [StatDigit(chat.count_voices),
                                   StatTimes(chat.duration_voices),
                                   StatPercent(chat.count_voices, chat.count_messages)],
                                  color=VOICES_COLOR
                                  ),
                          StatRow('Кружков',
                                  [StatDigit(chat.count_videos),
                                   StatTimes(chat.duration_videos),
                                   StatPercent(chat.count_videos, chat.count_messages)],
                                  color=VIDEOS_COLOR
                                  ),
                          StatRow('Стикеров',
                                  [StatDigit(chat.count_stickers),
                                   StatNullDigit(),
                                   StatPercent(chat.count_stickers, chat.count_messages)],
                                  color=STICKERS_COLOR
                                  ),
                          StatRow('Звонков',
                                  [StatDigit(chat.count_phone_call),
                                   StatTimes(chat.duration_phone_call),
                                   StatPercent(chat.count_phone_call, chat.count_messages)],
                                  color=PHONE_CALL_COLOR
                                  ),
                          StatRow('Средняя длина',
                                  [StatText(chat.count_chars / chat.count_messages, lambda i: f'~{round(i)} симв.')]
                                  )
                      ]
                      ).html

    html += '<div class="two-sides">'

    html += StatBlock('Слова',
                      [
                          StatRow('Количество',
                                  [StatDigit(chat.count_words)]
                                  ),
                          StatRow('Уникальных',
                                  [StatDigit(chat_count_unique_words)]
                                  )
                      ]
                      ).html

    html += StatBlock('Символы',
                      [
                          StatRow('Количество',
                                  [StatDigit(chat.count_chars)]
                                  ),
                          StatRow('Уникальных',
                                  [StatDigit(chat_count_unique_chars)]
                                  )
                      ]
                      ).html

    html += '</div>'
    html += '</div>'

    count_others_messages = chat.count_pin_messages + chat.count_phone_call

    html += StatPie([chat.count_sensible_messages, chat.count_voices, chat.count_videos,
                     chat.count_stickers, count_others_messages],
                    [SENSIBLE_COLOR, VOICES_COLOR, VIDEOS_COLOR,
                     STICKERS_COLOR, DEFAULT_COLOR],
                    chat.count_messages
                    ).html

    html += '</div>'

    for user in users:
        html += f'<section class="user"><div class="user-header"><h2>{user.name}</h2></div>'

        count_unique_chars = len(user.chars_map) + len(user.punctuation_map)
        count_unique_words = len(user.words_map)

        max_day_count_messages = max(user.days_count_messages.values())
        max_days_count_messages = [StatDate(day) for day, count in user.days_count_messages.items()
                                   if count == max_day_count_messages]

        html += StatBlock('Дни',
                          [
                              StatRow('Первое',
                                      [StatTimestamp(user.first_messages_timestamp)]
                                      ),
                              StatRow('Последнее',
                                      [StatTimestamp(user.last_messages_timestamp)]
                                      ),
                              StatRow('Максимальный',
                                      [*max_days_count_messages,
                                       StatText(max_day_count_messages, lambda i: f'{i} сообщ.')]
                                      )
                          ],
                          ).html

        html += StatBlock('Сообщения',
                          [
                              StatRow('Количество',
                                      [StatDigit(user.count_messages),
                                       StatPercent(user.count_messages, chat.count_messages),
                                       StatNullDigit(),
                                       StatBar([user.count_messages], [''], chat.count_messages),
                                       StatBar([user.count_messages], [''], user.count_messages)],
                                      ),
                              StatRow('Осмысленных',
                                      [StatDigit(user.count_sensible_messages),
                                       StatPercent(user.count_sensible_messages, chat.count_sensible_messages),
                                       StatPercent(user.count_sensible_messages, user.count_messages),
                                       StatBar([user.count_sensible_messages], [SENSIBLE_COLOR],
                                               chat.count_sensible_messages),
                                       StatBar([user.count_sensible_messages], [SENSIBLE_COLOR], user.count_messages)],
                                      color=SENSIBLE_COLOR
                                      ),
                              StatRow('Пересланных',
                                      [StatDigit(user.count_forwarded_messages),
                                       StatPercent(user.count_forwarded_messages, chat.count_forwarded_messages),
                                       StatPercent(user.count_forwarded_messages, user.count_messages),
                                       StatBar([user.count_forwarded_messages], [FORWARDED_COLOR],
                                               chat.count_forwarded_messages),
                                       StatBar([user.count_forwarded_messages], [FORWARDED_COLOR],
                                               user.count_messages)],
                                      color=FORWARDED_COLOR
                                      ),
                              StatRow('Закреплённых',
                                      [StatDigit(user.count_pin_messages),
                                       StatPercent(user.count_pin_messages, chat.count_pin_messages),
                                       StatPercent(user.count_pin_messages, user.count_messages),
                                       StatBar([user.count_pin_messages], [PIN_COLOR], chat.count_pin_messages),
                                       StatBar([user.count_pin_messages], [PIN_COLOR], user.count_messages)],
                                      color=PIN_COLOR
                                      ),
                              StatRow('Стикеров',
                                      [StatDigit(user.count_stickers),
                                       StatPercent(user.count_stickers, chat.count_stickers),
                                       StatPercent(user.count_stickers, user.count_messages),
                                       StatBar([user.count_stickers], [STICKERS_COLOR], chat.count_stickers),
                                       StatBar([user.count_stickers], [STICKERS_COLOR], user.count_messages)],
                                      color=STICKERS_COLOR
                                      )
                          ]
                          ).html

        html += StatBlock('Голосовых',
                          [
                              StatRow('Количество',
                                      [StatDigit(user.count_voices),
                                       StatPercent(user.count_voices, chat.count_voices),
                                       StatPercent(user.count_voices, user.count_messages),
                                       StatBar([user.count_voices], [VOICES_COLOR], chat.count_voices),
                                       StatBar([user.count_voices], [VOICES_COLOR], user.count_messages)],
                                      color=VOICES_COLOR
                                      ),
                              StatRow('Время',
                                      [StatTimes(user.duration_voices),
                                       StatPercent(user.duration_voices, chat.duration_voices)]
                                      ),
                              StatRow('Средняя длина',
                                      [StatTimes(int(user.duration_voices / user.count_voices))]
                                      )
                          ]
                          ).html

        html += StatBlock('Кружков',
                          [StatRow('Количество',
                                   [StatDigit(user.count_videos),
                                    StatPercent(user.count_videos, chat.count_videos),
                                    StatPercent(user.count_videos, user.count_messages),
                                    StatBar([user.count_videos], [VIDEOS_COLOR], chat.count_videos),
                                    StatBar([user.count_videos], [VIDEOS_COLOR], user.count_messages)],
                                   color=VIDEOS_COLOR
                                   ),
                           StatRow('Время',
                                   [StatTimes(user.duration_videos),
                                    StatPercent(user.duration_videos, chat.duration_videos)]
                                   ),
                           StatRow('Средняя длина',
                                   [StatTimes(int(chat.duration_videos / chat.count_videos))]
                                   )]
                          ).html

        html += StatBlock('Звонков',
                          [
                              StatRow('Количество',
                                      [StatDigit(user.count_phone_call),
                                       StatPercent(user.count_phone_call, chat.count_phone_call),
                                       StatPercent(user.count_phone_call, user.count_messages),
                                       StatBar([user.count_phone_call], [PHONE_CALL_COLOR], chat.count_phone_call),
                                       StatBar([user.count_phone_call], [PHONE_CALL_COLOR], user.count_messages)],
                                      color=PHONE_CALL_COLOR
                                      ),
                              StatRow('Время',
                                      [StatTimes(user.duration_phone_call),
                                       StatPercent(user.duration_phone_call, chat.duration_phone_call)]
                                      ),
                              StatRow('Средняя длина',
                                      [StatTimes(int(chat.duration_phone_call / chat.count_phone_call))]
                                      )]
                          ).html

        html += '<div class="two-sides">'

        html += StatPie([user.count_sensible_messages, user.count_voices, user.count_videos, user.count_stickers],
                        [SENSIBLE_COLOR, VOICES_COLOR, VIDEOS_COLOR, STICKERS_COLOR],
                        chat.count_messages
                        ).html

        html += StatPie([user.count_sensible_messages, user.count_voices, user.count_videos, user.count_stickers],
                        [SENSIBLE_COLOR, VOICES_COLOR, VIDEOS_COLOR, STICKERS_COLOR],
                        user.count_messages
                        ).html

        html += '</div>'

        html += StatBlock('Длинны сообщений',
                          [
                              StatRow('Средняя',
                                      [StatText(user.count_chars / user.count_messages, lambda i: f'~{round(i)} симв.')]
                                      ),
                              StatRow('Максимальная',
                                      [StatText(user.len_longest_message, lambda i: f'{i} симв.')]
                                      ),
                              StatLongMessages(user.longest_messages)
                          ]
                          ).html

        html += '<div class="two-sides">'

        html += StatBlock('Слова',
                          [
                              StatRow('Количество',
                                      [StatDigit(user.count_words),
                                       StatPercent(user.count_words, chat.count_words)]
                                      ),
                              StatRow('Уникальных',
                                      [StatDigit(count_unique_words),
                                       StatPercent(count_unique_words, chat_count_unique_words)]
                                      )
                          ]
                          ).html

        html += StatBlock('Символы',
                          [
                              StatRow('Количество',
                                      [StatDigit(user.count_chars),
                                       StatPercent(user.count_chars, chat.count_chars)]
                                      ),
                              StatRow('Уникальных',
                                      [StatDigit(count_unique_chars),
                                       StatPercent(count_unique_chars, chat_count_unique_chars)]
                                      )
                          ]
                          ).html

        html += '</div>'

        html += WordMap('Карта <i>по количеству</i>',
                sorted(user.words_map.items(), key=lambda item: item[1], reverse=True)).html

        html += WordMap('Карта <i>по алфавиту</i>',
                sorted(user.words_map.items(), key=lambda item: item[0].lower())).html

        html += WordMap('Карта <i>букв</i>',
                        sorted(user.chars_map.items(), key=lambda item: item[1], reverse=True)).html

        html += WordMap('Карта <i>символов</i>',
                        sorted(user.punctuation_map.items(), key=lambda item: item[1], reverse=True)).html

        html += '</section>'

    html += HTML_END

    with open(f'result/{output_name}.html', 'w', encoding='utf-8') as file:
        file.write(html)
