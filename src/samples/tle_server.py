# -*- coding: utf-8 -*-

import requests
import sys
import time
from flask import Flask, jsonify

from tle import TLE


app = Flask(__name__)


# user name (email address)
username = sys.argv[1]
# password
password = sys.argv[2]
# NORAD の衛星カタログ番号
"""
- 29479: ひので
- 25544: ISS?
"""
satelite_nums = ["123", "124", "125", "25544", "29479", "123456789"]

login_data = {'identity': username, 'password': password}
base_url = 'https://www.space-track.org/'
login_url = base_url + 'ajaxauth/login'

# TLE を更新する（Space-Track から取得し直す）周期
# 単位は秒
tle_get_period_sec = 30

tles = []
tle_get_time = 0


@app.route('/')
def return_tle():
    global tle_get_time, tles
    time_now = time.time()
    if time_now - tle_get_time > tle_get_period_sec:
        tles = update_tles()
        tle_get_time = time_now

    # tmp
    print tle_get_time
    return jsonify(ResultSet=tles)


def update_tles():

    s = requests.Session()
    # Space-Track にログイン
    s.post(login_url, data=login_data)
    # TLE を取得
    res = s.get(base_url + "basicspacedata/query/class/tle_latest/ORDINAL/1/NORAD_CAT_ID/{0}/orderby/TLE_LINE1 ASC/format/json".format(",".join(satelite_nums))).json()
    return res


if __name__ == '__main__':
    #global tles, tle_get_time, satelite_nums

    tles = update_tles()
    tle_get_time = time.time()

    # Space-Track からのレスポンスに含まれない番号は除去
    satelite_nums = map(lambda elem: elem["NORAD_CAT_ID"], tles)

    print tle_get_time

    app.run(debug=True)


"""
if __name__ == '__main__':
    res = get_tle()
    
    # get parameters from response JSON
    object_name = res["OBJECT_NAME"]
    object_type = res["OBJECT_TYPE"]
    epoch = res["EPOCH"]  # 元期
    e = res["ECCENTRICITY"]  # 楕円軌道の離心率
    mean_motion = res["MEAN_MOTION"]  # 平均運動
    # 平均運動変化係数
    mean_anomaly = res["MEAN_ANOMALY"]  # 平均近点角
    inclination = res["INCLINATION"]  # 軌道傾斜角
# 近地点引数
    right_ascension_of_asc_node = res["RA_OF_ASC_NODE"]  # 昇交点赤経
"""
