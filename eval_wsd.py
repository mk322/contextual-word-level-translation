import babelnet as bn
from babelnet import Language, POS
import json
import argparse
import ast



correct_file="xl-wsd-data/correct_trans_zh_en.json"
incorrect_file="xl-wsd-data/wrong_trans_zh_en.json"

sent_file="zh_en_sent.json"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"

with open("source_ids_dict_zh_en.txt", encoding="utf-8") as f:
    s = f.read()
    source_ids_dict = dict(ast.literal_eval(s))

pos_dict = {
    "VERB": POS.VERB,
    "NOUN": POS.NOUN,
    "ADJ": POS.ADJ,
    "ADV": POS.ADV
}

lang_dict = {
    "Chinese": Language.ZH,
    "English": Language.EN
}

def parse_source_dict(words_file):
    with open(words_file) as json_file:
        s_word_dict = json.load(json_file)
    s_lang = lang_dict[source_lang]
    source_ids_dict = {}
    for key in list(s_word_dict.keys()):
        source_word = s_word_dict[key][0]
        pos = pos_dict[s_word_dict[key][1]]
        source_id = []
        for synset in bn.get_synsets(source_word, from_langs=[s_lang], poses=[pos]):
            source_id.append(str(synset.id))
        source_ids_dict[key] = source_id
    with open("source_ids_dict_zh_en.txt", "w") as f:
        f.write(str(source_ids_dict))
    return source_ids_dict

def parse_dict(path):
    with open(path, "r", encoding="utf-8") as f1:
        result_dict = eval(f1.readline())
    top1_dict = {}
    for key in result_dict:
        top1_translations = sorted(result_dict[key], key=lambda key: key[1], reverse=True)
        top1_dict[key] = top1_translations
    return top1_dict

def parse_sense_label_dict(path):
    result_dict = {}
    with open(path, "r", encoding="utf-8") as f1:
        lines = f1.read().splitlines()
        for line in lines:
            parts = line.split(" bn")
            if parts[0] not in result_dict:
                result_dict[parts[0]] = []
            for part in parts[1:]:
                result_dict[parts[0]].append("bn"+part)
    return result_dict

def output_sense_label(top1_dict, source_ids_dict, output_file, target_lang):
    t_lang = lang_dict[target_lang]
    wsd_result = {}
    print("start")
    with open(output_file, "w", buffering=1) as o:
        for key in list(top1_dict.keys()):
            intersection = []
            i = 0
            while ((len(intersection) == 0) and (i < len(top1_dict[key]))):
                prediction = top1_dict[key][i][0]
                source_id = source_ids_dict[key]
                for synset in bn.get_synsets(prediction, from_langs=[t_lang]):
                    if str(synset.id) in source_id:
                        intersection.append(str(synset.id))
                i += 1
            wsd_result[key] = intersection
            #print(intersection)
            s = key
            for label in wsd_result[key]:
                s += f" {label}"
            print(s, file=o)

    print("finish")
if __name__ == "__main__":
    target_lang="English"
    source_lang="Chinese"
    words_file="zh_en_words.json"
    all_sense_path = "all_sense_label.txt"
    all_sense_dict = parse_sense_label_dict(all_sense_path)
    #output_file = f"predicted_wsd_labels_{source_lang}_{target_lang}.txt"
    #source_ids_dict = parse_source_dict(words_file)

    #for model_name in ["gpt-neo", "bloom", "gpt-j"]:
    for model_name in ["bloom", "gpt-j", "gpt-neo"]:
        if model_name == "gpt-neo":
            for model_size in ["2.7B", "1.3B", "125M"]:
                output_file = f"WSD_results/{model_name}/labels2_{source_lang}_{target_lang}_{model_size}.txt"
                result_dict_path = f"WSD_results/{model_name}/output_{source_lang}_{target_lang}_{model_size}_WSD.txt"
                top1_dict = parse_dict(result_dict_path)
                output_sense_label(top1_dict, source_ids_dict, output_file, target_lang)

        elif model_name == "bloom":
            for model_size in ["3b", "1b7", "1b1", "560m"]:
            #for model_size in ["1b7", "1b1", "560m",]:
                output_file = f"WSD_results/{model_name}/labels2_{source_lang}_{target_lang}_{model_size}.txt"
                result_dict_path = f"WSD_results/{model_name}/output_{source_lang}_{target_lang}_{model_size}_WSD.txt"
                top1_dict = parse_dict(result_dict_path)
                output_sense_label(top1_dict, source_ids_dict, output_file, target_lang)

        elif model_name == "gpt-j":
            model_size = "6B"
            output_file = f"WSD_results/{model_name}/labels2_{source_lang}_{target_lang}_{model_size}.txt"
            result_dict_path = f"WSD_results/{model_name}/output_{source_lang}_{target_lang}_{model_size}_WSD.txt"
            top1_dict = parse_dict(result_dict_path)
            output_sense_label(top1_dict, source_ids_dict, output_file, target_lang)
    """
