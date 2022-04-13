#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import traceback
import asyncio
from telethon import events

from .. import chat_id, jdbot, logger


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/jc$'))
async def cxjc(event):
    try:
        msg = await jdbot.send_message(chat_id, "开始查询进程...")
        cmd = "ps -ef"
        f = os.popen(cmd)
        txt = f.readlines()
        strReturn = ""
        if txt:
            for line in txt:
                if "timeout" in line:
                    continue
                if "/ql/build" in line:
                    continue
                if "backend" in line:
                    continue
                if "node" in line and ".js" in line:
                    pid = line.split()[0].ljust(10, ' ')
                    pid_name = line.split()[4]
                    res = "/kill"+pid+'文件名: '+pid_name+'\n'
                    strReturn = strReturn+res
                if "python3" in line and ".py" in line:
                    pid = line.split()[0].ljust(10, ' ')
                    pid_name = line.split()[4]
                    res = "/kill"+pid+'文件名: '+pid_name+'\n'
                    strReturn = strReturn+res
            await jdbot.delete_messages(chat_id, msg)
            if strReturn:
                await jdbot.send_message(chat_id, strReturn)
            else:
                await jdbot.send_message(chat_id, '当前系统未执行任何脚本')
        else:
            await jdbot.delete_messages(chat_id, msg)
            await jdbot.send_message(chat_id, '当前系统未执行任何脚本')

    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'(/kill)'))
async def pidkill(event):
    try:
        messages = event.raw_text.split("\n")
        for message in messages:
            if "kill" not in message:
                continue

            isdokill = 0
            killpid = message.replace("/kill", "")

            # 先检查是否存在该进程
            cmd = "ps -ef"
            f = os.popen(cmd)
            txt = f.readlines()
            if txt:
                for line in txt:
                    if "timeout" in line:
                        continue
                    if "/ql/build" in line:
                        continue
                    if "backend" in line:
                        continue
                    if "node" in line:
                        pid = line.split()[0]
                        if killpid == pid:
                            isdokill = 1
                            break
            else:
                await jdbot.send_message(chat_id, '当前系统未执行任何脚本')

            if isdokill == 0:
                await jdbot.send_message(chat_id, '进程结束失败: 当前系统未查询到该pid '+killpid)
                return

            # 存在进程则发起结束进程命令
            cmd = "kill "+killpid
            os.system(cmd)
            await asyncio.sleep(1)
            # 再次查询该id是否存在确认已经正常结束进程
            isdokill = 0
            cmd = "ps -ef"
            f = os.popen(cmd)
            txt = f.readlines()
            if txt:
                for line in txt:
                    if "timeout" in line:
                        continue
                    if "/ql/build" in line:
                        continue
                    if "backend" in line:
                        continue
                    if "node" in line:
                        pid = line.split()[0]
                        if killpid == pid:
                            isdokill = 1
                            break
            if isdokill == 0:
                await jdbot.send_message(chat_id, '进程'+killpid+'已被强制结束!')
            else:
                await jdbot.send_message(chat_id, '进程'+killpid+'强制结束失败!')

    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
