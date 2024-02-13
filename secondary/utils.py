from collections import OrderedDict


class MessageHolder:
    def __init__(self):
        self.messages = OrderedDict()

    def append(self, msg_id:int, content: str) -> None:
        self.messages[msg_id] = {"id": msg_id, "content": content}

    def get_messages(self) -> list:
        return [message for message in self.messages.values()]
