import json
import argparse
import ast


correct_file="xl-wsd-data/correct_trans_zh_en.json"
incorrect_file="xl-wsd-data/wrong_trans_zh_en.json"

sent_file="zh_en_sent.json"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"


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

def output_sense_label(top1_dict, source_ids_dict, all_sense_dict, output_file):
    wsd_result = {}
    print("start")
    with open(output_file, "w", buffering=1) as o:
        for key in list(top1_dict.keys()):
            intersection = []
            i = 0
            while ((len(intersection) == 0) and (i < len(top1_dict[key]))):
                prediction = top1_dict[key][i][0]
                source_id = source_ids_dict[key]
                for sense_label in all_sense_dict[prediction]:
                    if sense_label in source_id:
                        intersection.append(sense_label)
                i += 1
            wsd_result[key] = intersection
            s = key
            for label in wsd_result[key]:
                s += f" {label}"
            print(s, file=o)

    print("finish")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lemma_file", type=str, required=True)
    parser.add_argument("--words_file", type=str, required=True)
    parser.add_argument("--invent_file", type=str)
    parser.add_argument("--all_sense_path", type=str, required=True)
    parser.add_argument("--source_ids_dict_path", type=str)
    parser.add_argument("--output_file", type=str)
    parser.add_argument("--result_dict_path", type=str)

    args = parser.parse_args()
    lemma_file = args.lemma_file 
    words_file = args.words_file
    all_sense_path = args.all_sense_path
    invent_file = args.invent_file
    all_sense_dict = parse_sense_label_dict(args.all_sense_path)

    with open(args.source_ids_dict_path, encoding="utf-8") as f:
        s = f.read()
        source_ids_dict = dict(ast.literal_eval(s))
    top1_dict = parse_dict(args.result_dict_path)
    output_sense_label(top1_dict, source_ids_dict, all_sense_dict, args.output_file)