#########################################################################
# File Name: main.py
# Author: Wenqiang Hu
# mail: huwenqiang.hwq@protonmail.com
# Created Time: Wed Feb 16 14:06:31 2022
#########################################################################

# 高德 Key：aad49afa17b46e85e060bbe252f25a80

import urllib
import json
from requests.api import request

def get_poi(processeed_position):
    url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=aad49afa17b46e85e060bbe252f25a80' + '&polygon=' + str(processeed_position).strip()
    try:
        returned_result = urllib.request.urlopen(url).read()
        returned_result = returned_result.decode()
        # return_data = json.load(str(returned_result))
        # if (str(return_data[status]) == '1'):
        #     return str(returned_result) # 返回获取到的信息
        # if (str(return_data[status]) == '0'):
        #     return '-2' # 未获取到信息
        return str(returned_result) # 返回获取到的信息
    except:
        return '-1' # 网络错误等

if __name__ == "__main__":
    with open('./station_split_by_h3.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        
    # for police_station_key, value in json_data.items(): # police_station_key 为该派出所的名称，vlaue 为其后的所有键值对
    #     print(police_station_key) 
    #     for hexagon_id_key in value:
    #         print(hexagon_id_key) # hexagon_id_key 为每个六边形区域的ID
    #         material_position_data = str(value[hexagon_id_key]) # value[hexagon_id_key] 为六边形顶点的坐标值的集合，共七个为一组
    #         processeed_position = material_position_data.replace('[[', '').replace(' ', '').replace('],[', '|').replace(']]', '')
    #         print(get_poi(processeed_position))

    # print(get_poi('39.626978,116.081571|39.623717,116.084278|39.624504,116.089285|39.628551,116.091587|39.631813,116.088881|39.631026,116.083873|39.6269787,116.081571')) # 小数位数六位！！！！！！
    print(get_poi('116.081571,39.626978|116.084278,39.623717|116.089285,39.624504|116.091587,39.628551|116.088881,39.631813|116.083873,39.631026|116.081571,39.6269787')) # 小数位数六位！！！！！！ & 先经度后纬度！！！！