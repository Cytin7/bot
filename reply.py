import os
import re
import asyncio
from types import NoneType
import botpy
import requests
import json

from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message

# get appid & token
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class BaiduClient(botpy.Client):
    async def on_ready(self):
        # print("Bot is ready")
        _log.info(f"机器人「{self.robot.name}」正在运行中")

    # member message fetch
    async def on_message_create(self, message: Message):
        # _log.info(message.author.avatar)
        msg = message.content
        member = message.member
        _log.info(msg)

        # 角色处理
        if member.roles == NoneType:
            pass
        elif "4" in member.roles:
            # 不处理频道主消息
            return 0
        elif "2" in member.roles:
            # 不处理管理员消息
            return 0
        elif "5" in member.roles:
            # 不处理子管理员消息
            return 0

        # 处理消息，去除符号
        msg_remove_at = re.sub(r'<[^>]+>', "", msg)  # 去除@信息
        msg_remove = re.sub(r"[\s\w，。《》？【】！“”‘’：；,\./?!@#$%^&*\(\)\\]+", "", msg_remove_at)
        msg_remove = re.sub(r"((&lt;)|(&gt;))+", "", msg_remove)
        msg_no_ascii = re.sub(r"[\s\w]+", "", msg_remove_at)

        _log.info(msg_remove)
        length = len(msg_remove)
        for taboo in taboo_list:
            if taboo in msg_no_ascii:
                short_msg = msg if len(msg)<=14 else msg[0:7]+"…"+msg[-7:]
                await message.reply(content=f"您的消息：\n「{short_msg}」\n包含违禁词，请注意语言文明。\n如有误判，请联系频道子管理")
                return 0
        if length <= 10:
            # 不处理10个字以内的消息
            return 0

        # 百度审核内容
        params = {"text": msg}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            resp = response.json()
            if resp['conclusionType'] == 2:
                data_list = resp['data']
                text_msg = ""
                for data in data_list:
                    text_msg = text_msg+'、'+data['msg']
                short_msg = msg if len(msg)<=12 else msg[0:7]+"…"+msg[-7:]
                await message.reply(content=f"您的消息：\n「{short_msg}」\n被检测出违禁成分，请注意语言文明。\n提示信息：{text_msg[1:]}\n如有误判，请联系频道子管理。")
            else:
                await message.reply(content=f"您的消息：\n「{msg}」\n没有问题。")

class nonBaiduClient(botpy.Client):
    async def on_ready(self):
        # print("Bot is ready")
        _log.info(f"机器人「{self.robot.name}」正在运行中")

    # member message fetch
    async def on_message_create(self, message: Message):
        # _log.info(message.author.avatar)
        msg = message.content
        member = message.member
        _log.info(msg)

        # 角色处理
        if member.roles == NoneType:
            pass
        elif "4" in member.roles:
            # 不处理频道主消息
            return 0
        elif "2" in member.roles:
            # 不处理管理员消息
            return 0
        elif "5" in member.roles:
            # 不处理子管理员消息
            return 0

        # 处理消息，去除符号
        msg_remove_at = re.sub(r'<[^>]+>', "", msg)  # 去除@信息
        msg_remove = re.sub(r"[\s\w，。《》？【】！“”‘’：；,\./?!@#$%^&*\(\)\\]+", "", msg_remove_at)
        msg_remove = re.sub(r"((&lt;)|(&gt;))+", "", msg_remove)
        msg_no_ascii = re.sub(r"[\s\w]+", "", msg_remove_at)

        _log.info(msg_remove)
        length = len(msg_remove)
        for taboo in taboo_list:
            if taboo in msg_no_ascii:
                short_msg = msg if len(msg)<=14 else msg[0:7]+"…"+msg[-7:]
                await message.reply(content=f"您的消息：\n「{short_msg}」\n包含违禁词，请注意语言文明。\n如有误判，请联系频道子管理")
                return 0


# main program
if __name__ == "__main__":
    # 获取违禁词列表
    taboo_path = os.path.join(os.path.dirname(__file__), "taboo.txt")
    taboo_file = open(taboo_path, 'r', encoding='utf-8')
    taboo_list = taboo_file.read().splitlines()
    # 获取百度NLP工具的API接口token
    baidu_client_id = test_config["baiduapi"]
    baidu_client_secret = test_config["baidusecret"]
    host = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={baidu_client_id}&client_secret={baidu_client_secret}"
    answer = requests.get(host)
    if answer:
        # 设置百度NLP工具的request格式
        use_baidu = True
        access_token = answer.json()['access_token']
        request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        # 机器人主体程序
        intents = botpy.Intents(
            public_guild_messages=True, guild_messages=True)
        mybot = BaiduClient(intents=intents)
        mybot.run(appid=test_config["appid"], token=test_config["token"])
    else:
        # 机器人主体程序
        intents = botpy.Intents(
            public_guild_messages=True, guild_messages=True)
        mybot = nonBaiduClient(intents=intents)
        mybot.run(appid=test_config["appid"], token=test_config["token"])
