import logging
import os

from utils import MessageHolder

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("secondary.log"),
        logging.StreamHandler(),
    ],
)

primary_node = os.getenv("PRIMARY")


class Secondary:
    def __init__(self, host, port, message_holder=MessageHolder()):
        self.host = host
        self.port = port
        self.message_holder = message_holder

    def add_message(self, msg_id, message):
        self.message_holder.append(msg_id, message)
        return True

    def get_messages(self):
        return self.message_holder.get_messages()

    def __repr__(self):
        return f"{self.host}:{self.port}"
