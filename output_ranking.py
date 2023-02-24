import json
import argparse
import ast
import numpy as np
import os

#correct_file="xl-wsd-data/correct_trans_zh_en.json"
#incorrect_file="xl-wsd-data/wrong_trans_zh_en.json"

sent_file="zh_en_sent.json"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"


def same_lang_rank(word_dict, eng_dict, zh_dict):
    eng_count = 0
    source_count = 0
    zh_count = 0
    for key in zh_dict:
        #tran_top1 = -np.inf
        #zh_top1 = -np.inf
        eng_top1 = sorted(eng_dict[key], key=lambda key: key[1], reverse=True)[0]
        #if tran_dict:
            #tran_top1 = sorted(tran_dict[key], key=lambda key: key[1], reverse=True)[0][1]
        if zh_dict:
            zh_top1 = sorted(zh_dict[key], key=lambda key: key[1], reverse=True)[0]
        
        if eng_top1[1] > zh_top1[1]:
            if eng_top1[0] == word_dict[key]:
                source_count += 1
            else:
                eng_count += 1
        else:
            zh_count += 1
        #if eng_top1 == max(eng_top1, zh_top1):
            #eng_count += 1
        #elif tran_top1 == max(eng_top1, tran_top1, zh_top1):
            #tran_count += 1
        #elif zh_top1 == max(eng_top1, tran_top1, zh_top1):
            #zh_count += 1
    print(f"zh: {100*zh_count / len(zh_dict)}")
    print(f"eng: {100* eng_count / len(zh_dict)}")
    print(f"source: {100*source_count / len(zh_dict)}")


def diff_lang_rank(eng_dict, tran_dict, zh_dict):
    eng_count = 0
    tran_count = 0
    zh_count = 0
    for key in zh_dict:
        tran_top1 = -np.inf
        zh_top1 = -np.inf
        eng_top1 = sorted(eng_dict[key], key=lambda key: key[1], reverse=True)[0][1]
        if tran_dict:
            tran_top1 = sorted(tran_dict[key], key=lambda key: key[1], reverse=True)[0][1]
        if zh_dict:
            zh_top1 = sorted(zh_dict[key], key=lambda key: key[1], reverse=True)[0][1]
        if eng_top1 == max(eng_top1, tran_top1, zh_top1):
            eng_count += 1
        elif tran_top1 == max(eng_top1, tran_top1, zh_top1):
            tran_count += 1
        elif zh_top1 == max(eng_top1, tran_top1, zh_top1):
            zh_count += 1
    print(f"eng: {eng_count / len(eng_dict)}")
    #print(f"tran: {tran_count / len(eng_dict)}")
    print(f"zh: {zh_count / len(eng_dict)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word_path", type=str, required=True)
    parser.add_argument("--enPrompt_eng_path", type=str, required=True)
    parser.add_argument("--enPrompt_zh_path", type=str, required=True)

    parser.add_argument("--zhPrompt_eng_path", type=str, required=True)
    parser.add_argument("--zhPrompt_zh_path", type=str, required=True)

    parser.add_argument("--tranPrompt_eng_path", type=str, required=True)
    parser.add_argument("--tranPrompt_zh_path", type=str, required=True)

    args = parser.parse_args()

    with open(args.word_path) as json_file:
        word_dict = json.load(json_file)

    with open(args.zhPrompt_eng_path, "r", encoding="utf-8") as f1:
        zhPrompt_eng_dict = eval(f1.readline())
    with open(args.zhPrompt_zh_path, "r", encoding="utf-8") as f1:
        zhPrompt_zh_dict = eval(f1.readline())

    with open(args.tranPrompt_eng_path, "r", encoding="utf-8") as f1:
       tranPrompt_eng_dict = eval(f1.readline())
    with open(args.tranPrompt_zh_path, "r", encoding="utf-8") as f1:
        tranPrompt_zh_dict = eval(f1.readline())

    with open(args.enPrompt_eng_path, "r", encoding="utf-8") as f1:
        enPrompt_eng_dict = eval(f1.readline())

    with open(args.enPrompt_zh_path, "r") as f3:
        enPrompt_zh_dict = eval(f3.readline())

    print("engPrompt:")
    same_lang_rank(word_dict, enPrompt_eng_dict, enPrompt_zh_dict)
    #same_lang_rank(eng_dict, tran_dict, zh_dict)
    print("zhPrompt:")
    same_lang_rank(word_dict, zhPrompt_eng_dict, zhPrompt_zh_dict)

    print("tranPrompt:")
    same_lang_rank(word_dict, tranPrompt_eng_dict, tranPrompt_zh_dict)