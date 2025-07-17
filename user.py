from typing import List, Dict
import re


class User:
    def __init__(self, name: str, uid: str):
        self.name = name
        self.uid = uid

        self.longest_messages: List[str] = []
        self.len_longest_message = 0

        self.count_messages = 0
        self.count_sensible_messages = 0
        self.count_forwarded_messages = 0
        self.count_pin_messages = 0

        self.count_stickers = 0

        self.count_voices = 0
        self.duration_voices = 0

        self.count_videos = 0
        self.duration_videos = 0

        self.count_phone_call = 0
        self.duration_phone_call = 0

        self.count_words = 0
        self.count_chars = 0

        self.first_messages_timestamp = 0  # Unix-время
        self.last_messages_timestamp = 0   # Unix-время

        self.days_count_messages: Dict[str, int] = {}
        self.words_map: Dict[str, int] = {}
        self.chars_map: Dict[str, int] = {}
        self.punctuation_map: Dict[str, int] = {}

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

