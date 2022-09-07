
import httpx


## httpx 的请求方式 method 入参需要大写字母, 如 "GET" "POST" "HEAD"
## httpx 重定向属性为 follow_redirects, 默认是False, 非特殊需求一般默认False
async def getRequest(method, url, data=None, headers=None, params=None, json=None, allow_redirects=False, timeout=30):
    try:
        async with httpx.AsyncClient(verify=False, follow_redirects=allow_redirects) as client:
            res = await client.request(method, url=url, data=data, headers=headers, params=params, json=json, timeout=timeout)
    except:
        res = False
    return res
