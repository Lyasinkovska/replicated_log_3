import asyncio
import os
import time
from threading import Condition

from flask import Flask, request, make_response, jsonify

from secondary import Secondary
# Condition

app = Flask(__name__)
secondary = None


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = secondary.get_messages()
    app.logger.info(f"{secondary} messages: {messages}")
    response = make_response(jsonify({'messages': messages}), 200)
    return response


@app.route('/add_message', methods=['POST'])
async def add_message():
    app.logger.info(f'secondary request: {request.json}')
    msg_id, message = request.json['msg_id'], request.json['message']
    delay = int(os.getenv("DELAY"))
    await asyncio.sleep(delay)
    saved = secondary.add_message(msg_id, message)
    resp_body = {"summary": f"Message saved with id {msg_id}"}
    if not saved:
        resp_body["summary"] = "Message was not saved"
    app.logger.info(resp_body["summary"])
    response = make_response(jsonify(resp_body), 200)
    return response


if __name__ == '__main__':
    secondary = Secondary('localhost', 5001)
    app.run(debug=True, host='0.0.0.0', port=5001)
