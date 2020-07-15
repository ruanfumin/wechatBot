from collections import namedtuple
import time
from selenium import webdriver
from bs4 import BeautifulSoup


Water = namedtuple('WaterLevel', ['station', 'city', 'level', 'river', 'code'])

class WaterInfo(object):
    _url = 'http://yc.wswj.net/fxtweb/pages/hd.html'

    def __init__(self):
        self.chrome = webdriver.Chrome()
        
    def getWaterLevel(self) -> list:
        self.chrome.get(self._url)
        listButton = self.chrome.find_element_by_xpath("//span[@data-id='2']")
        listButton.click()
        time.sleep(3)
        soure_html = self.chrome.page_source
        self.chrome.quit()
        soup = BeautifulSoup(soure_html, "html.parser")
        tr_list = soup.select('.bg_cjsw')
        waterLevel_list = []
        for tr in tr_list:
            td_list = tr.select('td')
            if '芜湖市' == td_list[2].text:
                wl = Water(station=td_list[1].text, city=td_list[2].text, level=td_list[3].text, river=td_list[4].text, code=td_list[6].text) 
                waterLevel_list.append(wl)
        return waterLevel_list


if __name__ == '__main__':
    w = WaterInfo()
    l = w.getWaterLevel()
    for i in l:
        s = '{0} {1}'.format(i.station, i.level)
        print(s)
