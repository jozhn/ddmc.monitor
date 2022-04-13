# 基本配置
bark_id = ''  # bark app通知id
duration = 10  # 执行间隔时间秒
run_type = 2  # 监控类型 1首页监控(已经失效) 2购物车监控

# 首页get参数
key_word = '当前运力紧张，今天各时段已约满，敬请谅解'
station_id = ''  # 站点id

# 购物车post参数
ua = ''
cookie = 'DDXQSESSID=XXXXX'  # 账号cookie 类似:DDXQSESSID=XXXXX
city_number = '0101'  # ddmc-city-number 0101上海
device_id = ''  # ddmc-device-id
longitude = '121.43676'  # ddmc-longitude 上海的经度
latitude = '31.188311'  # ddmc-latitude 上海的纬度
uid = ''  # ddmc-uid
api_version = '9.49.2'  # ddmc-api-version
build_version = '2.82.0'    # ddmc-build-version
raw_body = ''

name_of_all_categories = [
    "预制菜", "蔬菜豆制品", "肉禽蛋", "水产海鲜", "水果鲜花", "叮咚特供", "乳品烘焙", "速食冻品", "粮油调味", "酒水饮料", "火锅到家", "熟食卤味",
    "休闲零食", "日用百货", "方便食品", "营养早餐", "宝妈严选", "轻养星球", "在家烧烤", "云仓快送"
]
name_of_categories_i_care = [
    '预制菜', '蔬菜豆制品', '肉禽蛋', '水产海鲜', '水果鲜花', '叮咚特供', '乳品烘焙', '速食冻品',
    "火锅到家", "熟食卤味", "休闲零食", "日用百货", "方便食品", "营养早餐"
]