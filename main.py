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

# def get_poi(latitude_1, longitude_1, latitude_2, longitude_2, latitude_3, longitude_3, latitude_4, longitude_4, latitude_5, longitude_5, latitude_6, longitude_6, latitude_7, longitude_7):
    # URL Example: https://restapi.amap.com/v5/place/polygon?key=aad49afa17b46e85e060bbe252f25a80&polygon=39.674895561543906,116.08144233426388|39.670846310437035,116.07913898343713|39.66758268717908,116.08184780353079|39.66836807281461,116.08685945650937|39.67241687308992,116.08916302675226|39.675680738540116,116.08645472466954|39.674895561543906,116.08144233426388&types=130000|150000&output=json
    #url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=aad49afa17b46e85e060bbe252f25a80' + '&polygon=' + str(latitude_1).strip() + ',' + str(longitude_1).strip() + '|' + str(latitude_2).strip() + ',' + str(longitude_2).strip() + '|' + str(latitude_3).strip() + ',' + str(longitude_3).strip() + '|' + str(latitude_4).strip() + ',' + str(longitude_4).strip() + '|' + str(latitude_5).strip() + ',' + str(longitude_5).strip() + '|' + str(latitude_6).strip() + ',' + str(longitude_6).strip() + '|' + str(latitude_7).strip() + ',' + str(longitude_7).strip() + '&output=json'
    #  + '&types=130000|150000'
    # try:
    #     returned_result = urllib.request.urlopen(url).read()
    #     returned_result = returned_result.decode()
    #     returned_result = str(returned_result)
    #     return returned_result
    # except:
    #     return '-1'

def get_poi(processeed_position):
    url = 'https://restapi.amap.com/v5/place/polygon?' + 'key=aad49afa17b46e85e060bbe252f25a80' + '&polygon=' + str(processeed_position).strip()
    try:
        returned_result = urllib.request.urlopen(url).read()
        returned_result = returned_result.decode()
        # returned_result = str(returned_result)
        return_data = json.load(returned_result)
        if (str(return_data[status]) == '1'):
            return str(returned_result)
        if (str(return_data[status]) == '0'):
            return '-2' # 未获取到信息
    except:
        return '-1' # 网络错误等

if __name__ == "__main__":
    with open('./station_split_by_h3.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
        
    for police_station_key, value in json_data.items():
        print(police_station_key) # police_station_key 为该派出所的名称，vlaue 为其后的所有键值对
        for hexagon_id_key in value:
            print(hexagon_id_key) # hexagon_id_key 为每个六边形区域的ID
            # print(value[hexagon_id_key]) # hexagon_id_key 为六边形顶点的坐标值的集合，共七个为一组

            #########################################################################
            # Material data example:  [[39.674895561543906, 116.08144233426388], [39.670846310437035, 116.07913898343713], [39.66758268717908, 116.08184780353079], [39.66836807281461, 116.08685945650937], [39.67241687308992, 116.08916302675226], [39.675680738540116, 116.08645472466954], [39.674895561543906, 116.08144233426388]]
            # Processed data example: '39.674895561543906,116.08144233426388|39.670846310437035,116.07913898343713|39.66758268717908,116.08184780353079|39.66836807281461,116.08685945650937|39.67241687308992,116.08916302675226|39.675680738540116,116.08645472466954|39.674895561543906,116.08144233426388'
            #########################################################################
            material_position_data = str(value[hexagon_id_key])
            processeed_position = material_position_data.replace('[[', '').replace(' ', '').replace('],[', '|').replace(']]', '')
            # print(processeed_position)
            print(get_poi(processeed_position))
        # input()

    # print(get_poi('39.674895561543906', '116.08144233426388', '39.670846310437035', '116.07913898343713', '39.66758268717908', '116.08184780353079', '39.66836807281461', '116.08685945650937', '39.67241687308992', '116.08916302675226', '39.675680738540116', '116.08645472466954', '39.674895561543906', '116.08144233426388'))
    # print(get_poi('39.69055146877753', '116.04009980769885', '39.68728671012143', '116.04281378762283', '39.68807339731376', '116.04782980938725', '39.69212463483959', '116.05013258981958', '39.69538963613406', '116.04741912790192', '39.6946031572855', '116.04240236747637', '39.69055146877753', '116.04009980769885'))