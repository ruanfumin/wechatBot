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
        baimaozhen = self.bot.groups().search('区联系白茆防汛抗旱工作群')[0]
        baimaozhen.send(w_info)


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
    schedule.every().day.at("00:03").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("01:02").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("02:04").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("03:05").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("04:02").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("05:04").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("06:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("07:03").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("08:02").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("09:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("10:03").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("11:02").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("12:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("13:11").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("14:09").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("15:07").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("16:04").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("17:04").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("18:09").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("19:06").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("20:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("21:10").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("22:06").do(wechatbot.sendWaterLevelMessage)
    schedule.every().day.at("23:04").do(wechatbot.sendWaterLevelMessage)
    # 每10分钟发消息防止掉线
    schedule.every(30).minutes.do(wechatbot.keepWechatOnline)
    while True:
        schedule.run_pending()
        time.sleep(1)
