import os
import pickle
import random
import threading
import time

import jieba
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.image import imread
from wordcloud import WordCloud
from datetime import datetime

from get_rank_api import GetRankApi
from settings import ignore_words, comment_sample, word_sample, media_id

my_data = {}
last_time = '2023/01/15-15:19'


def add_data(data: dict, li: list, ):
    for i in li:
        rank = i['score']
        if rank not in data['score']:
            data['score'][rank] = 0
        data['score'][rank] += 1
        data['content'].append(i['content'])


def get_rank_task(comment_type: str):
    data = {
        'score': {},
        'content': []
    }
    count = 0
    session = GetRankApi(comment_type, media_id=media_id)
    start = time.time()
    while True:
        li, total, next_cur = session.get_rank()
        t = threading.Thread(target=add_data, args=(data, li))
        t.start()
        count += len(li)
        print(f'{comment_type}: {count}/{total}')
        if next_cur == 0:
            break
    end = time.time()
    print(f'{comment_type}用时{end - start}')
    global my_data
    my_data[comment_type] = data


def run_get():
    t1 = threading.Thread(target=get_rank_task, args=('long',))
    t2 = threading.Thread(target=get_rank_task, args=('short',))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    with open('data.pkl', 'wb') as f:
        pickle.dump(my_data, f)


def word_cloud_pic(comment_type: str):
    print('词云生成中')
    start_time = time.time()
    words = []
    # jieba切片
    for i in random.sample(my_data[comment_type]['content'], comment_sample):
        words.extend(jieba.lcut(i, use_paddle=True))
    # 原始数据取样
    for i in my_data[comment_type]['content']:
        new_words = i
        if len(new_words) > comment_sample:
            new_words = random.sample(new_words, comment_sample)
        words.extend(jieba.lcut(new_words, use_paddle=True))
    # 抽样取词 优化速度
    if len(words) > word_sample:
        words = random.sample(words, word_sample)
    # 去除无用词
    len_count = word_sample
    # count = 0
    for i in words.copy():
        if i in ignore_words:
            words.remove(i)
        # count += 1
        # if count % 1000 == 0:
        #     print(count, len_count)
    WordCloud(font_path="msyh.ttc", max_words=500, width=1920, height=1080).generate(' '.join(words)).to_file(
        os.path.join('static', f'{comment_type}.jpg'))
    plt.imshow(imread(os.path.join('static', f'{comment_type}.jpg')))
    # plt.show()
    end_time = time.time()
    print(f'词云生成完成， 耗时：{end_time - start_time}秒')


def rank_pic():
    print('评分统计生成中')
    start_time = time.time()
    long_rank = pd.Series(my_data['long']['score'], name='长评')
    short_rank = pd.Series(my_data['short']['score'], name='短评')
    p_data = pd.DataFrame(data=pd.concat([long_rank, short_rank], axis=1),
                          index=pd.Index([2, 4, 6, 8, 10], name='评分'),
                          columns=pd.Index(['长评', '短评'], name='评论类型'))

    # print(p_data.loc[2])


    all_mark = (p_data.index * p_data.sum(axis=1)).sum()
    markers = p_data.sum(axis=1).sum()
    avg_mark = round(all_mark/markers, 2)
    print(avg_mark)

    p_data.plot.bar()
    plt.suptitle(f'平均分：{avg_mark}')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylabel('数量')
    plt.savefig(os.path.join('static', 'rank.jpg'))
    # plt.show()
    end_time = time.time()
    print(f'评分统计生成完成， 耗时：{end_time - start_time}秒')


def run_task():
    global last_time
    run_get()
    threading.Thread(target=rank_pic).start()
    threading.Thread(target=word_cloud_pic, args=('long', )).start()
    threading.Thread(target=word_cloud_pic, args=('short', )).start()
    now = datetime.now()
    last_time = now.strftime("%Y/%m/%d-%H:%M")


if __name__ == '__main__':
    # run_task()
    with open('data.pkl', 'rb') as f:
        my_data = pickle.load(f)  # type: dict
    # run_get()
    rank_pic()
    plt.show()
    word_cloud_pic('long')
    plt.show()
    word_cloud_pic('short')
    plt.show()

