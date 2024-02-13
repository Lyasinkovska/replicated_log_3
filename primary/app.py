import asyncio
import logging

from flask import Flask, request, make_response, jsonify

from primary import Primary
from utils import MessageHolder, CountDownLatch

app = Flask(__name__)
message_holder = MessageHolder()
primary = Primary(message_holder)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = primary.get_messages()
    app.logger.info(f"Primary node messages: {messages}")
    return make_response(jsonify({'messages': messages}), 200)


@app.route('/add_message', methods=['POST'])
async def add_message():
    message, write_concern = request.json['message'], request.json['write_concern']
    latch = CountDownLatch(write_concern)
    msg_id = await primary.add_message(message, latch=latch)
    # await primary.save_message(msg_id, message)
    await primary.create_tasks(msg_id, message, write_concern)
    resp_body = {"summary": f"Message saved with id {msg_id}"}
    if not msg_id:
        resp_body["summary"] = ("Message was not save"
                                "d")
    app.logger.info(resp_body["summary"])
    return make_response(jsonify(resp_body), 200)


# @app.route('/save_message', methods=['POST'])
# async def save_message():
#     app.logger.info(f'secondary request: {request.json}')
#     msg_id, message = request.json['msg_id'], request.json['message']
#     primary.message_holder.append(msg_id, message)
#     resp_body = {"summary": f"Message saved with id {msg_id}"}
#     app.logger.info(resp_body["summary"])
#     response = make_response(jsonify(resp_body), 200)
#     return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
