#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import json
import random
import urllib
from requests.api import request

# INPUT_FILE = 'test.json' # 测试用输入文件
INPUT_FILE = './station_split_by_h3.json' # 输入文件
OUTPUT_FILE = './result_dict_list_final.json' # 输出文件

PAGE_SIZE = 24 # 全局 page_size, 用于规定每页显示的数量

# User Key
# 以下五个为孟昊阳所有
USER_KEY_1 = 'aad49afa17b46e85e060bbe252f25a80'
USER_KEY_2 = '677d0126e70c3b35671c08a59ea52d78'
USER_KEY_3 = '615e912ab6aa668d068a32fd6ce01ff3'
USER_KEY_4 = '6b70e5ffb62e110b02b25d8904ee4a9d'
USER_KEY_5 = '9f00e38285dc77b127c98e1a128af2be'
# 以下五个为胡文强所有
USER_KEY_6 = 'ebd9973f5dfce59e6dc2972dac0f4e39'
USER_KEY_7 = '241153183e1f4ee347fdfadf9426174e'
USER_KEY_8 = '818b3586534a2ae2c95baa0c371f483e'
USER_KEY_9 = '65b7b13fbc79f8fd98fda675de28261e'
USER_KEY_10 = '2709fc90cb839fd90dd020034a5f1db7'


def user_key():
    USER_KEY_LIST = [USER_KEY_1, USER_KEY_2, USER_KEY_3, USER_KEY_4, USER_KEY_5, USER_KEY_6, USER_KEY_7, USER_KEY_8, USER_KEY_9, USER_KEY_10]
    return random.choice(USER_KEY_LIST)


def get_poi(page,processeed_position, result_types):
    try:
        # Url Example: https://restapi.amap.com/v5/place/polygon?key=aad49afa17b46e85e060bbe252f25a80&polygon=地址&types=类型代码&page_size=每页的页数
        url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=' + str(user_key()).strip() + '&polygon=' + str(processeed_position).strip() + '&types=' + str(result_types).strip() + '&page_size=' + str(PAGE_SIZE) + '&page_num=' + str(page).strip()
        response = urllib.request.urlopen(url)
        returned_data = json.load(response)

        if (returned_data["status"] == '1'):
            if (returned_data["count"] == '0'):
                return ['0', '', ''] # 单纯没查到而已
            return ('1', returned_data["count"], returned_data["pois"]) # 返回获取到 POI 信息
        if (returned_data["status"] == '0'):
            return ['-1', '', ''] # 查询失败, -1: Error: 查询状态有误!
    except:
        print ("Error: get_poi() 访问 API 失败!")
        return ['-2', '', '']


def get_location(returned_information_format, input_longtitude, input_latitude):
    # Url example: https://restapi.amap.com/v3/geocode/regeo?output=xml&location=116.310003,39.991957&key=用户的key&radius=1000&extensions=类型 (all/base)
    if (str(input_longtitude).strip() != 'NaN' and str(input_latitude).strip() != 'NaN'):
        url = 'https://restapi.amap.com/v3/geocode/regeo?output=' + str(returned_information_format).strip() + 'xml&location=' + str(input_longtitude).strip() + ',' + str(input_latitude).strip() + '&key=' + str(user_key()).strip() + '&radius=1000' + '&extensions=base'
        try:
            response = urllib.request.urlopen(url)
            returned_data = json.load(response)
            return returned_data["regeocode"]["formatted_address"]
        except:
            print ("Error: get_location() 访问 API 失败!")
            return 'Error: 查询状态有误!'
    else:
        return 'Error: 输入有误!'


if __name__ == "__main__":
    start_time = time.time()
    try:
        with open(INPUT_FILE, 'r', encoding = 'utf8') as fp: # 目前为调试用
            json_data = json.load(fp)
    except:
        print ('打开文件' + INPUT_FILE + '错误!')
        quit()

    # 初始化各项统计数据
    police_station_quantity = 0 # 派出所数量
    search_success = 0 # 搜索到的数量
    search_fail = 0 # 未搜索到的数量
    search_error = 0 # 发生错误的数量

    result_dict = {} # 结果

    for police_station_key, value in json_data.items(): # police_station_key 为该派出所的名称，vlaue 为其后的所有键值对
        print(police_station_quantity + 1, ': 正在处理:', police_station_key)
        result_dict [police_station_key] = {} # 以派出所名称为 Dict 的第一个 Key
        # result_list [police_station_key] = {} # 以派出所名称为 List 的第一个元素
        police_station_quantity = police_station_quantity + 1

        for hexagon_id_key in value: # hexagon_id_key 为每个六边形区域的ID
            print ('  ', hexagon_id_key)
            result_dict [police_station_key] [hexagon_id_key] = [] # 以这个为名的列表
            material_position_data = str(value[hexagon_id_key]) # value[hexagon_id_key] 为六边形顶点的坐标值的集合，共七个

            # 处理得到适合 get_poi() 函数输入的坐标值
            processed_position = material_position_data.replace('[[', '').replace(' ', '').replace('],[', '|').replace(']]', '')
            splitted_position = str(processed_position).split('|')
            result_position = ''
            hex_len=len(splitted_position)
            for i in range (0,hex_len):
                material_splitted_pairs = splitted_position[i].split(',')
                pocessed_splitted_pairs = str(material_splitted_pairs[1]).strip()[0:10] + ',' + str(material_splitted_pairs[0]).strip()[0:9] # 完成字符串顺序的调换 (经度 + 纬度) 并截断
                result_position = result_position + str(pocessed_splitted_pairs).strip() + '|'
            result_position = result_position[:-1] # 删掉多余的 |

            # 计算六边形的中心点坐标
            center_position_longtitude = 0 # 经度
            center_position_latitude = 0 # 纬度
            for i in range (0,hex_len): # 注意只求前六个的和
                material_splitted_pairs = splitted_position[i].split(',')
                center_position_longtitude = center_position_longtitude + float(str(material_splitted_pairs[1]).strip()[0:10])
                center_position_latitude = center_position_latitude + float(str(material_splitted_pairs[0]).strip()[0:9])
            center_position_longtitude = center_position_longtitude / hex_len # 经度
            center_position_latitude = center_position_latitude / hex_len # 纬度

            for page_index in range(100):
                [returned_poi_status, returned_poi_info_count, returned_poi_info_details] = get_poi(page_index+1,result_position, '130000|150000') # Search Types 为：政府机构及社会团体 (130000) 与 交通设施服务 (150000)，用 '|' 分隔

                result_dict [police_station_key] [hexagon_id_key] = {"count": returned_poi_info_count, "center_point": {"center_position_longtitude": center_position_longtitude, "center_position_latitude": center_position_latitude, "center_location": get_location("json", center_position_longtitude, center_position_latitude)}, "政府机构及社会团体": [], "交通设施服务": []} # 初始化第三层

                print ('        Count:', returned_poi_info_count) # 输出本次查询到的 POI 个数
                
                if (returned_poi_status == '1'): # '0': 'Error: 未搜索到结果!', '-1': 'Error: 查询状态有误! 请检查用户 Key 是否合法!', '-2': '网络错误'（在 try 里面添加）
                    search_success = search_success + 1
                    result_count = 0
                    while int(result_count) < int(returned_poi_info_count):
                        returned_poi_info_dict = returned_poi_info_details[result_count] # 此时已经转为 dict 类型的数据

                        # 以下为返回信息中各个值的提取
                        returned_poi_name = returned_poi_info_dict["name"]
                        returned_poi_id = returned_poi_info_dict["id"]
                        returned_poi_location = returned_poi_info_dict["location"]
                        returned_poi_type = returned_poi_info_dict["type"]
                        returned_poi_typecode = returned_poi_info_dict["typecode"]

                        if (returned_poi_typecode[0:2] == '13'):
                            result_dict [police_station_key] [hexagon_id_key] ["政府机构及社会团体"].append ({"name": returned_poi_name, "id": returned_poi_id, "type": returned_poi_type, "typecode": returned_poi_typecode, "location": returned_poi_location})
                        elif (returned_poi_typecode[0:2] == '15'):
                            result_dict [police_station_key] [hexagon_id_key] ["交通设施服务"].append ({"name": returned_poi_name, "id": returned_poi_id, "type": returned_poi_type, "typecode": returned_poi_typecode, "location": returned_poi_location})
                        result_count = result_count + 1
                        # print (result_dict)

                elif (returned_poi_status == '0'):
                    # print ('Error: 未搜索到结果!')
                    result_dict [police_station_key] [hexagon_id_key] [0] = '0' # 第 0 个就是 count 所处的位置
                    search_fail = search_fail + 1
                elif (returned_poi_status == '-1'):
                    print ('Error: 查询状态有误! 请检查用户 Key 是否合法!')
                    search_error = search_error + 1
                    
                if returned_poi_info_count == " " or returned_poi_info_count == "":
                    poi_count = 0
                else:
                    poi_count = int(returned_poi_info_count)
                    print ("第" + str(page_index) + "页")
                if poi_count < PAGE_SIZE:
                    break
            # time.sleep(1000) # 休眠 1000 ms

    # 写入字典
    json_str = json.dumps(result_dict)
    with open(OUTPUT_FILE, 'w') as json_file:
        json_file.write(json_str)
    end_time = time.time()
    print ('程序运行花费:', end_time - start_time, '共处理派出所数量:', police_station_quantity, ', 处理区块数量:', search_success + search_fail + search_error, ', 其中搜索到了:', search_success, ', 未搜索到:', search_fail, ', 发生错误:', search_error, ', 输出文件已写入到当前目录下的' + OUTPUT_FILE + '中')


# In[ ]:
