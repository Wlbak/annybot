import re, requests, json, time
from telethon import events
from .. import chat_id, jdbot, logger

@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r"(\n|.)*https://u.jd.com/[a-zA-Z0-9]+"))
async def get_shoptoken(events):
    try:
        start_msg = await jdbot.send_message(chat_id, f"开始运行")
        msg_list = []
        header = {}
        header['Referer'] = 'https://shop.m.jd.com'
        url = events.message.text
        url_list = re.findall(r'https://u.jd.com/[a-zA-Z0-9]+', url)
        for url in url_list:
            #time.sleep(3)
            #await jdbot.send_message(chat_id, url)
            
            try:
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
                print(shoptoken)
            
                header = {'Referer': 'https://h5.m.jd.com', 'User-Agent': '%E5%BF%AB%E6%8D%B7%E6%8C%87%E4%BB%A4/7788.19 CFNetwork/1125.2 Darwin/19.4.0'}
            
                url = f'https://api.m.jd.com/api?appid=interCenter_shopSign&t=1662264226000&loginType=2&functionId=interact_center_shopSign_getActivityInfo&body=%7B%22token%22:%22{shoptoken}%22,%22venderId%22:%22%22%7D&jsonp=jsonp1000'
            
                resp = requests.get(url, headers=header).text
                # type1优惠券，4豆子，6积分，14红包（100=1元）
                
                resp = json.loads(re.findall('\{.*\}', resp)[0])
                startTime = time.strftime('%Y/%m/%d',time.localtime(resp['data']['startTime']/1000))
                endTime = time.strftime('%Y/%m/%d',time.localtime(resp['data']['endTime']/1000))
                ac_time = f'#时间: {startTime}-{endTime}'
                msg_list.append(ac_time)
                ac_list = resp['data']['continuePrizeRuleList']
                for i in ac_list:
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
                    msg = f'#签到{days}天,{discount}{type},共计{number}份'
                    # print(msg)
                    msg_list.append(msg)
                msg_list.append(shoptoken + '\n')
            except :
                pass
        msg1 = '\n'.join(msg_list)
        await jdbot.delete_messages(chat_id,start_msg)
        await jdbot.send_message(chat_id, msg1)
    except Exception as e:
        title = "【💥错误💥】"
        tip = '建议百度/谷歌进行查询'
        await jdbot.send_message(chat_id, f"{title}\n\n错误原因：{str(e)}\n\n{tip}")
        logger.error(f"错误--->{str(e)}")