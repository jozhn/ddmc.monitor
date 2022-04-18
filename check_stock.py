import json
import os
import time

import requests
import config


def send_msg_bark(msg):
    bark_msg_url = 'https://api.day.app/' + config.bark_id + '/'
    params = {'group': '叮咚买菜'}
    requests.get(bark_msg_url + msg, params=params)


# 通过 station_id 获取所有分类 id
def get_categories():
    cate_url = "https://maicai.api.ddxq.mobi/homeApi/newCategories"
    headers = {'User-Agent': config.ua,
               }
    payload = {'api_version': '9.49.1',
               'station_id': config.station_id,
               }
    r = requests.get(cate_url, params=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        with open("all_categories.json", 'w') as json_obj:
            json.dump(res, json_obj, ensure_ascii=False)
            json_obj.close()
        return


# 生成所有大分类和子分类的标准 json 格式文件
def extract_categories():
    get_categories()
    f = open("all_categories.json")
    all_categories = json.loads(f.read())
    formatted_categories = {'top_categories': []}
    for top_category in all_categories['data']['cate']:
        data = {
            'name': top_category['name'],
            'top_category_id': top_category['id'],
            'category_image_url': top_category['category_image_url'],
            'sub_categories': []
        }
        for sub_category in top_category['cate']:
            sub_data = {
                'name': sub_category['name'],
                'sub_category_id': sub_category['id']
            }
            data['sub_categories'].append(sub_data)
        formatted_categories['top_categories'].append(data)
    with open("all_categories_formatted.json", 'w', encoding='utf8') as json_file:
        json.dump(formatted_categories, json_file, ensure_ascii=False)
    f.close()


# 通过经纬度获取站点名称
def get_station_name(longitude, latitude):
    url = "https://sunquan.api.ddxq.mobi/api/v2/user/location/refresh/"
    headers = {
        'User-Agent': config.ua,
    }
    payload = {
        "longitude": longitude,
        "latitude": latitude,
    }
    r = requests.get(url, headers=headers, params=payload)
    res = r.json()
    return res['data']['station_info']['name']


# 获取每个子分类的现有库存
def get_menu_with_category_id(category_id):
    cate_detail_url = "https://maicai.api.ddxq.mobi/homeApi/categoriesNewDetail/"
    headers = {
        'User-Agent': config.ua,
    }
    payload = {
        'city-number': config.city_number,
        'station-id': config.station_id,
        "category_id": category_id,
        "version_control": "new"
    }

    r = requests.get(cate_detail_url, headers=headers, params=payload)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        menu = {'sub_category_name': res['data']['category_name'], 'products': []}
        if 'cate' in res['data']:
            foods = []
            for sub_category in res['data']['cate']:
                if sub_category['id'] != "stock_no":
                    # print("\t" + sub_category['name'])
                    for product in sub_category['products']:
                        foods.append(product['name'])
                menu['products'] = foods
        return menu


def check_stock():
    if not os.path.exists("all_categories_formatted.json"):
        extract_categories()
    flag = False
    msg = ""
    with open("all_categories_formatted.json", encoding='utf-8') as f:
        flag = False
        all_categories = json.load(f)

        for top_category in all_categories["top_categories"]:
            all_submenu = []
            if top_category['name'] in config.name_of_categories_i_care:

                for sub_category in top_category["sub_categories"]:
                    menu = get_menu_with_category_id(sub_category['sub_category_id'])
                    if len(menu['products']) > 0:
                        all_submenu.append(menu)
                count = 0
                for menu in all_submenu:
                    count += len(menu['products'])
                if count > 0:
                    flag = True
                    print("|------" + get_station_name(config.longitude, config.latitude))
                    print("|-" + top_category['name'])
                    msg += top_category['name'] + ", "
                    print("| |")
                    for menu in all_submenu:
                        if len(menu['products']) > 0:
                            print("| |-" + sub_category['name'] + ": " + str(len(menu['products'])))
                            for product in menu['products']:
                                print("| |  |-" + product)
    if flag:
        msg = "有菜啦！" + msg
        print(msg)
        send_msg_bark(msg)
    else:
        print(
            "|------"
            + get_station_name(config.longitude, config.latitude) + " "
            + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            + "没有菜哦！"
        )
