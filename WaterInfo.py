from collections import namedtuple
import time
import json
import requests
from pyecharts import options
from pyecharts.charts import Line
from numpy import mean


Water = namedtuple('WaterLevel', ['tm', 'rz'])


class WaterInfo(object):
    def __init__(self) -> None:
        URL = 'http://cjsw.cjh.com.cn:8088/swjapp/call.nut'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'http://wx.cjh.com.cn/cjsw/swwx/view/sssq-zd-hd.html?stcd=62904500&t=1594883640'
            }
        form_data = {"requests":[{"interfaceName":"publicApi.getStationInfo","params":{"stcd":"62904500"},"os":3,"version_code":60,"token":""}]}
        self.r = requests.post(url=URL, headers=headers, data=json.dumps(form_data))
    
    def getTodayHourData(self) -> list:
        """获取今天的水位"""
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
    
    def _filterHour(self):
        """过滤 仅保留整点时间数据"""
        hour = time.localtime().tm_hour
        hourList = []
        for i in range(hour+1):
            if i < 10:
                s = time.strftime("%Y-%m-%d ", time.localtime()) + '0' + str(i) + ':00:00'
            else:
                s = time.strftime("%Y-%m-%d ", time.localtime()) + str(i) + ':00:00'
            hourList.append(s)
        return hourList
    
    def render(self):
        title = '凤凰颈闸下水位: ' + time.strftime("%Y年%m月%d日", time.localtime())
        data = self.getTodayHourData()
        x_data = []
        y_data = []
        for i in data:
            x_data.append(i.tm[11:-3]), y_data.append(i.rz)
        x_data.reverse()
        avg_water = mean(y_data)
        max_water = max(y_data)
        min_water = min(y_data)
        line = (Line()
            .add_xaxis(x_data)
            .add_yaxis('水位', y_data, linestyle_opts=options.LineStyleOpts(type_='solid'))
            .set_series_opts(
                markline_opts=options.MarkLineOpts(
                    data=[
                        options.MarkLineItem(y=avg_water, name='平均水位', type_='average'),
                        options.MarkLineItem(y=max_water, name='最高水位', type_='max'),
                        options.MarkLineItem(y=min_water, name='最低水位', type_='min'),
                        ]
                )
            )
            .set_global_opts(
                title_opts=options.TitleOpts(
                    title=title,
                    title_textstyle_opts=options.TextStyleOpts(color='red')
                    ),
                yaxis_opts=options.AxisOpts(name="水位/m", is_scale=14, max_=max_water),
                xaxis_opts=options.AxisOpts(name="时间")
                )
            )
        line.render("图例.html")

if __name__ == '__main__':
    w = WaterInfo()
    w.render()
