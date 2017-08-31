import requests
from bs4 import BeautifulSoup
res=requests.get('http://www.dce.com.cn/publicweb/businessguidelines/queryContractInfoVariety.html?variety=m')
soup=BeautifulSoup(res.text,'html.parser')
trs= soup.find_all('tr')
for i in range(125,len(trs)): #从m1707开始
    tds = trs[i].find_all('td')
    name=tds[1].text
    begin_trade_date=tds[4].text #开始交易日
    end_trade_date=tds[5].text   #最后交易日
    print(name,begin_trade_date,end_trade_date)