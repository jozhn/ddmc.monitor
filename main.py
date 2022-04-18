import requests
import time
import sys
import config
from check_stock import check_stock, send_msg_bark


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
            print(r.text)
            if find > 0:
                print('还没有运力！', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            else:
                txt = '叮咚买菜有运力啦!!!'
                send_msg_bark(txt)
    else:
        print('请求异常', r.text)


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
            all_full = True
            for reserve_time in reserve_times:
                all_full = all_full and reserve_time['fullFlag']
            if not all_full:
                txt = '叮咚买菜可以预约啦!!!最早可预约时间：' + reserve_time['select_msg']
                send_msg_bark(txt)
            else:
                print('还没有可预约时间!')
        else:
            print('请求异常!')
    else:
        print('请求异常', r.text)


def run():
    while True:
        if config.run_type == 1:
            check_home()
        elif config.run_type == 2:
            check_cart()
        else:
            check_stock()
        time.sleep(config.duration)


if __name__ == '__main__':
    # 给在服务器后台执行使用
    if len(sys.argv) > 1:
        run_type = int(sys.argv[1])
        if run_type in [1, 2, 3]:
            config.run_type = run_type
    run()
