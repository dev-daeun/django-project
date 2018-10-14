__all__ = (
    'Webtoon',
    'WebtoonNotExist',
)


class Webtoon:
    TEST_WEBTOON_ID = 714834
    EPISODE_LIST_BASE_URL = 'https://comic.naver.com/main.nhn'

    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail

    def __repr__(self):
        return self.title

    def get_episode_list_url_params_dict(self, **kwargs):
        params = {
            'title_id': self.webtoon_id,
        }
        params.update[kwargs]
        return params


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'Webtoon(title: {self.title})을 찾을 수 없습니다'
