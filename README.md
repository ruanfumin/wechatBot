# 微信机器人自动发水位数据助手

## 背景
> 防汛期间，单位通过人工获取各水文站点数据制作表格按时修改数据截图发工作群中，人工获取数据辛苦且不稳定，防汛各阶段要求不同，比如防汛形势紧张时，水文数据需要一小时一发，任务单一还繁重。

## 特性
- 使用REQUESTS库即时获取水文数据
- 基于wxpy库实现微信发消息功能
- 使用schedule库实现定时功能

## 安装
安装依赖库：
```shell
pip install -r Requirements.txt
```

## 简介
数据来源：[长江水文 水情信息](http://wx.cjh.com.cn/cjsw/swwx/view/sssq-zd-hd.html?stcd=62904500&t=1594883640)

运行:
```shell
python main.py
```

出现微信二维码，扫描登陆微信。


## 更新日志

- 2020.8.8 剥离站点三线数据信息