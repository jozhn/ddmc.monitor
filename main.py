import requests
import time
import config

bark_msg_url = 'https://api.day.app/' + config.bark_id + '/'


# 检查主页公告 无需cookie
def check_home():
    url = 'https://maicai.api.ddxq.mobi/homeApi/newDetails'
    payload = {'station_id': config.station_id}
    r = requests.get(url, params=payload)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        if res['code'] == 0:
            find = r.text.find(config.key_word)
            params = {'group': '叮咚买菜'}
            print(res)
            if find > 0:
                txt = '叮咚买菜有运力啦!!!'
                requests.get(bark_msg_url + txt, params=params)
            else:
                print('还没有运力！', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


# 检查购物车 需要cookie
def check_cart():
    url = 'https://maicai.api.ddxq.mobi/order/getMultiReserveTime'
    headers = {'Cookie': config.cookie,
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded',
               'User-Agent': config.ua,
               'ddmc-api-version': '9.49.1',
               'ddmc-app-client-id': '4',
               'ddmc-build-version': '2.81.4',
               'ddmc-channel': 'applet',
               'ddmc-city-number': config.city_number,
               'ddmc-device-id': config.device_id,
               'ddmc-ip': '',
               'ddmc-latitude': config.latitude,
               'ddmc-longitude': config.longitude,
               'ddmc-os-version': '[object Undefined]',
               'ddmc-station-id': config.station_id,
               'ddmc-uid': config.uid,
               'Accept-Encoding': 'gzip,compress,br,deflate',
               'Referer': 'https://servicewechat.com/wx1e113254eda17715/421/page-frame.html',
               }
    raw = config.raw_body
    r = requests.post(url, headers=headers, data=raw)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        print(res)
        if res['code'] == 0:
            reserve_times = res['data'][0]['time'][0]['times']
            params = {'group': '叮咚买菜'}
            for reserve_time in reserve_times:
                if not reserve_time['fullFlag']:
                    txt = '叮咚买菜可以预约啦!!!最早可预约时间：' + reserve_time['select_msg']
                    requests.get(bark_msg_url + txt, params=params)
                    break
        else:
            print('还没有可预约时间!')


def run():
    while True:
        if config.run_type == 1:
            check_home()
        else:
            check_cart()
        time.sleep(config.duration)


if __name__ == '__main__':
    run()
