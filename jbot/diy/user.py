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


@client.on(events.NewMessage(chats=-100163665271, pattern=r"(\n|.)*[A-Za-z0-9]{32}.*"))
async def wuxian(event):
    try:
        themsg = event.message.text
        chat = await event.get_chat()
        title = chat.title
        messages = themsg.split("\n")
        messages = filter(None, messages)
        end = False
        identity = '无线活动'
        variable = ""
        for message in messages:
            if not re.search(r"[A-Za-z0-9]{32}", message):
                continue
            kname = "jd_task_wuxian_custom"
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
            if identity == "无线活动":
                await cmd("jtask /jd/scripts/jd_task_wuxin.js now")
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


@client.on(events.NewMessage(chats=-1001578578897, pattern=r'export\s(computer_activityIdList|jd_mhurlList|jd_nzmhurl|M_WX_ADD_CART_URL|M_FOLLOW_SHOP_ARGV|M_WX_SHOP_GIFT_URL|M_FAV_SHOP_ARGV|jd_cjhy_activityId|jd_zdjr_activityId|welfare|M_WX_ADD_CART_URL).*=(".*"|\'.*\')'))
async def activityID(event):
    try:
        text = event.message.text
        if "computer_activityIdListL" in text:
            name = "电脑配件"
        elif "WXGAME_ACT_ID" in text:
            name = "打豆豆"
        elif "jd_mhurlList" in text:
            name = "盲盒抽京豆"
        elif "jd_nzmhurl" in text:
            name = "女装盲盒抽京豆"
        elif "M_GYG_SHOP_ARGV" in text:
            name = "M店铺刮奖"
        elif "M_WX_ADD_CART_URL" in text:
            name = "M加购有礼"
        elif "M_WX_FOLLOW_DRAW_URL" in text:
            name = "M关注抽奖"
        elif "M_WX_LUCK_DRAW_URL" in text:
            name = "M幸运抽奖"
        elif "M_WX_SHOP_GIFT_URL" in text:
            name = "Mwx关注有礼"
        elif "M_FOLLOW_SHOP_ARGV" in text:
            name = "M店铺关注有礼"
        elif "M_FAV_SHOP_ARGV" in text:
            name = "M收藏有礼"
        elif "jd_cjhy_activityId" in text:
            name = "cj组队瓜分"
        elif "jd_zdjr_activityId" in text:
            name = "lz组队瓜分"
        elif "SHARE_ACTIVITY_ID" in text:
            name = "分享有礼"
        elif "welfare" in text:
            name = "联合关注+加购+分享领豆"
        elif "M_WX_LUCK_DRAW_URL" in text:
            name = "M幸运抽奖"
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
            if "computer_activityIdListL" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_computer.js now')
            elif "WXGAME_ACT_ID" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_dadoudou.js now')
            elif "jd_mhurlList" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_fav_shop_gift.js now')
            elif "jd_nzmhurl" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_nzmh.js now')
            elif "M_GYG_SHOP_ARGV" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_shop_gyg.js now')
            elif "M_WX_ADD_CART_URL" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_wx_addCart.js now')
            elif "M_WX_FOLLOW_DRAW_URL" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_wx_followDraw.js now')
            elif "M_WX_LUCK_DRAW_URL" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_wx_luckDraw.js now')
            elif "M_WX_SHOP_GIFT_URL" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_wx_shopGift.js now')
            elif "M_FOLLOW_SHOP_ARGV" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_follow_shop.js now')
            elif "M_FAV_SHOP_ARGV" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_fav_shop_gift.js now')
            elif "jd_cjhy_activityId" in event.message.text:
                await cmd('jtask /jd/scripts/jd_cjzdgf.js now')
            elif "jd_zdjr_activityId" in event.message.text:
                await cmd('jtask /jd/scripts/jd_zdjr.js now')
            elif "SHARE_ACTIVITY_ID" in event.message.text:
                await cmd('jtask /jd/scripts/g_jd_share.js now')
            elif "welfare" in event.message.text:
                await cmd('jtask /jd/scripts/fav_and_addcart.js now')
            elif "M_WX_LUCK_DRAW_URL" in event.message.text:
                await cmd('jtask /jd/scripts/m_jd_wx_luckDraw.js now')
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




@client.on(events.NewMessage(chats=[-1001578578897], pattern=r"(\n|.)*export shareActivityId=[\"|\'].*[\"|\']"))
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


        