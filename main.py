import requests
import time
import config

bark_msg_url = 'https://api.day.app/' + config.bark_id + '/'


# 检查主页公告 无需cookie
def check_home():
    url = 'https://maicai.api.ddxq.mobi/homeApi/newDetails'
    headers = {'User-Agent': config.ua,
               }
    payload = {'api_version': '9.49.1',
               'station_id': config.station_id,
               }
    r = requests.get(url, params=payload, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        res = r.json()
        if res['code'] == 0:
            find = r.text.find(config.key_word)
            params = {'group': '叮咚买菜'}
            print(r.text)
            if find > 0:
                print('还没有运力！', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                txt = '叮咚买菜有运力啦!!!'
                requests.get(bark_msg_url + txt, params=params)


# 检查购物车 需要cookie
def check_cart():
    url = 'https://maicai.api.ddxq.mobi/order/getMultiReserveTime'
    headers = { 'Connection': 'keep-alive',
                'Content-Length': '2215',
                'content-type': 'application/x-www-form-urlencoded',
                'ddmc-city-number': config.city_number,
                'ddmc-build-version': config.build_version,
                'ddmc-device-id': config.device_id,
                'ddmc-station-id': config.station_id,
                'ddmc-channel': 'applet',
                'ddmc-os-version': '[object Undefined]',
                'ddmc-app-client-id': '4',
                'Cookie': config.cookie,
                'ddmc-ip': '',
                'ddmc-longitude': config.longitude,
                'ddmc-latitude': config.latitude,
                'ddmc-api-version': config.api_version,
                'ddmc-uid': config.uid,
                'Accept-Encoding': 'gzip,compress,br,deflate',
                'User-Agent': config.ua,
                'Referer': 'https://servicewechat.com/wx1e113254eda17715/422/page-frame.html',
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
            all_full = True
            for reserve_time in reserve_times:
                all_full = all_full and reserve_time['fullFlag']
            if not all_full:
                txt = '叮咚买菜可以预约啦!!!最早可预约时间：' + reserve_time['select_msg']
                requests.get(bark_msg_url + txt, params=params)
            else:
                print('还没有可预约时间!')
        else:
            print('请求异常!')


def run():
    while True:
        if config.run_type == 1:
            check_home()
        else:
            check_cart()
        time.sleep(config.duration)


if __name__ == '__main__':
    run()
