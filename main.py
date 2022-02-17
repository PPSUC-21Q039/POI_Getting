#########################################################################
# File Name: main.py
# Author: Wenqiang Hu
# mail: huwenqiang.hwq@protonmail.com
# Created Time: Wed Feb 16 14:06:31 2022
#########################################################################

import json
import urllib
from requests.api import request

USER_KEY = 'aad49afa17b46e85e060bbe252f25a80' # 用户 Key 

def get_poi(processeed_position, result_types): # 完成前记得添加 try，其中 except 的返回值是 -2
    # Url Example: https://restapi.amap.com/v5/place/polygon?key=aad49afa17b46e85e060bbe252f25a80&polygon=地址&types=类型代码
    url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=' + USER_KEY.strip() + '&polygon=' + str(processeed_position).strip() + '&types=' + str(result_types).strip()
    response = urllib.request.urlopen(url)
    returned_data = json.load(response)

    if (returned_data["status"] == '1'):
        if (returned_data["count"] == '0'):
            return ['0', '', ''] # 单纯没查到而已
        return ('1', returned_data["count"], returned_data["pois"]) # 返回获取到 POI 信息
    if (returned_data["status"] == '0'):
        return ['-1', '', ''] # 查询失败, -1: Error: 查询状态有误!

def get_location(returned_information_format, input_longtitude, input_latitude):
    # Url example: https://restapi.amap.com/v3/geocode/regeo?output=xml&location=116.310003,39.991957&key=用户的key&radius=1000&extensions=类型 (all/base)
    if (str(input_longtitude).strip() != 'NaN' and str(input_latitude).strip() != 'NaN'):
        url = 'https://restapi.amap.com/v3/geocode/regeo?output=' + str(returned_information_format).strip() + 'xml&location=' + str(input_longtitude).strip() + ',' + str(input_latitude).strip() + '&key=' + USER_KEY.strip() + '&radius=1000' + '&extensions=base'
        try:
            response = urllib.request.urlopen(url)
            returned_data = json.load(response)
            return returned_data["regeocode"]["formatted_address"]
        except:
            return 'Error: 查询状态有误!'
    else:
        return 'Error: 输入有误!'

if __name__ == "__main__":
    try:
        with open('./station_split_by_h3.json', 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
    except:
        print ('打开文件 (station_split_by_h3.json) 错误!')
        quit()
    # 统计数据
    police_station_quantity = 0 # 派出所数量
    search_success = 0 # 搜索到的数量
    search_fail = 0 # 未搜到的数量
    search_error = 0 # 发生错误的数量

    for police_station_key, value in json_data.items(): # police_station_key 为该派出所的名称，vlaue 为其后的所有键值对
        print(police_station_key) 
        police_station_quantity = police_station_quantity + 1
        for hexagon_id_key in value: # hexagon_id_key 为每个六边形区域的ID
            material_position_data = str(value[hexagon_id_key]) # value[hexagon_id_key] 为六边形顶点的坐标值的集合，共七个

            # 处理得到适合 get_poi() 函数输入的坐标值
            processed_position = material_position_data.replace('[[', '').replace(' ', '').replace('],[', '|').replace(']]', '')
            splitted_position = str(processed_position).split('|')
            result_position = ''
            for i in range (0,7):
                material_splitted_pairs = splitted_position[i].split(',')
                pocessed_splitted_pairs = str(material_splitted_pairs[1]).strip()[0:10] + ',' + str(material_splitted_pairs[0]).strip()[0:9] # 完成字符串顺序的调换 (经度 + 纬度) 并截断
                result_position = result_position + str(pocessed_splitted_pairs).strip() + '|'
            result_position = result_position[:-1] # 删掉多余的 |

            # 计算六边形的中心点坐标
            center_position_longtitude = 0 # 经度
            center_position_latitude = 0 # 纬度
            for i in range (0,6): # 注意只求前六个的和
                material_splitted_pairs = splitted_position[i].split(',')
                center_position_longtitude = center_position_longtitude + float(str(material_splitted_pairs[1]).strip()[0:10])
                center_position_latitude = center_position_latitude + float(str(material_splitted_pairs[0]).strip()[0:9])
            center_position_longtitude = center_position_longtitude / 6 # 经度
            center_position_latitude = center_position_latitude / 6 # 纬度
            
            # Output Example: 
            # ID: 8831818741fffff , 坐标: 116.0841505 , 39.671631166666664 , 地址: 北京市房山区窦店镇G4京港澳高速
            print ('ID:', hexagon_id_key, ', 坐标:', center_position_longtitude, ',', center_position_latitude, ', 地址:', get_location('json', center_position_longtitude, center_position_latitude))
            [get_poi_status, get_poi_info_count, get_poi_info_details] = get_poi(result_position, '130000|150000') # Search Types 为：政府机构及社会团体 (150000) 与 交通设施服务 (130000)，用 '|' 分隔

            if (get_poi_status == '1'): # '0': 'Error: 未搜索到结果!' '-1': 'Error: 查询状态有误! 请检查用户 Key 是否合法!' '-2': '网络错误'（在 try 里面添加）
                print (get_poi_info_count) 
                print (get_poi_info_details)
                search_success = search_success +1 
            elif (get_poi_status == '0'):
                print ('Error: 未搜索到结果!')
                search_fail = search_fail + 1
            elif (get_poi_status == '-1'):
                print ('Error: 查询状态有误! 请检查用户 Key 是否合法!')
                search_error = search_error + 1
               
