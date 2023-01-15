# -*- coding: utf-8 -*-
import httpx
from settings import headers, media_id


class GetRankApi:
    def __init__(self, comment_type, media_id, cursor=0):
        self.cursor = cursor
        self.next = None
        self.comment_type = comment_type
        self.media_id = media_id
        self.client = httpx.Client()
        # self.get_rank()

    def get_rank(self):
        """
        :param cursor: cursor position
        :return: list total_count
        """
        url = f'https://api.bilibili.com/pgc/review/{self.comment_type}/list'

        try:
            resp = self.client.get(url=url, headers=headers, params={
                'media_id': self.media_id,
                'ps': 12575,
                'sort': 0,
                'cursor': self.next,
            })
        except:
            return self.get_rank()
        try:
            resp = resp.json()
        except:
            print('报错啦', self.next)
            return self.get_rank()
        # print(resp)
        self.next = resp['data']['next']
        return resp['data']['list'], resp['data']['total'], resp['data']['next']


if __name__ == '__main__':
    session = GetRankApi('long', media_id)
    print(session.get_rank())

