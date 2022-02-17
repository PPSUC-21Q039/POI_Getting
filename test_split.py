processed_position = '39.674895561543906,116.08144233426388|39.670846310437035,116.07913898343713|39.66758268717908,116.08184780353079|39.66836807281461,116.08685945650937|39.67241687308992,116.08916302675226|39.675680738540116,116.08645472466954|39.674895561543906,116.08144233426388'
splitted_position = str(processed_position).split('|')
result_position = ''
#for splitted_pairs in splitted_position:
for i in range(0,7):
    material_splitted_pairs = splitted_position[i].split(',')
    pocessed_splitted_pairs = str(material_splitted_pairs[1]).strip()[0:10] + ',' + str(material_splitted_pairs[0]).strip()[0:9]
    print (pocessed_splitted_pairs)
    result_position = result_position + str(pocessed_splitted_pairs).strip() + '|'
    
print(result_position[:-1])