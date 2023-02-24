import json
source_lang = "French"
lang = "fr"
tlang = "en"
word2label = {}

def sanity_check(source_lang, lang, tlang):
    correct_file = f"xl-wsd-files/{source_lang}/correct_trans_{lang}_{tlang}.json"
    incorrect_file = f"xl-wsd-files/{source_lang}/wrong_trans_{lang}_{tlang}.json"
    lemma_file = f"xl-wsd-files/{source_lang}/{lang}_{tlang}_lemma.json"
    invent_file = f"xl-wsd-data/inventories/inventory.{lang}.txt"
    key_file = f"xl-wsd-data/evaluation_datasets/test-{lang}/test-{lang}.gold.key.txt"
    with open(correct_file, "r") as f:
        correct_dict = json.load(f)

    with open(incorrect_file, "r") as f:
        incorrect_dict = json.load(f)

    with open(lemma_file, "r") as f:
        lemma_dict = json.load(f)

    with open(invent_file , "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split("\t")
            word = parts[0].split("#")[0]
            pos_ = str(parts[0].split("#")[1])
            for label in parts[1:]:
                if label.endswith("\n"):
                    label = label[:-1]
                if (word, pos_) not in word2label:
                    word2label[(word, pos_)] = [str(label)]
                else:
                    word2label[(word, pos_)].append(str(label))

    key_dict = {}
    with open(key_file , "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            parts = line.split(" ")
            key = parts[0]
            labels = []
            for label in parts[1:]:
                labels.append(label)
            key_dict[key] = labels

    num_no_wrong_tran_spec = 0
    num_no_wrong_trans = 0
    num_no_correct_trans = 0
    for key in lemma_dict:
        lemma = lemma_dict[key]
        lemma_tuple = (lemma[0].lower(), lemma[1])
        if key not in correct_dict:
            num_no_correct_trans += 1
        else:
            if set(word2label[lemma_tuple]) != set(key_dict[key]):
                if key not in incorrect_dict:
                    num_no_wrong_trans += 1
                    num_no_wrong_tran_spec += 1
                    #if all(x in correct_dict[key] for x in incorrect_dict[key]):
                elif set(incorrect_dict[key]).issubset(set(correct_dict[key])):
                        num_no_wrong_tran_spec += 1
    with open("sanity_check.txt", "a") as f:
        print("Source Language:", source_lang, "Target Language:", tlang, file=f)
        print("total # examples:", len(lemma_dict), file=f)
        #print("total # examples with only one label:", num_no_wrong_label)
        print("total # examples that have no correct translation:", num_no_correct_trans, file=f)
        print("total # examples that have multiple sense labels but with no wrong translation:", num_no_wrong_trans, file=f)
        print("total # examples that have multiple sense labels but with no unique wrong translation:", num_no_wrong_tran_spec, file=f)
        print(file=f)

target_langs = ["en", "es", "zh"]
source_langs = ["Catalan", "Basque", "German", "French", "Italian"]
langs = ["ca", "eu", "de", "fr", "it"]
for i in range(len(source_langs)) :
    for target_lang in target_langs:
        sanity_check(source_langs[i], langs[i], target_lang)
