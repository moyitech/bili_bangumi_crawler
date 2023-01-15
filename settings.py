# -*- coding = utf-8 -*-
# @Time: 2023/01/14
# @Author:MoyiTech
# @Software: PyCharm
headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 '
                  'Safari/537.36 Edg/108.0.1462.54',
}

ignore_words = [
    '的',
    '了',
    '和',
    '在',
    '我',
    '是',
    '就',
    '你',
    '他',
    '吗',
    '吧',
    '这',
    '有',
    '不',
    '给',
    '也',
    '都',
    '看',
    '还',
    '对',
    '说',
    '很',
    '能',
    '人',
    '但',
    '不是',
    '把',
    '被',
    '做',
    '但是'
]
comment_sample = 5000
word_sample = 5000
media_id = 4315402
refresh_time = 600  # 单位:秒
http_host = '0.0.0.0'
http_port = 5005
