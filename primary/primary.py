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
        logging.FileHandler("primaty.log"),
        logging.StreamHandler(),
    ],
)


class Primary:
    def __init__(self, message_holder):
        self.message_holder = message_holder
        self.message_counter = 0

    def add_message(self, message):
        self.message_counter = self.message_counter + 1
        self.message_holder.append(self.message_counter, message)
        logging.info(f"Secondary nodes: {secondary_nodes}")
        for sec_node in secondary_nodes:
            asyncio.run(self.send_message(sec_node, message))
        return self.message_counter

    async def send_message(self, secondary_url, message):
        secondary_url = f"{secondary_url}/add_message"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=secondary_url,
                                        ssl=False,
                                        json={"msg_id": self.message_counter,
                                              "message": message},
                                        headers={"Content-Type": "application/json"}
                                        ) as resp:
                    result = await resp.json()
                    return result
        except ClientConnectionError as e:
            logging.error(e)
            return {"summary": f"{e}"}

    def get_messages(self):
        return self.message_holder.get_messages()
