import json
INPUT_FILE = 'result_dict_list_final.json'
# OUTPUT_FILE = 'result_dict_list_final.json' 
with open(INPUT_FILE, 'r', encoding='utf8') as fp:
    json_data = json.load(fp)
    print(json_data)
#with open(OUTPUT_FILE, 'w'):
#    json_data.write(json_str)