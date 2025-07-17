from config import MESSAGES_DB_PATH, OUTPUT_NAME
from analysis import parsing
from html_layout.html_output import make_html
from json import load
import time

start_time = time.time()
with open(MESSAGES_DB_PATH, 'r', encoding='utf-8') as file:
    data = load(file)
print(f'Забрал данные')

chat, users = parsing(data)
del data
print(f'Проанализировал данные. Делаю HTML')

make_html(chat=chat, users=users, output_name=OUTPUT_NAME)
print(f'Статистика по чату «{chat.name}» готова!')
print(f"Время выполнения: {time.time() - start_time:.2f} секунд")
