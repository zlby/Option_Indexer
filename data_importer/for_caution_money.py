import requests
from bs4 import BeautifulSoup
from option.models import *


def update_deposit():
     res=requests.get('http://www.dce.com.cn/publicweb/notificationtips/queryDayTradParaByVariety.html?variety=m')
     soup=BeautifulSoup(res.text,'html.parser')
     trs= soup.find_all('tr')
     query_set_future = Future.objects.all()
     query_set_option = Option.objects.all()

     for i in range(2,len(trs)):
          tds=trs[i].find_all('td')
          name=tds[0].text.strip()
          name = name.lower()
          price=tds[2].text.strip()
          price = float(price.replace(',', ''))
          for future in query_set_future:
               if future.code == name:
                    obj = Future.objects.get(code=name)
                    obj.deposit_today = price
                    obj.save()
                    break
          for option in query_set_option:
               if option.code == name:
                    obj = Option.objects.get(code=name)
                    obj.deposit_today = price
                    obj.save()
                    break


