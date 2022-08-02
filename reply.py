import os
import asyncio
import botpy

from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message

# get appid & token
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    def on_ready(self):
        print("Bot is ready")       
        # _log.info(f"robot 「{self.robot.name}」 on_ready!")
    
    # async def on_at_message_create(self, message: Message):
    #     _log.info(message.author.avatar)
    #     if "sleep" in message.content:
    #         await asyncio.sleep(10)
    #     _log.info(message.author.username)
    #     await message.reply(content=f"机器人{self.robot.name}收到你的@消息了: {message.content}")


# main program
if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    mybot = MyClient(intents=intents)
    mybot.run(appid=test_config["appid"], token=test_config["token"])
