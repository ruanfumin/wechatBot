from collections import namedtuple
import time
import json
import requests
from StationThreeLine import wuWeiDaDi


Water = namedtuple('WaterLevel', ['datetime', 'waterlevel']) # 水位元祖 [时间， 水位]


class WaterInfo(object):
    """获取水位数据的类"""

    def _response(self) -> None:
        """发送请求获取数位Json数据"""
        URL = 'http://cjsw.cjh.com.cn:8088/swjapp/call.nut'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'http://wx.cjh.com.cn/cjsw/swwx/view/sssq-zd-hd.html?stcd=62904500&t=1594883640'
            }
        form_data = {"requests":[{"interfaceName":"publicApi.getStationInfo","params":{"stcd":"62904500"},"os":3,"version_code":60,"token":""}]}
        self.r = None
        while True:
            self.r = requests.post(url=URL, headers=headers, data=json.dumps(form_data))
            if self.r.status_code == 200:
                break
            else:
                self.r.raise_for_status()
            print('HTTP请求异常,等待60秒再次尝试.')
            time.sleep(60)

    def getAllData(self) -> list:
        """获取所有水位数据"""
        self._response()
        data_obj = json.loads(self.r.text, strict=False)
        dataList = data_obj['responses'][0]['data']['dataList']
        result = []
        for data in dataList:
            w = Water(datetime=data['tm'], waterlevel=float(data['rz']))
            result.append(w)
        return result

    def getTodayData(self) -> list:
        """获取今日所有水位数据"""
        dataList = self.getAllData() # 所有水位数据
        today = time.strftime("%Y-%m-%d", time.localtime())
        todayLength = len(today)
        result = []
        for data in dataList:
            if today == data.datetime[:todayLength]:
                result.append(data)
        return result

    def getTodayHourData(self) -> list:
        """获取今日所有整点水位数据"""
        dataList = self.getTodayData() # 今日水位数据
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
            if data.datetime in hourList:
                result.append(data)
        return result

    def getTodayNowHourData(self, minute: int = 1) -> Water:
        """获取现在的整点水位，若无进入循环等待，获取到跳出循环"""
        while True:
            if self.getTodayHourData() == []: # 刚过0点，整点数据为0的情况
                print('0点异常等待')
                time.sleep(60 * minute)
                continue
            hourData = self.getTodayHourData()[0]
            if hourData.datetime == time.strftime("%Y-%m-%d %H:00:00", time.localtime()):
                s = '{0} 成功获取当前整点水位数据'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print(s)
                return hourData
            s = '{0} 没有当前整点数据，等待{1}秒再次尝试'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), str(minute * 60))
            print(s)
            time.sleep(60 * minute)
    
    def _sjoin(self, station, waterlevel: float) -> str:
        s = '\n'
        if waterlevel > station.baozheng:
            a = ("%.2f" % (waterlevel-station.baozheng))
            s = s + '超保证水位' + ': ' + str(a) + 'm'
        elif waterlevel > station.jingjie:
            a = ("%.2f" % (waterlevel-station.jingjie))
            s = s + '超警戒水位' + ': ' + str(a) + 'm'
        elif waterlevel > station.shefang:
            a = ("%.2f" % (waterlevel-station.shefang))
            s = s + '超设防水位' + ': ' + str(a) + 'm'
        return s
    
    def getWuWeiDaDiTextInfo(self, waterlevel: Water):
        s = '站名：{0}\n'.format(wuWeiDaDi.name)
        # print(waterlevel)
        s = s + '时间：{0}\n当前水位：{1}m'.format(*(waterlevel.datetime, waterlevel.waterlevel))
        s = s + self._sjoin(wuWeiDaDi, waterlevel.waterlevel)
        return s

if __name__ == '__main__':
    w = WaterInfo()
    print(w.getWuWeiDaDiTextInfo(w.getTodayNowHourData()))
