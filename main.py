import schedule
import time
import datetime
from wxpy import Bot
from WaterInfo import WaterInfo


class WechatBot(object):
    def __init__(self) -> None:
        self.bot = Bot(cache_path=True)


    def sendWaterLevelMessage(self) -> None:
        """向保安站工作群发水位信息"""
        w = WaterInfo()
        w_info = w.getInfoStr()
        baimaozhen = self.bot.groups().search('区联系白茆防汛抗旱工作群')[0]
        yezhuqun = self.bot.groups().search('保安站建设工作业主群')[0]
        baimaozhen.send(w_info)
        yezhuqun.send(w.getWuwei())

    def sendTestMessage(self) -> None:
        """向微信小号(python)发送测试信息"""
        xiaohao = self.bot.friends().search('Python')[0]
        xiaohao.send('你好，这是测试信息')


    def keepWechatOnline(self) -> None:
        """防止微信掉线"""
        gongqingtuan = self.bot.mps().search('滁州水文')[0]
        gongqingtuan.send('我爱水文')
        print("于 " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "向滁州水文发送消息防止掉线。")


if __name__ == '__main__':
    wechatbot = WechatBot()
    schedule.every().day.at("00:05").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("01:05").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("02:05").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("03:05").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("04:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("05:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("06:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("07:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("08:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("09:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("10:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("11:06").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("12:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("13:08").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("14:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("15:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("16:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("17:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("18:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("19:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("20:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("21:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("22:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("23:10").do(wechatbot.sendWaterLevelMessage)
    # 每10分钟发消息防止掉线
    schedule.every(30).minutes.do(wechatbot.keepWechatOnline)
    while True:
        schedule.run_pending()
        time.sleep(1)
