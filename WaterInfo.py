from collections import namedtuple
import time
import json
import requests


Water = namedtuple('WaterLevel', ['tm', 'rz'])
WaterLevel = namedtuple('WaterLevel', ['name', 'sf', 'jj', 'bz'])


class WaterInfo(object):

    def _response(self) -> None:
        URL = 'http://cjsw.cjh.com.cn:8088/swjapp/call.nut'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'http://wx.cjh.com.cn/cjsw/swwx/view/sssq-zd-hd.html?stcd=62904500&t=1594883640'
            }
        form_data = {"requests":[{"interfaceName":"publicApi.getStationInfo","params":{"stcd":"62904500"},"os":3,"version_code":60,"token":""}]}
        self.r = requests.post(url=URL, headers=headers, data=json.dumps(form_data))

    def _filterHour(self):
        """过滤非整点时间数据"""
        hour = time.localtime().tm_hour
        hourList = []
        for i in range(hour+1):
            if i < 10:
                s = time.strftime("%Y-%m-%d ", time.localtime()) + '0' + str(i) + ':00:00'
            else:
                s = time.strftime("%Y-%m-%d ", time.localtime()) + str(i) + ':00:00'
            hourList.append(s)
        return hourList

    def getTodayHourData(self) -> list:
        """获取今日整点水位"""
        self._response()
        data_obj = json.loads(self.r.text)
        dataList = data_obj['responses'][0]['data']['dataList']
        r = []
        today = time.strftime("%Y-%m-%d", time.localtime())
        todayLength = len(today)
        for data in dataList:
            if today == data['tm'][:todayLength]: # 筛选出今日数据
                hourList = self._filterHour()
                if data['tm'] in hourList:
                    w = Water(tm=data['tm'], rz=float(data['rz']))
                    r.append(w)
        return r
    
    
    def _sjoin(self, station: WaterLevel, waterlevel: float) -> str:
        s = '\n'
        if waterlevel > station.bz:
            a = ("%.2f" % (waterlevel-station.bz))
            s = s + station.name + '超保证水位' + ': ' + str(a) + 'm'
        elif waterlevel > station.jj:
            a = ("%.2f" % (waterlevel-station.jj))
            s = s + station.name + '超警戒水位' + ': ' + str(a) + 'm'
        elif waterlevel > station.sf:
            a = ("%.2f" % (waterlevel-station.sf))
            s = s + station.name + '超设防水位' + ': ' + str(a) + 'm'
        return s
    
    def _isNow(self) -> bool:
        data = self.getTodayHourData()[0]
        if data.tm == time.strftime("%Y-%m-%d %H:00:00", time.localtime()):
            return True
        return False

    def getInfoStr(self):
        yongding = WaterLevel(name='永定大圩', sf=11.5, jj=13.2, bz=14.5)
        heishazhou = WaterLevel(name='黑沙洲、天然洲', sf=11.0, jj=13.0, bz=13.5)
        while True:
            if self._isNow():
                break
            time.sleep(60)
        data = self.getTodayHourData()[0]
        s = """时间:{tm}
站名:凤凰颈闸下
现在水位:{rz}m""".format(tm=data.tm, rz=data.rz)
        s = s + self._sjoin(yongding, data.rz)
        s = s + self._sjoin(heishazhou, data.rz)
        return s

    def getWuwei(self):
        wuwei = WaterLevel(name='无为大堤', sf=11.5, jj=13.2, bz=15.84)
        while True:
            if self._isNow():
                break
            time.sleep(60)
        data = self.getTodayHourData()[0]
        s = """时间:{tm}
站名:凤凰颈闸下
现在水位:{rz}m""".format(tm=data.tm, rz=data.rz)
        s = s + self._sjoin(wuwei, data.rz)
        return s 

if __name__ == '__main__':
    w = WaterInfo()
    print(w.getWuwei())
