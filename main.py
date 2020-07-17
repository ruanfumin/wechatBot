import schedule
import time
import datetime
from wxpy import Bot
from WaterInfo import WaterInfo


class WechatBot(object):
    def __init__(self) -> None:
        self.bot = Bot(cache_path=True)

    def sendWaterLevelMessage(self) -> None:
        """向工作群发水位信息"""
        w = WaterInfo()
        w._isNow()
        baimaozhen = self.bot.groups().search('区联系白茆防汛抗旱工作群')[0]
        yezhuqun = self.bot.groups().search('保安站建设工作业主群')[0]
        baimaozhen.send(w.getYongdingAndHeishazhou())
        yezhuqun.send(w.getWuwei())

    def sendTestMessage(self) -> None:
        """向微信小号(python)发送测试信息"""
        xiaohao = self.bot.friends().search('Python')[0]
        xiaohao.send('<a href="https://jingyan.baidu.com/article/47a29f2439c718c0142399aa.html"> 点击蓝色字体，打开百度搜索 </a>')

    def keepWechatOnline(self) -> None:
        """防止微信掉线"""
        gongqingtuan = self.bot.mps().search('滁州水文')[0]
        gongqingtuan.send('我爱水文')
        print("于 " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "向滁州水文发送消息防止掉线。")


if __name__ == '__main__':
    wechatbot = WechatBot()
    for i in range(0,24):
        s = ''
        if i < 10:
            s = '0' + str(i) + ':05'
        else:
            s = str(i) + ':05'
        schedule.every().day.at(s).do(wechatbot.sendWaterLevelMessage)
    # schedule.every().second.do(wechatbot.sendTestMessage)
    
    # 每10分钟发消息防止掉线
    schedule.every(30).minutes.do(wechatbot.keepWechatOnline)
    while True:
        schedule.run_pending()
        time.sleep(1)
