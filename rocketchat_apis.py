from rocketchat.api import RocketChatAPI
from config import UI_URL

api = RocketChatAPI(settings={'username': 'jabir.ai', 'password': '@jabir.a!',
                              'domain': UI_URL})

def send_message_to_room(message,room_id):
    api.send_message(message,room_id)