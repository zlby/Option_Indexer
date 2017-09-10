#爬取豆粕现货数据
import requests
from bs4 import BeautifulSoup


def get_spot_today():

    res=requests.get('http://www.sci99.com/price-560-21165-24698.html')
    soup=BeautifulSoup(res.text,'html.parser')
    table=soup.find('table')
    trs=table.find_all('tr',recursive=False)
    for tr in trs:
        date=tr.contents[1].string.strip()
        spot_price=tr.contents[3].string.strip()
        print(date,spot_price)
