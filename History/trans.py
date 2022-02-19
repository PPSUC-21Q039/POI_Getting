import json
INPUT_FILE = 'result_dict_list.json'
with open(INPUT_FILE, 'r', encoding='utf8') as fp:
    json_data = json.load(fp)
    print(json_data)