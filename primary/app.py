import os
from flask import Flask, request, make_response, jsonify
from primary import Primary
from utils import MessageHolder, CountDownLatch
from replicated_logger import logger

app = Flask(__name__)
message_holder = MessageHolder()
host, port = os.getenv("HOST"), int(os.getenv("PORT", 5000))
primary = Primary(host, port, message_holder=message_holder)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = primary.get_messages()
    logger.info(f"Primary node messages: {messages}")
    return make_response(jsonify({'messages': messages}), 200)


@app.route('/add_message', methods=['POST'])
async def add_message():
    message, write_concern = request.json['message'], request.json['write_concern']
    latch = CountDownLatch(write_concern)
    msg_id = primary.get_id(latch)
    await primary.save_and_replicate_messages(msg_id, message)
    resp_body = {"summary": f"Message saved with id {msg_id}"}
    if not msg_id:
        resp_body["summary"] = "Message was not saved"
    logger.info(resp_body["summary"])
    return make_response(jsonify(resp_body), 200)


if __name__ == '__main__':
    app.run(debug=True, host=os.getenv("HOST"), port=int(os.getenv("PORT", 5000)))
