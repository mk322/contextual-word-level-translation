import argparse
import json
import random
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model_name', type=str, default='gpt-neo', required=True)
parser.add_argument('-s', '--model_size', type=str, required=True)
parser.add_argument('-d', '--dict_file', type=str, default="contextual_words_cmn.json")
parser.add_argument('-t', '--target_lang', type=str, default="Chinese")
parser.add_argument('-i', '--incorrect_words_file', type=str, default="wrong_words_ch.txt")
parser.add_argument('--incorrect_words_num', type=int, default=50)
parser.add_argument('--seed', type=int, default=666)
parser.add_argument('--out_path', type=str, default="./Results/gpt-neo/", required=True)
args = parser.parse_args()

if args.model_name == "gpt-neo":
    if args.model_size != "20B":
        result_txt = f"{args.out_path}/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
    else: 
        result_txt = f"{args.out_path}/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
elif args.model_name == "bloom":
    result_txt = f"{args.out_path}/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
elif args.model_name == "gpt-J":
    result_txt = f"{args.out_path}/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
wrong_word_list = []

with open(args.dict_file) as json_file:
    words_dict = json.load(json_file)

with open(args.incorrect_words_file, encoding="utf-8") as t:
    words = t.read().splitlines()
    random.seed(args.seed)
    chosen_words = random.choices(words, k=args.incorrect_words_num)
    for word in chosen_words:
        word = word.split(" ")
        # Filter out the English Translations in Non-English Parts
        wrong_word_list.append(word[0])


con_res = f"{args.out_path}{args.target_lang}_{args.model_size}_{args.incorrect_words_num}_context.txt"
uncon_res = f"{args.out_path}{args.target_lang}_{args.model_size}_{args.incorrect_words_num}_uncontext.txt"

with open(con_res, "r", encoding="utf-8") as f1:
    result_dict = eval(f1.readline())

with open(uncon_res, "r", encoding="utf-8") as f2:
    uncontext_dict = eval(f2.readline())

# Evaluation

# Metric 1a: calculated percentage of examples that the top 1 translation is correct.
num_correct_top1 = len(words_dict) * 2
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        topk_translations = sorted(result_dict[(source_word, j)], key=lambda key: key[1], reverse=True)[0]
        if topk_translations[0] not in words_dict[source_word][j]:
            num_correct_top1 -= 1
            break
percent_correct_top1 = num_correct_top1 / (len(words_dict) * 2)


# Metric 1b: calculated percentage of examples that correct translations are on the top k.
num_correct_topk = len(words_dict) * 2
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        topk_translations = sorted(result_dict[(source_word, j)], key=lambda key: key[1], reverse=True)[:len(words_dict[source_word][j])]
        for top_pair in topk_translations:
            if top_pair[0] not in words_dict[source_word][j]:
                num_correct_topk -= 1
                break

percent_correct_topk = num_correct_topk / (len(words_dict) * 2)

# Metric 2: What is the average log likelihood score of the correct translations (across pairs) vs. 
# average across all other word (non correct) pairs
sum_correct_log = 0
num_correct = 0
num_wrong = 0
sum_wrong_log = 0
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        for pair in result_dict[(source_word, j)]:
            if pair[0] in words_dict[source_word][j]:
                sum_correct_log += pair[1]
                num_correct += 1
            else:
                sum_wrong_log += pair[1]
                num_wrong += 1

avg_log_correct = round(sum_correct_log / num_correct, 6)
avg_log_wrong = round(sum_wrong_log / num_wrong, 6)

# Metric 3: For words with multiple correct translations, which translations does the model give a higher log likelihood to?
top1_dict = {}
correct_dict = {}
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        correct_dict[(source_word, j//2)] = words_dict[source_word][j]
        high = -np.inf
        #if len(words_dict[source_word]) > 1:
        for pair in result_dict[(source_word, j)]:
            if (pair[0] not in wrong_word_list) and (pair[1] > high):
                high = pair[1]
                top1_dict[(source_word, j//2)] = pair
count = 0

for key in top1_dict:
    if top1_dict[key][0] in correct_dict[key]:
        count += 1
precision_wsd = round(count / (2*len(words_dict)), 6)

# Metric 4: Precision without context
uncontext_top1_dict = {}
num_correct_top1_uncon = len(words_dict)
for source_word in words_dict.keys():
    top1_translations = sorted(uncontext_dict[source_word], key=lambda key: key[1], reverse=True)[0][0]
    uncontext_top1_dict[source_word] = top1_translations
    correct_translations = words_dict[source_word][0] + words_dict[source_word][2]
    if top1_translations not in correct_translations:
        num_correct_top1_uncon -= 1

percent_correct_top1_uncon = round(num_correct_top1_uncon / len(words_dict), 6)

# Metric 5: Pecentage of examples that flips after adding contexts
valid_example = 0
flip = 0
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        if j == 2:
            other = 0
        else:
            other = 2
        if uncontext_top1_dict[source_word] in words_dict[source_word][other]:
            valid_example += 1
            top1_translations = sorted(result_dict[(source_word, j)], key=lambda key: key[1], reverse=True)[0][0]
            if top1_translations in words_dict[source_word][j]:
                flip += 1
        
percent_flip = round(flip / valid_example, 6)



# Metric 6: percentage of examples that adding the context "fixes" uncontextualized translation errors
errors =  0
fixed = 0
for source_word in words_dict.keys():
    for j in range(0, len(words_dict[source_word]), 2):
        # uncontextualized error
        correct_translations = words_dict[source_word][0] + words_dict[source_word][2]
        if uncontext_top1_dict[source_word] not in correct_translations:
            errors += 1
            top1_translations = sorted(result_dict[(source_word, j)], key=lambda key: key[1], reverse=True)[0][0]
            if top1_translations in words_dict[source_word][j]:
                fixed += 1

percent_fix = 0
if errors > 0:
    percent_fix = round(fixed / errors, 6)


print("complete")

# print out the results
with open(result_txt, "w", encoding='utf-8') as r:
    print("Metric 1:", file=r)
    print(f"top1: {round(percent_correct_top1, 6)}; topk: {round(percent_correct_topk, 6)}", file=r)
    print("Metric 2", file=r) 
    print(f"average correct log-likelihood: {avg_log_correct}; average wrong log-likelihood: {avg_log_wrong}", file=r)
    print("Metric 3", file=r)
    print(f"WSD Acc: {precision_wsd}", file=r)
    print("Metric 4", file=r)
    print(f"without context top 1 acc: {percent_correct_top1_uncon}", file=r)
    print("Metric 5", file=r)
    print(f"percentage of examples that flip: {percent_flip}, {flip}, {valid_example}", file=r)
    print("Metric 6", file=r)
    print(f"percentage of examples that fix: {percent_fix}, {fixed}, {errors}", file=r)