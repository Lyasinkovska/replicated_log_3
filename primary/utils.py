from asyncio import Condition
from collections import OrderedDict
from replicated_logger import logger


class MessageHolder:
    def __init__(self):
        self.messages = OrderedDict()
        self.message_counter = 0

    def append(self, msg_id: int, content: str):
        self.messages[msg_id] = {"id": msg_id, "content": content}
        logger.info(f'Message saved: {msg_id}:{self.messages[msg_id]}')

    def get_messages(self) -> list:
        return [message for message in self.messages.values()]

    def generate_id(self) -> int:
        self.message_counter += 1
        return self.message_counter


class CountDownLatch:
    def __init__(self, count=1):
        self.count = count
        self.condition = Condition()

    async def count_down(self):
        await self.condition.acquire()
        self.count -= 1
        if self.count <= 0:
            self.condition.notify_all()
        self.condition.release()

    async def wait(self):
        await self.condition.acquire()
        while self.count > 0:
            await self.condition.wait()
        self.condition.release()
