from rocketchat.api import RocketChatAPI

api = RocketChatAPI(settings={'username': 'jabir.ai', 'password': '@jabir.a!',
                              'domain': 'http://localhost:3000'})

def send_message_to_room(message,room_id):
    api.send_message(message,room_id)