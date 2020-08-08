from collections import namedtuple


# 站点三线水位 [站名， 设防水位， 警戒水位， 保证水位]
WaterLevel = namedtuple('WaterLevel', ['name', 'shefang', 'jingjie', 'baozheng'])

yongDingDaWei = WaterLevel(name='永定大圩', shefang=11.5, jingjie=13.2, baozheng=14.5)
heiShaZhouAndTianRanZhou = WaterLevel(name='黑沙洲、天然洲', shefang=11.0, jingjie=13.0, baozheng=13.5)
wuWeiDaDi = WaterLevel(name='无为大堤', shefang=11.5, jingjie=13.2, baozheng=15.84)
