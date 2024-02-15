import os
import aiohttp
import asyncio

from aiohttp import ClientConnectionError

from replicated_logger import logger

secondary_nodes = os.getenv("SECONDARY_1"), os.getenv("SECONDARY_2")


class Primary:
    def __init__(self, host, port, message_holder):
        self.host = host
        self.port = port
        self.message_holder = message_holder
        self._latch = None

    def get_id(self, latch):
        self.latch = latch
        return self.message_holder.generate_id()

    @property
    def latch(self):
        return self._latch

    @latch.setter
    def latch(self, new_latch):
        self._latch = new_latch

    async def save_and_replicate_messages(self, msg_id, message):
        tasks = [asyncio.create_task(self.save_message(msg_id, message))]
        for sec_node in secondary_nodes:
            tasks.append(asyncio.create_task(self.send_message(f"{sec_node}/add_message", msg_id, message)))
        await self.latch.wait()

    async def save_message(self, msg_id, message):
        logger.info('Successfully save_messages')
        self.message_holder.append(msg_id, message)
        await asyncio.sleep(0.01)
        await self.latch.count_down()

    async def send_message(self, secondary_url, msg_id, message):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=secondary_url,
                                        ssl=False,
                                        json={"msg_id": msg_id,
                                              "message": message},
                                        headers={"Content-Type": "application/json"},
                                        ) as response:
                    result = await response.json()
                logger.info(f'RESULT {result} response.status  {response.status}')

                if response.status == 200:
                    await self.latch.count_down()
        except ClientConnectionError as e:
            logger.error(e)
            return {"summary": f"{e}"}

    def get_messages(self):
        return self.message_holder.get_messages()

    def __repr__(self):
        return f"{self.host}:{self.port}"
