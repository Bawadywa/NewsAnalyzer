import requests
from bs4 import BeautifulSoup
import codecs

html_parser = 'html.parser'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/101.0.4951.54 Safari/537.36'
}

urls = {'tsn': 'https://tsn.ua/',
        '24tv': 'https://24tv.ua/',
        'epravda': 'https://www.epravda.com.ua/news/',
        'pravda': 'https://www.pravda.com.ua/news/',
        'liga': 'https://news.liga.net/ua',
        'zaxid': 'https://zaxid.net/news/',
        'ukrinform': 'https://www.ukrinform.ua/block-lastnews',
        'unn': 'https://www.unn.com.ua/uk/news',
        'radiosvoboda': 'https://www.radiosvoboda.org/z/630',
        'korrespondent': 'https://ua.korrespondent.net/all/',
        'segodnya': 'https://ukraine.segodnya.ua/ua/allnews.html',
        'gazeta': 'https://gazeta.ua/news',
        'mind': 'https://mind.ua/news',
        'censor': 'https://censor.net/ua/news/all',
        'zn': 'https://zn.ua/ukr/all-news',
        'espreso': 'https://espreso.tv/news',
        'lb': 'https://lb.ua/'
        }


class Parser:
    def __init__(self, headers, soup_parser):
        self.headers = headers
        self.soup_parser = soup_parser

    def parse_tsn(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get sidebar section with news
            news_block = soup.select_one('section.l-sidebar')
            # get links with titles
            news_items = news_block.select('a.c-card__link')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('tsn', e)
            return []

    def parse_24tv(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get sidebar divs with news
            news_block = soup.select_one('div.news-list-wrapper')
            # get links with titles
            news_items = news_block.select('div.news-title a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('24tv', e)
            return []


    def parse_epravda(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # remove em elements to clean data
            em_elements = soup.find_all('em')
            for em in em_elements:
                em.decompose()
            # get sidebar div with news
            news_block = soup.select_one('div.news_list')
            # get links with titles
            news_items = news_block.select('div.article__title a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('epravda', e)
            return []

    def parse_pravda(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # remove em elements to clean data
            em_elements = soup.find_all('em')
            for em in em_elements:
                em.decompose()
            # get sidebar div with news
            news_block = soup.select_one('div.container_sub_news_list')
            # get links with titles
            news_items = news_block.select('div.article_header a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('pravda', e)
            return []

    def parse_liga(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # remove archive link to clean data
            archive_div = soup.select_one('div.more-news.archive-button')
            archive_div.decompose()
            # get sidebar div with news
            news_block = soup.select_one('div#all-news')
            # get links with titles
            news_items = news_block.find_all('a', class_='')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('liga', e)
            return []

    def parse_zaxid(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # remove desc elements to clean data
            desc_elements = soup.select('div.desc')
            for desc in desc_elements:
                desc.decompose()
            # get sidebar div with news
            news_block = soup.select_one('div.archive_page')
            # get divs with titles
            news_items = news_block.select('div.news-title')
            # read titles from divs and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('zaxid', e)
            return []

    def parse_ukrinform(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get section with news
            news_block = soup.select_one('section.restList')
            # get links with titles
            news_items = news_block.select('article a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('ukrinform', e)
            return []

    def parse_unn(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div.h-news-feed')
            # get links with titles
            news_items = news_block.select('li a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('unn', e)
            return []

    def parse_radiosvoboda(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div.media-block-wrap')
            # get titles
            news_items = news_block.select('div.media-block h4')
            # read titles and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('radiosvoboda', e)
            return []

    def parse_korrespondent(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div.articles-list')
            # get links with titles
            news_items = news_block.select('div.article__title a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('korrespondent', e)
            return []

    def parse_segodnya(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div.main')
            # get links with titles
            news_items = news_block.select('div.b-article__title a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('segodnya', e)
            return []

    def parse_mind(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div#new_content')
            # get links with titles
            news_items = news_block.select('div.news-item-title a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('mind', e)
            return []

    def parse_censor(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div.items-list')
            # get links with titles
            news_items = news_block.select('div.news-list-item h2 > a.news-list-item__link')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('censor', e)
            return []

    def parse_zn(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # remove telegram link to clean data
            tg_link = soup.select('a.news_zn_')
            for link in tg_link:
                link.decompose()
            # get div with news
            news_block = soup.select_one('div#left')
            # get links with titles
            news_items = news_block.select('div.news_block_item a.news_item')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('zn', e)
            return []

    def parse_espreso(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # get div with news
            news_block = soup.select_one('div.news_page__similar_content')
            # get links with titles
            news_items = news_block.select('div.news_page_similar_content_item__wrapper div.title > a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('espreso', e)
            return []

    def parse_lb(self, url):
        try:
            # make GET request and get response
            response = requests.get(url, headers=headers)
            # get html as text from response
            html = response.text
            # read html using bs4
            soup = BeautifulSoup(html, html_parser)
            # remove time elements, first ul block and show more li to clean data
            time_elements = soup.find_all('time')
            for time_elem in time_elements:
                time_elem.decompose()
            ul_elem = soup.select_one('section.col-left ul.feed-main')
            ul_elem.decompose()
            li_elem = soup.select_one('li.show-more')
            li_elem.decompose()
            # get div with news
            news_block = soup.select_one('section.col-left ul.feed-main')
            # get links with titles
            news_items = news_block.select('li a')
            # read titles from links and strip them
            news_titles = list(map(lambda item: item.text.strip(), news_items))
            result_titles = [title for title in news_titles if title]
            # for title in result_titles:
            #     print(title)
            return result_titles
        except Exception as e:
            print('lb', e)
            return []

    def get_all_news(self):
        news = self.parse_tsn(urls['tsn']) + self.parse_24tv(urls['24tv']) + self.parse_epravda(urls['epravda']) +\
               self.parse_pravda(urls['pravda']) + self.parse_liga(urls['liga']) + self.parse_zaxid(urls['zaxid']) +\
               self.parse_ukrinform(urls['ukrinform']) + self.parse_unn(urls['unn']) + self.parse_radiosvoboda(urls['radiosvoboda']) +\
               self.parse_korrespondent(urls['korrespondent']) + self.parse_segodnya(urls['segodnya']) + self.parse_mind(urls['mind']) +\
               self.parse_censor(urls['censor']) + self.parse_zn(urls['zn']) + self.parse_espreso(urls['espreso']) + self.parse_lb(urls['lb'])
        return news


def parse_today(file):
    parser = Parser(headers, html_parser)

    all_news = parser.get_all_news()

    with codecs.open(file, 'w+', encoding='utf-8') as f:
        for title in all_news:
            title = title.replace('\n', '')
            f.write(title)
            f.write('\n')

    return True

