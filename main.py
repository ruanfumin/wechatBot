import schedule
import time
import datetime
from wxpy import Bot
from waterlevel import WaterLevel


class WechatBot(object):
    def __init__(self) -> None:
        self.bot = Bot(cache_path=True)


    def sendWaterLevelMessage(self) -> None:
        """向保安站工作群发水位信息"""
        w = WaterLevel()
        w_info = w.getInfo()
        jianguanchu = self.bot.groups().search('保安站建设管理处')[0]
        yezhuqun = self.bot.groups().search('保安站建设工作业主群')[0]
        jianguanchu.send(w_info)
        yezhuqun.send(w_info)


    def sendTestMessage(self) -> None:
        """向微信小号(python)发送测试信息"""
        xiaohao = self.bot.friends().search('Python')[0]
        xiaohao.send('你好，这是测试信息')


    def keepWechatOnline(self) -> None:
        """防止微信掉线"""
        gongqingtuan = self.bot.mps().search('芜湖共青团')[0]
        gongqingtuan.send('你好啊，团团')
        print("于 " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "向团团发送消息防止掉线。")


if __name__ == '__main__':
    wechatbot = WechatBot()
    schedule.every().day.at("06:10").do(wechatbot.sendWaterLevelMessage)
    # 每10分钟发消息防止掉线
    schedule.every(30).minutes.do(wechatbot.keepWechatOnline)
    while True:
        schedule.run_pending()
        time.sleep(1)
