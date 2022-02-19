#########################################################################
# File Name: main.py
# Author: Wenqiang Hu
# mail: huwenqiang.hwq@protonmail.com
# Created Time: Wed Feb 16 14:06:31 2022
#########################################################################

#########################################################################
# To do:
# 增加代理池

import time
import json
import random
import urllib
from requests.api import request

if __name__ == "__main__":
    start_time = time.time()
    try:
        with open('./station_split_by_h3.json', 'r', encoding='utf8') as fp:
        # with open('./test.json', 'r', encoding='utf8') as fp: # 目前为调试用
            json_data = json.load(fp)
    except:
        print ('打开文件 (station_split_by_h3.json) 错误!')
        quit()

    # 统计数据
    police_station_quantity = 0 # 派出所数量
    ALL = 0

    for police_station_key, value in json_data.items(): # police_station_key 为该派出所的名称，vlaue 为其后的所有键值对
        print('正在处理:', police_station_key) 
        police_station_quantity = police_station_quantity + 1

        for hexagon_id_key in value: # hexagon_id_key 为每个六边形区域的ID
            ALL = ALL + 1
    end_time = time.time()
    print ('程序运行花费:', end_time - start_time, '共处理派出所数量:', police_station_quantity, ', 处理区块数量:', ALL)
