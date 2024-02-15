import asyncio
from replicated_logger import logger
import os

from flask import Flask, request, make_response, jsonify

from secondary import Secondary

app = Flask(__name__)
secondary = None


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = secondary.get_messages()
    logger.info(f"{secondary} messages: {messages}")
    response = make_response(jsonify({'messages': messages}), 200)
    return response


@app.route('/add_message', methods=['POST'])
async def add_message():
    logger.info(f'Secondary request: {request.json}')
    msg_id, message = request.json['msg_id'], request.json['message']
    delay = int(os.getenv("DELAY"))
    await asyncio.sleep(delay)
    saved = secondary.add_message(msg_id, message)
    resp_body = {"summary": f"Message saved with id {msg_id}"}
    response = make_response(jsonify(resp_body), 200)
    if not saved:
        resp_body["summary"] = "Message was not saved"
        response = make_response(jsonify(resp_body), 500)
    logger.info(resp_body["summary"])
    return response


if __name__ == '__main__':
    host, port = os.getenv("HOST"), int(os.getenv("PORT", 5001))
    secondary = Secondary(host, port)
    app.run(debug=True, host=host, port=port)
