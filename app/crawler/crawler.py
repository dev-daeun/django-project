import os
import pickle  # 파이썬 자료형의 데이터를 파일에 r/w 하게 해주는 모듈.
import re

import requests
from bs4 import BeautifulSoup

from .data import Episode, Webtoon, WebtoonNotExist


class Crawler:
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    SAVE_PATH = os.path.join(ROOT_PATH, 'saved_data')

    def __init__(self):
        self._webtoon_dict = {}
        os.makedirs(self.SAVE_PATH, exist_ok=True)  # exist_ok=False: 폴더가 이미 존재하면 OSError 발생.

    def get_html(self):
        """
        웹툰 전체 목록의 HTML을 리턴한다.
        파일로 저장되어 있다면 파일을 읽어온다. 위치는 ./saved_data/weekday.html
        파일로 저장되어있지 않다면 웹에서 요청해서 받아온다.

        :return: 문자열 형태의 HTML 내용.
        """
        root = os.path.dirname(os.path.abspath(__file__))
        dir_path = os.path.join(root, 'saved_data')
        file_path = os.path.join(dir_path, 'weekday.html')

        if os.path.exists(file_path):
            html = open(file_path, 'rt').read()
        else:
            os.makedirs(dir_path, exist_ok=True)
            response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
            html = response.text
            open(file_path, 'wt').write(html)
        return html

    @property
    def webtoon_dict(self):
        """
        _webtoon_dict에 있는 모든 웹툰 리스트를 리턴한다.
        html을 읽어와서 요일별 웹툰들을 파싱하고, 파싱한 웹툰제목이 _webtoon_dict에 없으면 Webtoon클래스의 객체를 새로 추가한다.
        :return: _webtoon_dict
        """
        if not self._webtoon_dict:
            html = self.get_html()
            soup = BeautifulSoup(html, 'lxml')  # lxml파서는 디폴트로 제공하는 html.parser 보다 속도가 빠르다.
            day_columns = soup.select_one('div.list_area.daily_all').select('.col')  # select(): css문법으로 태그를 뽑아준다.
            element_list = []
            for col in day_columns:
                day_element = col.select('.col_inner ul > li')
                element_list.extend(day_element)

            for element in element_list:
                # select_one(): 셀렉된 태그들 중 첫번째 태그 리턴. html 클래스는 대괄호로 접근.
                href = element.select_one('a.title')['href']
                # re.search(): href 문자열에서 정규식에 매칭되는 문자열을 리턴. 예) titleId=1234
                matched_querystring = re.search(r'titleId=(\d+)', href)
                # group(): 정규식에 들어맞는 문자열을 제외한 값만 리턴. 예) 1234
                webtoon_id = matched_querystring.group()
                title = element.select_one('a.title').get_text(strip=True)  # 문자열 양 끝에 whitespace 제거.
                url_thumbnail = element.select_one('.thumb > a > img')['src']

                if title not in self._webtoon_dict:
                    new_webtoon = Webtoon(webtoon_id, title, url_thumbnail)
                    self._webtoon_dict[title] = new_webtoon

        return self._webtoon_dict

    def webtoon_list(self):
        """
        웹툰 전체 목록을 웹툰 제목으로 출력한다.
        """
        # 딕셔너리의 키, 밸류를 순회할 때는 dict.items()
        for title, webtoon in self.webtoon_dict.items():
            print(title)

    def get_webtoon(self, title):
        """
        title이 제목인 Webtoon객체를 가져옴
        :param title:
        :return: Webtoon
        """
        try:
            return self.webtoon_dict[title]
        except KeyError:
            raise WebtoonNotExist(title)


    def save(self):
        """
        _webtoon_dict을 saved_data/crawler.pickle 에 기록한다.
        """
        # pickle에서 파이썬 자료형의 데이터를 r/w할 때는 바이트단위로 읽어온다.
        with open(os.path.join(self.SAVE_PATH, 'crawler.pickle'), 'wb') as f:
            pickle.dump(self._webtoon_dict, f)

    def load(self):
        """
        saved_data/crawler.pickle 파일을 읽어들여서 _webtoon_dict 을 업데이트한다.
        """
        with open(os.path.join(self.SAVE_PATH, 'crawler.pickle'), 'rb') as f:
            self._webtoon_dict = pickle.load(f)