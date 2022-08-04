import os
import re
import asyncio
import botpy
import requests
import json

from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message

# get appid & token
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        # print("Bot is ready")
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    # member message fetch
    async def on_message_create(self, message: Message):
        # _log.info(message.author.avatar)
        msg = message.content
        member = message.member

        _log.info(msg)

        # 处理消息，去除符号
        msg_remove = re.sub(r"(<.*?>)", "", msg)
        msg_remove = re.sub(r"((&lt;)|(&gt;))+?","",msg_remove)
        msg_remove = re.sub(r"[\s,\.\?\"\':;!，。？！：；（）\(\)\[\]“”‘’]+?","",msg_remove)
        # params = {"text": msg}
        # response = requests.post(request_url, data=params, headers=headers)
        # if response:
        #     resp = response.json()
        #     if resp['conclusionType'] == 2:
        #         data_list = resp['data']
        #         text_msg=""
        #         for data in data_list:
        #             text_msg = text_msg+'、'+data['msg']
        #         await message.reply(content=f"您的消息：“{msg}”\n{text_msg[1:]}")
        #     else:
        #         await message.reply(content=f"您的消息：“{msg}”")
        _log.info(msg_remove)
        length = len(msg_remove)
        if "4" in member.roles:
            _log.info("频道主信息")
            await message.reply(content=f"频道主您好！\n您的消息：“{msg}”\n字符串长度：{length}")
            return 0
        elif "2" in member.roles:
            _log.info("管理员信息")
            await message.reply(content=f"管理员您好！\n您的消息：“{msg}”\n字符串长度：{length}")
            return 0
        elif "5" in member.roles:
            _log.info("子管理员信息")
            await message.reply(content=f"子管理员您好！\n您的消息：“{msg}”\n字符串长度：{length}")
            return 0


# main program
if __name__ == "__main__":
    # text detector API
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
    baidu_client_id = test_config["baiduapi"]
    baidu_client_secret = test_config["baidusecret"]
    host = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={baidu_client_id}&client_secret={baidu_client_secret}"
    answer = requests.get(host)
    if answer:
        access_token = answer.json()['access_token']
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}

    # bot
    intents = botpy.Intents(public_guild_messages=True, guild_messages=True)
    mybot = MyClient(intents=intents)
    mybot.run(appid=test_config["appid"], token=test_config["token"])
