import requests
from bs4 import BeautifulSoup
from datetime import datetime
from option.models import News
import logging

log = logging.getLogger('option')


class NewsSpider:
    index_url = 'http://finance.sina.com.cn/money/future/M/'

    @staticmethod
    def get_data():
        log.info(datetime.now())
        res = requests.get(NewsSpider.index_url)
        res.encoding = 'gb2312'
        soup = BeautifulSoup(res.text.replace(u'\xa0', u' '), 'html.parser')
        news_content_list = soup.find('div', 'contlist')

        for li in news_content_list.find_all('li'):
            title = li.a.text
            time = datetime.strptime('%s' % datetime.now().year+li.a.next_sibling, '%Y(%m-%d %H:%M)')
            url = li.a['href'].strip()
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup.find('div', id='artibody'):
                p = soup.find('div', id='artibody').find_all('p')
                text = ''
                for i in range(1, len(p) - 1):
                    text = text + p[i].text.strip() + '\n'
                text = text.strip()
                if text:
                    News.objects.create(title=title, content=text, time=time)

