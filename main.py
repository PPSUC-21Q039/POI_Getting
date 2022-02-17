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

USER_KEY = 'aad49afa17b46e85e060bbe252f25a80' # 用户 Key

# 暂时不用 try，不然没法 Ctrl + c 中止
# def get_poi(processeed_position):
#     url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=aad49afa17b46e85e060bbe252f25a80' + '&polygon=' + str(processeed_position).strip()
#     try:
#         returned_result = urllib.request.urlopen(url).read()
#         returned_result = returned_result.decode()
#         # return_data = json.load(str(returned_result))
#         # if (str(return_data[status]) == '1'):
#         #     return str(returned_result) # 返回获取到的信息
#         # if (str(return_data[status]) == '0'):
#         #     return '-2' # 未获取到信息
#         return str(returned_result) # 返回获取到的信息
#     except:
#         return '-1' # 网络错误等

def get_poi(processeed_position, result_types):
    url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=' + USER_KEY.strip() + '&polygon=' + str(processeed_position).strip() + '&types=' + str(result_types).strip()
    response = urllib.request.urlopen(url)
    returned_data = json.load(response)

    if (returned_data['status'] == '1'):
        if (returned_data['count'] == '0'):
            return 'Error: 未搜索到结果!'
        return returned_data['pois'] # 返回获取到 POI 信息
    if (returned_data['status'] == '0'):
        return 'Error: 查询状态有误!' # 未获取到信息
    
def get_center_position(center_position_longtitude, center_position_latitude):

    return

def get_location(returned_information_format, input_longtitude, input_latitude):
    # Url example: https://restapi.amap.com/v3/geocode/regeo?output=xml&location=116.310003,39.991957&key=<用户的key>&radius=1000&extensions=all (all/base)
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
    with open('./station_split_by_h3.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        
    for police_station_key, value in json_data.items(): # police_station_key 为该派出所的名称，vlaue 为其后的所有键值对
        print(police_station_key) 
        for hexagon_id_key in value:
            # print(hexagon_id_key) # hexagon_id_key 为每个六边形区域的ID
            material_position_data = str(value[hexagon_id_key]) # value[hexagon_id_key] 为六边形顶点的坐标值的集合，共七个为一组

            processed_position = material_position_data.replace('[[', '').replace(' ', '').replace('],[', '|').replace(']]', '')
            splitted_position = str(processed_position).split('|')
            # 得到适合 get_poi() 函数输入的坐标值
            result_position = ''
            for i in range (0,7):
                material_splitted_pairs = splitted_position[i].split(',')
                pocessed_splitted_pairs = str(material_splitted_pairs[1]).strip()[0:10] + ',' + str(material_splitted_pairs[0]).strip()[0:9] # 完成字符串顺序的调换：经度 + 纬度 并截断
                result_position = result_position + str(pocessed_splitted_pairs).strip() + '|'
            result_position = result_position[:-1] # 删掉多余的 |

            # 计算六边形的中心点坐标
            center_position_longtitude = 0 # 经度
            center_position_latitude = 0 # 纬度
            for i in range (0,6):
                material_splitted_pairs = splitted_position[i].split(',')
                center_position_longtitude = center_position_longtitude + float(str(material_splitted_pairs[1]).strip()[0:10])
                center_position_latitude = center_position_latitude + float(str(material_splitted_pairs[0]).strip()[0:9])
            center_position_longtitude = center_position_longtitude / 6
            center_position_latitude = center_position_latitude / 6
            # Example: 
            # ID: 8831818741fffff , 坐标: 116.0841505 , 39.671631166666664
            print ('ID:', hexagon_id_key, ', 坐标:', center_position_longtitude, ',', center_position_latitude, ', 地址:', get_location('json', center_position_longtitude, center_position_latitude))
            
            print ()
            print (get_poi(result_position, '130000|150000')) # Search Types 为：政府机构及社会团体 与 交通设施服务，编号分别为 150000 和 130000,用 '|' 分隔
