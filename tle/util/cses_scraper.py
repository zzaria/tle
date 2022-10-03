import logging

import aiohttp
from lxml import html


class CSESError(Exception):
    pass


session = aiohttp.ClientSession()

cookies = {
    'PHPSESSID': 'a8bf92047389d7f208a5ddf410fc4711fb04e7ea',
}
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^92^\\^, ^\\^',
    'sec-ch-ua-mobile': '?1',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://cses.fi/login',
    'Accept-Language': 'en-US,en;q=0.9',
}


async def _fetch(url):
    async with session.get(url,headers=headers,cookies=cookies) as response:
        if response.status != 200:
            raise CSESError(f"Bad response from CSES, status code {response.status}")
        tree = html.fromstring(await response.read())
    return tree


async def get_problems():
    tree = await _fetch('https://cses.fi/problemset/list/')
    links = [li.get('href') for li in tree.xpath('//*[@class="task"]/a')]
    ids = sorted(int(x.split('/')[-1]) for x in links)
    return ids


async def get_problem_leaderboard(num):
    tree = await _fetch(f'https://cses.fi/problemset/stats/{num}/')
    fastest_table, shortest_table = tree.xpath(
        '//table[@class!="summary-table" and @class!="bot-killer"]')

    fastest = [a.text for a in fastest_table.xpath('.//a')]
    shortest = [a.text for a in shortest_table.xpath('.//a')]
    return fastest, shortest
