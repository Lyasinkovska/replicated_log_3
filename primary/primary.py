import logging
import os
import aiohttp
import asyncio

from aiohttp import ClientConnectionError

secondary_nodes = os.getenv("SECONDARY_1"), os.getenv("SECONDARY_2")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("primary.log"),
        logging.StreamHandler(),
    ],
)


class Primary:
    def __init__(self, message_holder):
        self.message_holder = message_holder
        self.message_counter = 0
        self.latch = None

    async def add_message(self, message, latch):
        self.message_counter += 1
        # self.message_holder.append(self.message_counter, message)
        self.latch = latch
        # await self.latch.count_down()
        return self.message_counter

    # @property
    # def countdown_latch(self):
    #     return self.latch
    #
    # @countdown_latch.setter
    # def countdown_latch(self, write_concern):
    #     self.latch = write_concern

    async def create_tasks(self, msg_id, message, wc):

        # logging.info(f'countdown count ----- {self.countdown_latch.count}')
        # tasks = [asyncio.create_task(self.send_message('http://primary:5000/save_message', msg_id, message))]
        tasks = [asyncio.create_task(self.save_message(msg_id, message))]

        # tasks = []
        for sec_node in secondary_nodes:
            logging.info(f'CREATING TASKS ----- {f"{sec_node}/add_message", msg_id, message}')
            tasks.append(asyncio.create_task(self.send_message(f"{sec_node}/add_message", msg_id, message)))
        await self.latch.wait()
        # acks = 0
        # logging.info(f'{wc}')
        # try:
        #     for task in asyncio.as_completed(tasks):
        #         logging.info(f'acks {acks} wc {wc} {task}')
        #         ack = await task
        #         if ack:
        #             acks += 1
        #         if acks >= wc:
        #             break
        # except asyncio.TimeoutError:
        #     print('Gave up after timeout')
        #
        # if acks >= wc:
        #     logging.info(
        #         f"Message {msg_id} replicated to {acks} secondaries, meeting write concern of {wc}."
        #     )
        #     return "Message replicated according to write concern."
        # else:
        #     logging.warning(
        #         f"Message {msg_id} did not meet write concern. Only {acks} secondaries acknowledged."
        #     )
        #     return "Write concern not met; message may not be fully replicated."

    async def save_message(self, msg_id, message):
        self.message_holder.append(msg_id, message)

        await asyncio.sleep(0.01)
        await self.latch.count_down()
        # return True

    async def send_message(self, secondary_url, msg_id, message):
        try:
            async with aiohttp.ClientSession() as session:

                async with session.post(url=secondary_url,
                                        ssl=False,
                                        json={"msg_id": msg_id,
                                              "message": message},
                                        headers={"Content-Type": "application/json"}
                                        ) as response:
                    result = await response.json()
                logging.info(f'RESULT {result} response.status  {response.status}')
                # logging.debug(f'write_concern {self.countdown_latch.count}')
                #
                if response.status == 200:
                    await self.latch.count_down()
                # return response.status == 200

        except ClientConnectionError as e:
            logging.error(e)
            return {"summary": f"{e}"}

    def get_messages(self):
        return self.message_holder.get_messages()
