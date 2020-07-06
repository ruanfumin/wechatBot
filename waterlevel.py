import time
import json
import requests


class WaterLevel(object):
    """获取水位信息类"""

    def __init__(self) -> None:
        """初始化请求地址及请求参数"""
        self.URL = "http://www.whswj.net/ahwater/whshqxx/BusinessHandler.ashx"
        date_now = time.strftime("%Y%m%d", time.localtime())
        self.params = {
            "name": "SelectToDayZZSQBriefing",
            "time": date_now + "0600",
            "stcdid": "4023"
        }
        
    
    def _getRequest(self) -> bool:
        """发送获取数据请求
        Returns:
            bool: True成功 False失败
        """
        response = requests.get(self.URL, params=self.params)
        if(response.status_code == 200):
            # json字符串 -> json对象
            json_obj = json.loads(response.text)
            # 凤凰颈闸下位置为8
            self._info = json_obj[7]
            self._info['date'] = time.strftime("%Y年%m月%d日", time.localtime()) + "6:00"
            return True
        else:
            return False

    def getInfo(self) -> str:
        if(self._getRequest()):
            # 当前水位，设防水位，警戒水位，保证水位
            z, sf, wrz, grz = float(self._info['Z']), 11.5,float(self._info['WRZ']),float(self._info['GRZ'])
            description = "描述："
            if z < sf:
                description = ''
            elif z < wrz:
                description = description + "已达设防水位"
            elif z < grz:
                description = description + "已达警戒水位"
            else:
                description = description + "已达保证水位"
            waterlevelinfo = """站名：{STNM}
时间：{date}
水位高度：{Z}m\n""".format(**self._info)
            waterlevelinfo = waterlevelinfo + description + """\n比昨日: {RZF}m
设防水位：11.5m
警戒水位：{WRZ}m
保证水位：{GRZ}m
历史最高水位：{OBHTZ}m""".format(**self._info)
            return waterlevelinfo
        else:
            return ""
