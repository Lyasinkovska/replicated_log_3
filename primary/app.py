from flask import Flask, request, make_response, jsonify

from primary import Primary
from utils import MessageHolder

app = Flask(__name__)
message_holder = MessageHolder()
primary = Primary(message_holder)


@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = primary.get_messages()
    app.logger.info(f"Primary node messages: {messages}")
    response = make_response(jsonify({'messages': messages}), 200)
    return response


@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.json['message']
    msg_id = primary.add_message(message)
    resp_body = {"summary": f"Message saved with id {msg_id}"}
    if not msg_id:
        resp_body["summary"] = "Message was not saved"
    app.logger.info(resp_body["summary"])
    response = make_response(jsonify(resp_body), 200)
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
