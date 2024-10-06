from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_cors import CORS
from rocketchat_apis import send_message_to_room
import logging
import sys
from model import *
from config import *

app = Flask(__name__)
CORS(app)

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@app.route("/", methods=['GET'])
def chat_page():
    return render_template('chat.html',ui_url = UI_URL)


@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        chat_id = data['_id']

        if data["messages"]:
            if data["messages"][0]["u"]["username"] == data["agent"]["username"]:
                pass
            else:
                if check_message_age(data["messages"][0]["ts"]):
                    resp = chat(data["messages"][0]["msg"], chat_id)
                    send_message_to_room(resp, data['_id'])

    except Exception as e:
        print(e)

    finally:
        return jsonify({"status": "success"}), 200


@app.route('/api/question', methods=['POST'])
def post_question():
    json = request.get_json(silent=True)
    question = json['question']
    user_id = json['user_id']
    logging.info("post question `%s` for user `%s`", question, user_id)
    resp = chat(question, user_id)
    data = {'answer': resp}
    return jsonify(data), 200


if __name__ == '__main__':
    init_llm()
    index = init_index(Settings.embed_model)
    init_query_engine(index)
    app.run(host='0.0.0.0', port=HTTP_PORT, debug=True)
