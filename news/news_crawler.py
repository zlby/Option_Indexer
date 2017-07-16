import requests
from bs4 import BeautifulSoup
class News_item(object):
    def __init__(self,title,time,content_url):
        self.title=title
        self.time=time
        self.content_url=content_url

    def __repr__(self) -> str:
        return self.title+self.time+self.content_url

    def get_content(self):
        r=requests.get(self.content_url)
        r.encoding='utf-8'
        s=BeautifulSoup(r.text,'html.parser')
        s= s.find('div',id='artibody')
        p = s.find_all('p')
        result=''
        for i in range(1, len(p)-1):
            result=result+p[i].text

        # br=s.find_all('br')
        # for i in range(0,len(br)-1):
        #     result=result+br[i].text
        return result.strip();

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, News_item):
            return self.title==o.title
        else:
            return False


res=requests.get('http://finance.sina.com.cn/money/future/M/')
res.encoding='gb2312'
soup=BeautifulSoup(res.text,'html.parser')
news_contlist=soup.find('div', 'contlist')
news_list=[]
# file=open("news.txt","w", 'utf-8')
file = open('news.txt', 'w', encoding='utf-8')
for li in news_contlist.find_all('li'):
    if News_item(li.a.text, li.a.next_sibling, li.a['href']) not in news_list:
     news_list.append(News_item(li.a.text, li.a.next_sibling, li.a['href']))

for i in range(0,len(news_list)):
    content=news_list[i].get_content()
    if len(content)>30 :
      file.write(news_list[i].title+'\n')
      file.write(news_list[i].time+'\n')
      file.write(content.replace(u'\xa0',u' ')+'\n')
      file.write('\n')
file.close()