# ddmc.monitor
叮咚买菜运力监控，站点库存监控。监控叮咚站点首页信息购物车预约时间信息及站点库存存在日间随机更新的情况，通过Bark app通知到手机。

## 使用说明

### 抓包

首先需要自己使用Fiddler等工具对叮咚买菜小程序抓包（PC小程序比较方便），获取`config.py`中需要的参数。

### 运行

本脚本提供了三种监控方式，修改 run_type 切换：

1. **站点首页关键字监控**(免登陆，不会封号但可能封ip，默认使用)
    - 抓包获取站点id，填写**station_id**即可
    - 关键词不存在时则提醒(关键词为`由于近期疫情问题，配送运力紧张，本站点当前运力已约满`)
    - 可能相比购物车有延迟
2. **购物车预约时间监控**(需要登录，有封号风险，谨慎使用)
    - 需要填写UA等信息作为header
    - 然后`raw_body`填Fiddler里面请求信息的Raw tab最下面的一串url格式的字符串(类似`uid=xxx&longitude=xxx`，购物车点结算-预约时间就有了)
3. **自己站点菜品库存和更新提醒**
    - 需要填写 **station_id，longitude, latitude**
    - 可以自己从 name_of_all_categories 中挑选并添加或修改自己关心的分类的菜品到 name_of_categories_i_care 中。

执行main.py即可

## 依赖
- python3
- requests

## 声明

仅供学习交流使用，请勿用于非法用途。
