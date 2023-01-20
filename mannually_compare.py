import json

correct_dict_path = "xl-wsd-data/correct_trans_zh_en_no_under.json"
output_path = "WSD_Results/bloom/output_Chinese_English_3b_WSD.txt"
with open(correct_dict_path, "r") as f:
    correct_dict = json.load(f)

def parse_dict(path):
    with open(path, "r", encoding="utf-8") as f1:
        result_dict = eval(f1.readline())
    top1_dict = {}
    for key in result_dict:
        top1_translations = sorted(result_dict[key], key=lambda key: key[1], reverse=True)
        top1_dict[key] = top1_translations
    return top1_dict

top1_dict = parse_dict(output_path)

count = 0
for key in top1_dict:
    prediction = top1_dict[key][0][0]
    if(prediction in correct_dict[key]):
        count += 1
print(count)
print(count / len(top1_dict))


"""
gold = "xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt"
ans = "WSD_Results/bloom/labels3_Chinese_English_7b1.txt"
gold_dict = {}
ans_dict = {}
with open(gold) as f1:
    for line in f1:
        fields = line.strip().split(" ")
        id, *answers = fields
        gold_dict[id] = set(answers)

with open(ans) as f2:
    for line1 in f2:
        fields = line1.strip().split(" ")
        id1, *answers = fields
        ans_dict[id1] = set(answers)

print(ans_dict)

count = 0
for key in gold_dict:
    if(len(ans_dict[key] & gold_dict[key]) > 0):
        count += 1
print(count)
print(count / len(gold_dict))
"""        



#'d000.s9121.t011': {'bn:00092464v', 'bn:00086417v', 'bn:00086264v', 'bn:00092593v', 'bn:00086418v', 'bn:00083918v', 'bn:00082127v', 'bn:00083377v', 'bn:00084079v'}, 'd000.s9121.t012': {'bn:00093819v', 'bn:00086881v', 'bn:00091463v', 'bn:00086880v', 'bn:00086879v', 'bn:00086794v', 'bn:00085082v'}}