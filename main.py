import schedule
import time
import datetime
from wxpy import Bot
from WaterInfo import WaterInfo


class WechatBot(object):
    def __init__(self) -> None:
        print('程序开始运行')
        self.bot = Bot(cache_path=True)
        self.water = WaterInfo()
        self.baimaozheng = self.bot.groups().search('区联系白茆防汛抗旱工作群')[0] # 白茆镇联系群
        self.yezhuqun = self.bot.groups().search('保安站建设工作业主群')[0] # 保安站业主群

    def sendWaterLevelMessage(self) -> None:
        """发水位信息"""
        s = '{0} 准备向工作群发水位数据'.format(time.strftime("%H:%M:%S", time.localtime()))
        print(s)
        w = self.water.getTodayNowHourData()
        self.baimaozheng.send(self.water.getYongdingAndHeishazhou(w))
        self.yezhuqun.send(self.water.getWuwei(w))
        s = '{0} 已向工作群发送水位数据'.format(time.strftime("%H:%M:%S", time.localtime()))
        print(s)

    def keepWechatOnline(self) -> None:
        """防止微信掉线"""
        gongzhonghao = self.bot.mps().search('菜鸟学Python')[0]
        gongzhonghao.send('人生苦短，我学Python')
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "发送消息防止掉线")


if __name__ == '__main__':
    wechatbot = WechatBot()
    for i in range(0,24):
        s = ''
        if i < 10:
            s = '0' 
        s = s + str(i) + ':16'
        schedule.every().day.at(s).do(wechatbot.sendWaterLevelMessage)
    
    # 每10分钟发消息防止掉线
    schedule.every(10).minutes.do(wechatbot.keepWechatOnline)
    while True:
        schedule.run_pending()
        time.sleep(1)
