#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .. import chat_id, jdbot, client, logger, api_id, api_hash, proxystart, proxy, _ConfigDir, _ScriptsDir, _JdbotDir, _JdDir, TOKEN
from ..bot.utils import cmd, backfile, jdcmd, V4, QL, _ConfigFile, myck
from ..diy.utils import getbean, my_chat_id, rwcon
from telethon import events, TelegramClient
import re, asyncio, time, datetime, os, sys, requests, json, traceback

bot_id = int(TOKEN.split(":")[0])

@client.on(events.NewMessage(from_users=chat_id, pattern=r"^-u$"))
async def user(event):
    try:
        chat = await event.get_chat()
        await event.delete()
        # await asyncio.sleep(0.2)
        msg = await client.send_message(chat.id, "**容器YM 监控正常**")
        await asyncio.sleep(5)
        await client.delete_messages(chat.id, msg)
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=-1001550564596, pattern=r"(\n|.)*[A-Za-z0-9]{32}.*"))
async def zudui(event):
    try:
        themsg = event.message.text
        chat = await event.get_chat()
        title = chat.title
        messages = themsg.split("\n")
        messages = filter(None, messages)
        end = False
        identity = '组队瓜分'
        variable = ""
        for message in messages:
            if not re.search(r"[A-Za-z0-9]{32}", message):
                continue
            kname = "jd_task_wdz_custom"
            vname = message.replace("`", "").replace(" ", "").replace("\n", "")
            kv = f'{kname}="{vname}"'
            variable = f"export {kv}"
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
            if re.search(f'{kname}=[\'\"]{vname}[\'\"]', configs):
                await jdbot.send_message(chat_id, f"**从：{title}\n监控到（{identity}）变量已存在\n不再执行 . . .**")
                continue
            if configs.find(kname) != -1:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
                end = f"**从：{title}\n监控到（{identity}）替换变量成功**"
            elif configs.find(kname) == -1:
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find("↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 1, f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"**从：{title}\n监控到（{identity}）新增变量成功**"
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
                f3.write(configs)
        if end:
            msg = await jdbot.send_message(chat_id, f"{end}\n\n`{variable}`")
            if identity == "组队瓜分":
                await cmd("jtask /jd/scripts/jd_task_wdz.js now")
            else:
                await jdbot.edit_message(msg, f"车况不佳，导致发生严重意外!")
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=-100166309759, pattern=r'export\s(jd_task_jgyl_custom|jd_task_gzcj_custom|jd_task_lhjcj_custom|jd_task_wdz_custom|jd_task_lzzd_custom|jd_task_cjzd_custom|jd_task_glyl_custom|jd_task_qdyl_custom|jd_task_fshd_custom|jd_task_fsyl_custom|jd_task_mdsx_custom).*=(".*"|\'.*\')'))
async def activityID(event):
    try:
        text = event.message.text
        if "jd_task_jgyl_custom" in text:
            name = "加购有礼"
        elif "jd_task_gzcj_custom" in text:
            name = "关注抽奖"
        elif "jd_task_lhjcj_custom" in text:
            name = "老虎机抽奖"
        elif "jd_task_wdz_custom" in text:
            name = "微定制"
        elif "jd_task_lzzd_custom" in text:
            name = "lz组队"
        elif "jd_task_cjzd_custom" in text:
            name = "cj组队"
        elif "jd_task_glyl_custom" in text:
            name = "盖楼有礼"
        elif "jd_task_qdyl_custom" in text:
            name = "签到有礼"
        elif "jd_task_fshd_custom" in text:
            name = "粉丝互动"
        elif "jd_task_fsyl_custom" in text:
            name = "分享有礼"
        elif "jd_task_mdsx_custom" in text:
            name = "读秒手速"
        else:
            return
        msg = await jdbot.send_message(chat_id, f'【监控】 监测到`{name}` 环境变量！')
        messages = event.message.text.split("\n")
        change = ""
        for message in messages:
            if "export " not in message:
                continue
            kv = message.replace("export ", "")
            key = kv.split("=")[0]
            value = re.findall(r'"([^"]*)"', kv)[0]
            configs = rwcon("str")
            if kv in configs:
                continue
            if key in configs:
                configs = re.sub(f'{key}=("|\').*("|\')', kv, configs)
                change += f"【替换】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            else:
                if V4:
                    end_line = 0
                    configs = rwcon("list")
                    for config in configs:
                        if "第五区域" in config and "↑" in config:
                            end_line = configs.index(config) - 1
                            break
                    configs.insert(end_line, f'export {key}="{value}"\n')
                else:
                    configs = rwcon("str")
                    configs += f'export {key}="{value}"\n'
                change += f"【新增】 `{name}` 环境变量成功\n`{kv}`\n\n"
                msg = await jdbot.edit_message(msg, change)
            rwcon(configs)
        if len(change) == 0:
            await jdbot.edit_message(msg, f"【取消】 {name} 环境变量无需改动！")
            return
        try:
            if "jd_task_jgyl" in event.message.text:
                await cmd('jtask /jd/own/jd_task_jgyl.js now')
            elif "jd_task_gzcj" in event.message.text:
                await cmd('jtask /jd/own/jd_task_gzcj.js now')
            elif "jd_task_lhjcj" in event.message.text:
                await cmd('jtask /jd/own/jd_task_lhjcj.js now')
            elif "jd_task_wdz" in event.message.text:
                await cmd('jtask /jd/own/jd_task_wdz.js now')
            elif "jd_task_lzzd" in event.message.text:
                await cmd('jtask /jd/own/jd_task_lzzd.js now')
            elif "jd_task_cjzd" in event.message.text:
                await cmd('jtask /jd/own/jd_task_cjzd.js now')
            elif "jd_task_glyl" in event.message.text:
                await cmd('jtask /jd/own/jd_task_glyl.js now')
            elif "jd_task_qdyl" in event.message.text:
                await cmd('jtask /jd/own/jd_task_qdyl.js now')
            elif "jd_task_fshd" in event.message.text:
                await cmd('jtask /jd/own/jd_task_fshd.js now')
            elif "jd_task_fsyl" in event.message.text:
                await cmd('jtask /jd/own/jd_task_fsyl.js now')
            elif "jd_task_mdsx" in event.message.text:
                await cmd('jtask /jd/own/jd_task_mdsx.js now')
            else:
                await jdbot.edit_message(msg, f"看到这行字,是有严重BUG!")
        except ImportError:
            pass
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")




@client.on(events.NewMessage(chats=[-1001788479863], pattern=r"(\n|.)*export shareActivityId=[\"|\'].*[\"|\']"))
async def jian_kong(event):
    try:
        themsg = event.message.text
        chat = await event.get_chat()
        title = chat.title
        messages = themsg.split("export ")
        messages = filter(None, messages)
        end = False
        identity=''
        kv_names = ['shareActivityId',
                    'shareActivityToken',
                    'shareActivityType'
        ]
        variable = ""
        for message in messages:
            if "=" not in message:
                continue
            if "shareActivityId" in message:
                identity = "分享礼包"
            template = re.compile(r"((?:\n|.)*=[\"|\'].*[\"|\'])(\n|.*).*")
            kv = re.sub(r"\n.*", "", re.sub(template, r"\1", message)).replace("*", "").replace("\'", "\"").replace("`", "")
            kname = kv.split("=")[0]
            vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
            variable += f'{kname}="{vname}"\n'
            if kv in configs:
                continue
            if configs.find(kname) != -1 and any(kname == s for s in kv_names):
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
                end = f"**从：{title}\n监控到（{identity}）替换变量成功**"
            elif configs.find(kname) == -1 and any(kname == s for s in kv_names):
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find("↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 1, f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"**从：{title}\n监控到（{identity}）新增变量成功**"
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
                f3.write(configs)
        if end:
            msg = await jdbot.send_message(chat_id, f"{end}\n\n`{variable}`")
            if "分享礼包" == identity:
                await cmd("jtask /jd/scripts/m_jd_share.js now")
            else:
                await jdbot.edit_message(msg, f"车况不佳，导致发生严重意外!")
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")


@client.on(events.NewMessage(chats=-1001592120340, pattern=r"(\n|.)*([A-Za-z0-9]{32}|j=.+).*"))
async def wuxian(event):
    try:
        themsg = event.message.text
        chat = await event.get_chat()
        title = chat.title
        messages = themsg.split("\n")
        messages = filter(None, messages)
        end = False
        identity = ''
        variable = ""
        for message in messages:
            message = message.replace("`", "").replace(" ", "").replace("\n", "")
            if re.search(r"[A-Za-z0-9]{32}", message) and not re.search(r"(j=.+)", message):
                kname = "jd_task_wuxian_custom"
                vname = message
                identity = '无线活动'
            elif re.search(r"j=.+", message):
                kname = "jd_task_jdjoy_custom"
                vname = re.findall(r"j=[\'\"]?([^\'\"]+)[\'\"]?", message)[0]
                identity = 'jdjoy任务'
            else:
                continue
            kv = f'{kname}="{vname}"'
            variable = f"export {kv}"
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
            if re.search(f'{kname}=[\'\"]{vname}[\'\"]', configs):
                await jdbot.send_message(chat_id, f"**从：{title}\n监控到（{identity}）变量已存在\n不再执行 . . .**")
                continue
            if configs.find(kname) != -1:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
                end = f"**从：{title}\n监控到（{identity}）替换变量成功**"
            elif configs.find(kname) == -1:
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find("↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 1, f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"**从：{title}\n监控到（{identity}）新增变量成功**"
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
                f3.write(configs)
        if end:
            msg = await jdbot.send_message(chat_id, f"{end}\n\n`{variable}`")
            if identity == "无线活动":
                await cmd("jtask /jd/scripts/jd_task_wuxian.js now")
            elif identity == "jdjoy任务":
                await cmd("jtask /jd/scripts/jd_task_jdjoy.js now")
            else:
                await jdbot.edit_message(msg, f"车况不佳，导致发生严重意外!")
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")

@client.on(events.NewMessage(chats=-1001516831231, pattern=r"(\n|.)*[A-Za-z0-9]{32}.*"))
async def wuxian(event):
    try:
        themsg = event.message.text
        chat = await event.get_chat()
        title = chat.title
        messages = themsg.split("\n")
        messages = filter(None, messages)
        end = False
        identity = 'QITOQITO'
        variable = ""
        for message in messages:
            if not re.search(r"[A-Za-z0-9]{32}", message):
                continue
            kname = "QITOQITO"
            vname = message.replace("`", "").replace(" ", "").replace("\n", "")
            kv = f'{kname}="{vname}"'
            variable = f"export {kv}"
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
            if re.search(f'{kname}=[\'\"]{vname}[\'\"]', configs):
                await jdbot.send_message(chat_id, f"**从：{title}\n监控到（{identity}）变量已存在\n不再执行 . . .**")
                continue
            if configs.find(kname) != -1:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
                end = f"**从：{title}\n监控到（{identity}）替换变量成功**"
            elif configs.find(kname) == -1:
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find("↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 1, f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"**从：{title}\n监控到（{identity}）新增变量成功**"
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
                f3.write(configs)
        if end:
            msg = await jdbot.send_message(chat_id, f"{end}\n\n`{variable}`")
            if identity == "QITOQITO":
                await jdbot.edit_message(msg, '更新成功啦')
            else:
                await jdbot.edit_message(msg, f"车况不佳，导致发生严重意外!")
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")

@client.on(events.NewMessage(chats=-100153333418, pattern=r"(\n|.)*([A-Za-z0-9]{32}|j=.+).*"))
async def wuxian(event):
    try:
        themsg = event.message.text
        chat = await event.get_chat()
        title = chat.title
        messages = themsg.split("\n")
        messages = filter(None, messages)
        end = False
        identity = ''
        variable = ""
        for message in messages:
            message = message.replace("`", "").replace(" ", "").replace("\n", "")
            if re.search(r"[A-Za-z0-9]{32}", message) and not re.search(r"(j=.+)", message):
                kname = "jd_task_wuxian_custom"
                vname = message
                identity = '无线活动'
            elif re.search(r"j=.+", message):
                kname = "jd_task_jdjoy_custom"
                vname = re.findall(r"j=[\'\"]?([^\'\"]+)[\'\"]?", message)[0]
                identity = 'jdjoy任务'
            else:
                continue
            kv = f'{kname}="{vname}"'
            variable = f"export {kv}"
            with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
                configs = f1.read()
            if re.search(f'{kname}=[\'\"]{vname}[\'\"]', configs):
                await jdbot.send_message(chat_id, f"**从：{title}\n监控到（{identity}）变量已存在\n不再执行 . . .**")
                continue
            if configs.find(kname) != -1:
                configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
                end = f"**从：{title}\n监控到（{identity}）替换变量成功**"
            elif configs.find(kname) == -1:
                if V4:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.readlines()
                    for config in configs:
                        if config.find("第五区域") != -1 and config.find("↑") != -1:
                            end_line = configs.index(config)
                            break
                    configs.insert(end_line - 1, f'export {kname}="{vname}"\n')
                    configs = ''.join(configs)
                else:
                    with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
                        configs = f2.read()
                    configs += f'export {kname}="{vname}"\n'
                end = f"**从：{title}\n监控到（{identity}）新增变量成功**"
            with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
                f3.write(configs)
        if end:
            msg = await jdbot.send_message(chat_id, f"{end}\n\n`{variable}`")
            if identity == "无线活动":
                await cmd("jtask /jd/scripts/jd_task_wuxian.js now")
            elif identity == "jdjoy任务":
                await cmd("jtask /jd/scripts/jd_task_jdjoy.js now")
            else:
                await jdbot.edit_message(msg, f"车况不佳，导致发生严重意外!")
    except Exception as e:
        title = "★错误★"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + e.__traceback__.tb_frame.f_code.co_name
        details = "错误详情：第 " + str(e.__traceback__.tb_lineno) + " 行"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n{details}\n{traceback.format_exc()}\n{tip}")
        logger.error(f"错误--->{str(e)}")
        

@client.on(events.NewMessage(chats=-1001675809610, pattern=r'(\n|.)*https://u.jd.com/[a-zA-Z0-9]+'))
async def get_shoptoken(events):
    try:
        await client.send_message(-1001675809610, f"开始运行")
        msg_list = []
        header = {}
        header['Referer'] = 'https://shop.m.jd.com'
        url = events.message.text
        await client.send_message(-1001675809610, url)
        url_list = re.findall(r'https://u.jd.com/[a-zA-Z0-9]+', url)
        for url in url_list:
            html = re.findall("'https://u.jd.com.*?'", requests.get(url).text)[0].replace("'", "")
            resp = requests.get(html, headers=header).url
            gx = re.findall('(?<=gx=).*?(?=&)', resp)[0]
            shopId = re.findall('(?<=shopId=)\w+', resp)[0]
            utm_term = re.findall('(?<=utm_term=)\w+', resp)[0]
            body = '{' + f'"ad_od":"share","cu":"true","gx":"{gx}","rid":"12432","shopId":"{shopId}","utm_campaign":"t_1001871922_","utm_medium":"jingfen","utm_source":"kong","utm_term":"{utm_term}","utm_user":"plusmember","source":"m-shop"' + '}'

            url = f'https://api.m.jd.com/client.action?functionId=whx_getShopHomeActivityInfo&t=1662134109133&appid=shop_view&clientVersion=11.0.0&client=wh5&area=1_72_2799_0&uuid=16575557460081799873293&body={body}'
    
            resp = json.loads(requests.get(url, headers=header).text)
            # print(resp)
            shoptoken = resp['result']['signStatus']['isvUrl'].split('=')[1]
            # print(shoptoken)
    
            header = {'Referer': 'https://h5.m.jd.com', 'User-Agent': '%E5%BF%AB%E6%8D%B7%E6%8C%87%E4%BB%A4/7788.19 CFNetwork/1125.2 Darwin/19.4.0'}
    
            url = f'https://api.m.jd.com/api?appid=interCenter_shopSign&t=1662264226000&loginType=2&functionId=interact_center_shopSign_getActivityInfo&body=%7B%22token%22:%22{shoptoken}%22,%22venderId%22:%22%22%7D&jsonp=jsonp1000'
    
            resp = requests.get(url, headers=header).text
            # type1优惠券，4豆子，6积分，14红包（100=1元）
    
            resp = json.loads(re.findall('\{.*\}', resp)[0])
            ac_list = resp['data']['continuePrizeRuleList']
    
            for i in ac_list:
    
                level = i['level']
                days = i['days']
                discount = int(i['prizeList'][0]['discount'])
                number = i['prizeList'][0]['number']
                type = int(i['prizeList'][0]['type'])
                if type == 1:
                    type = '优惠券'
                elif type == 4:
                    type = '金豆'
                elif type == 6:
                    type = '积分'
                elif type == 14:
                    type = '红包'
                    discount = discount / 100
                else:
                    type = '未知'
                msg = f'#level:{level},签到{days}天,{discount}{type},共计{number}份'
                # print(msg)
                msg_list.append(msg)
            msg_list.append(shoptoken)
        msg1 = '\n'.join(msg_list)
        await client.send_message(-1001675809610, msg1)
    except Exception as e:
        title = "【💥错误💥】"
        name = "文件名：" + os.path.split(__file__)[-1].split(".")[0]
        function = "函数名：" + sys._getframe().f_code.co_name
        tip = '建议百度/谷歌进行查询'
        await client.send_message(-1001675809610, f"{title}\n\n{name}\n{function}\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")
        
        
        
        
        
        
        
        
        
        