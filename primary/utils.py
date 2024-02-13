import asyncio
import logging
from asyncio import Condition
from collections import OrderedDict

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("primary.log"),
        logging.StreamHandler(),
    ],
)


class MessageHolder:
    def __init__(self):
        self.messages = OrderedDict()

    def append(self, msg_id, content):
        self.messages[msg_id] = {"id": msg_id, "content": content}
        # await asyncio.sleep(5)

    def get_messages(self):
        return [message for message in self.messages.values()]


class CountDownLatch:
    def __init__(self, count=1):
        self.count = count
        self.lock = Condition()

    async def count_down(self):
        await self.lock.acquire()
        # if self.count == 0:
        #     self.lock.release()
        #     return
        logging.info(f'1 before count_down {self.count}')
        self.count -= 1
        logging.info(f'2 after count_down {self.count}')
        if self.count <= 0:
            logging.info(f'3 self.count count_down {self.count}')
            self.lock.notify_all()
        self.lock.release()

    async def wait(self):
        logging.debug(f'in wait {self.count}')
        await self.lock.acquire()
        while self.count > 0:
            # self.lock.release()
            # return
            # while self.count > 0:
            #     logging.info(f'self.count wait {self.count}')
            await self.lock.wait()
        self.lock.release()
