from utils import MessageHolder

from replicated_logger import logger


class Secondary:
    def __init__(self, host, port, message_holder=MessageHolder()):
        self.host = host
        self.port = port
        self.message_holder = message_holder

    def add_message(self, msg_id: int, message: str):
        self.message_holder.append(msg_id, message)
        return True

    def get_messages(self) -> list:
        return self.message_holder.get_messages()

    def __repr__(self):
        return f"{self.host}:{self.port}"
