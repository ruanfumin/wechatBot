from collections import namedtuple
import time
import json
import requests


Water = namedtuple('WaterLevel', ['tm', 'rz'])
WaterLevel = namedtuple('WaterLevel', ['name', 'sf', 'jj', 'bz'])


class WaterInfo(object):

    def _response(self) -> None:
        """发送请求获取数位Json数据"""
        URL = 'http://cjsw.cjh.com.cn:8088/swjapp/call.nut'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'http://wx.cjh.com.cn/cjsw/swwx/view/sssq-zd-hd.html?stcd=62904500&t=1594883640'
            }
        form_data = {"requests":[{"interfaceName":"publicApi.getStationInfo","params":{"stcd":"62904500"},"os":3,"version_code":60,"token":""}]}
        self.r = requests.post(url=URL, headers=headers, data=json.dumps(form_data))

    def getAllData(self) -> list:
        """获取所有水位数据"""
        self._response()
        data_obj = json.loads(self.r.text)
        dataList = data_obj['responses'][0]['data']['dataList']
        result = []
        for data in dataList:
            w = Water(tm=data['tm'], rz=float(data['rz']))
            result.append(w)
        return result

    def getTodayData(self) -> list:
        """获取今日所有水位数据"""
        dataList = self.getAllData() # 在所有水位数据基础上过滤
        today = time.strftime("%Y-%m-%d", time.localtime())
        todayLength = len(today)
        result = []
        for data in dataList:
            if today == data.tm[:todayLength]:
                result.append(data)
        return result

    def getTodayHourData(self) -> list:
        """获取今日所有整点水位数据"""
        dataList = self.getTodayData() # 在今日水位数据基础上过滤
        hour = time.localtime().tm_hour
        hourList = []
        result = []
        for i in range(hour + 1):
            if i < 10:
                s = time.strftime("%Y-%m-%d ", time.localtime()) + '0' + str(i) + ':00:00'
            else:
                s = time.strftime("%Y-%m-%d ", time.localtime()) + str(i) + ':00:00'
            hourList.append(s)
        for data in dataList:
            if data.tm in hourList:
                result.append(data)
        return result

    def getTodayNowHourData(self, minute: int = 1) -> Water:
        """获取现在的整点水位数据，若无就进入循环等待，获取到跳出循环"""
        while True:
            if self.getTodayHourData() == []: # 刚过0点，整点数据为0的情况
                print('0点异常等待')
                time.sleep(60 * minute)
                continue
            hourData = self.getTodayHourData()[0]
            if hourData.tm == time.strftime("%Y-%m-%d %H:00:00", time.localtime()):
                s = '{0} 成功获取当前整点水位数据'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print(s)
                return hourData
            s = '{0} 没有当前整点数据，等待{1}秒再次尝试'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(minute * 60))
            print(s)
            time.sleep(60 * minute)
    
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
    
    def getYongdingAndHeishazhou(self, w: Water) -> str:
        """获取永定和黑沙洲水位信息"""
        yongding = WaterLevel(name='永定大圩', sf=11.5, jj=13.2, bz=14.5)
        heishazhou = WaterLevel(name='黑沙洲、天然洲', sf=11.0, jj=13.0, bz=13.5)
        s = "时间:{tm}\n站名:凤凰颈闸下\n现在水位:{rz}m".format(tm=w.tm, rz=w.rz)
        s = s + self._sjoin(yongding, w.rz)
        s = s + self._sjoin(heishazhou, w.rz)
        return s

    def getWuwei(self, w: Water) -> str:
        """获取无为大堤水位信息"""
        wuwei = WaterLevel(name='无为大堤', sf=11.5, jj=13.2, bz=15.84)
        s = "时间:{tm}\n站名:凤凰颈闸下\n现在水位:{rz}m".format(tm=w.tm, rz=w.rz)
        s = s + self._sjoin(wuwei, w.rz)
        return s

if __name__ == '__main__':
    w = WaterInfo()
    # i = w.getWuwei(w.getTodayNowHourData())
    print(w.getTodayNowHourData())
