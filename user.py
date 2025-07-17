from typing import List, Dict
import re
from dataclasses import dataclass, field


@dataclass()
class User:
    name: str
    uid: str

    longest_messages: List[str] = field(default_factory=list)
    len_longest_message: int = 0

    count_messages: int = 0
    count_sensible_messages: int = 0
    count_forwarded_messages: int = 0
    count_pin_messages: int = 0

    count_stickers: int = 0

    count_voices: int = 0
    duration_voices: int = 0

    count_videos: int = 0
    duration_videos: int = 0

    count_phone_call: int = 0
    duration_phone_call: int = 0

    count_words: int = 0
    count_chars: int = 0

    first_messages_timestamp: int = 0  # Unix-время
    last_messages_timestamp: int = 0   # Unix-время

    days_count_messages: Dict[str, int] = field(default_factory=dict)
    words_map: Dict[str, int] = field(default_factory=dict)
    chars_map: Dict[str, int] = field(default_factory=dict)
    punctuation_map: Dict[str, int] = field(default_factory=dict)

    @staticmethod
    def remove_non_alpha(text):
        return re.sub(r'[^a-zA-Zа-яА-ЯёЁë]', '', text)

    @staticmethod
    def remove_alpha(text):
        return re.sub(r'[a-zA-Zа-яА-ЯёЁë]', '', text)

    @staticmethod
    def remove_spaces(text):
        return re.sub(r'\s+', '', text)

    def __add_count_messages(self):
        self.count_messages += 1

    def __add_count_sensible_messages(self):
        self.count_sensible_messages += 1

    def __add_count_forwarded_messages(self):
        self.count_forwarded_messages += 1

    def __add_count_pin_messages(self):
        self.count_pin_messages += 1

    def __add_count_stickers(self):
        self.count_stickers += 1

    def __add_count_voices(self):
        self.count_voices += 1

    def __add_count_videos(self):
        self.count_videos += 1

    def __add_count_phone_call(self):
        self.count_phone_call += 1

    def __add_duration_voices(self, duration: int):
        self.duration_voices += duration

    def __add_duration_videos(self, duration: int):
        self.duration_videos += duration

    def __add_duration_phone_call(self, duration: int):
        self.duration_phone_call += duration

    def __add_count_word(self, text: str):
        words = text.split()
        self.count_words += len(words)

    def __add_count_char(self, text: str):
        self.count_chars += len(text)

    def __upd_messages_timestamps(self, time: int):
        if self.first_messages_timestamp == 0 or time < self.first_messages_timestamp:
            self.first_messages_timestamp = time

        if self.last_messages_timestamp == 0 or time > self.last_messages_timestamp:
            self.last_messages_timestamp = time

    def __upd_days_count_messages(self, day: str):
        if day in self.days_count_messages:
            self.days_count_messages[day] += 1
        else:
            self.days_count_messages[day] = 1

    def __upd_longest_message(self, text: str):
        len_text = len(text)

        if len_text > self.len_longest_message:
            self.longest_messages = [text]
            self.len_longest_message = len_text
        elif len_text == self.len_longest_message:
            self.longest_messages.append(text)

    def __upd_words_map(self, text: str):
        words = text.split()

        for word in words:
            word = word.lower()
            word = self.remove_non_alpha(word)

            if word == '':
                return

            if word in self.words_map:
                self.words_map[word] += 1
            else:
                self.words_map[word] = 1

    def __upd_chars_map(self, text: str):
        text = self.remove_spaces(text)
        text = self.remove_non_alpha(text)

        for char in text:
            if char in self.chars_map:
                self.chars_map[char] += 1
            else:
                self.chars_map[char] = 1

    def __upd_punctuation_map(self, text: str):
        text = self.remove_spaces(text)
        text = self.remove_alpha(text)

        for punct in text:
            if punct in self.punctuation_map:
                self.punctuation_map[punct] += 1
            else:
                self.punctuation_map[punct] = 1

    def add_message_info(self, message: dict):
        day = message["date"].split("T")[0]
        timestamp = int(message['date_unixtime'])
        text_entities = message['text_entities']

        text = ''
        for text_entity in text_entities:
            text += text_entity['text']

        self.__add_count_messages()
        if text != '':
            self.__add_count_sensible_messages()
        if 'forwarded_from' in message:
            self.__add_count_forwarded_messages()

        if message['type'] == 'service':
            if message['action'] == 'phone_call':
                self.__add_count_phone_call()
                if 'duration_seconds' in message:
                    self.__add_duration_phone_call(int(message['duration_seconds']))
            elif message['action'] == 'pin_message':
                self.__add_count_pin_messages()

        if 'media_type' in message:
            if message['media_type'] == 'sticker':
                self.__add_count_stickers()
            elif message['media_type'] == 'voice_message':
                self.__add_count_voices()
                self.__add_duration_voices(int(message['duration_seconds']))
            elif message['media_type'] == 'video_message':
                self.__add_count_videos()
                self.__add_duration_videos(int(message['duration_seconds']))

        self.__add_count_word(text)
        self.__add_count_char(text)

        if 'forwarded_from' not in message:
            self.__upd_longest_message(text)
        self.__upd_days_count_messages(day)
        self.__upd_messages_timestamps(timestamp)
        self.__upd_words_map(text)
        self.__upd_chars_map(text)
        self.__upd_punctuation_map(text)

