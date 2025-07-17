from typing import List
from user import User


def parsing(data: dict):
    chat_name = data['name']
    chat_id = data['id']
    messages = data['messages']
    chat = User(chat_name, f'chat{chat_id}')
    del data, chat_name, chat_id

    users: List[User] = []

    for message in messages:
        if 'from' in message:
            name = message['from']
            uid = message['from_id']
        else:
            name = message['actor']
            uid = message['actor_id']

        user = next((u for u in users if u.uid == uid), None)

        if user is None:
            user = User(name, uid)
            users.append(user)

        user.add_message_info(message)
        chat.add_message_info(message)

    return chat, users
