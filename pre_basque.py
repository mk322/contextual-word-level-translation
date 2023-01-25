import json
correct_path = "xl-wsd-files/Basque/correct_trans_eu_en.json"
incorrect_path = "xl-wsd-files/Basque/wrong_trans_eu_en.json"

with open(correct_path, "r") as f:
    dict_correct = json.load(f)

with open(incorrect_path, "r") as f:
    dict_incorrect = json.load(f)

dict_correct_u = {}

dict_incorrect_u = {}
for key in dict_correct:
    dict_correct_u[key] = []
    for word in dict_correct[key]:
        dict_correct_u[key].append(word + " gisa itzultzen da")

for key in dict_incorrect:
    dict_incorrect_u[key] = []
    for word in dict_incorrect[key]:
        dict_incorrect_u[key].append(word + " gisa itzultzen da")

with open("xl-wsd-files/Basque/correct_trans_eu_en_f.json", "w") as f:
    json.dump(dict_correct_u, f)

with open("xl-wsd-files/Basque/wrong_trans_eu_en_f.json", "w") as f:
    json.dump(dict_incorrect_u, f)