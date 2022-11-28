from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F
import torch
import numpy as np
import json
import argparse
import random

lang_dict_nltk = {
    "Chinese": "cmn",
    "English": "eng",
    "German": "ger"
}

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model_name', type=str, default='gpt-neo', required=True)
parser.add_argument('-s', '--model_size', type=str, required=True)
parser.add_argument('-d', '--dict_file', type=str, default="contextual_words_cmn.json")
parser.add_argument('-t', '--target_lang', type=str, default="Chinese")
parser.add_argument('-i', '--incorrect_words_file', type=str, default="wrong_words_ch.txt")
parser.add_argument('--incorrect_words_num', type=int, default=50)
parser.add_argument('--seed', type=int, default=666)

args = parser.parse_args()

if args.model_name == "gpt-neo":
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-"+args.model_size)
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-"+args.model_size, return_dict_in_generate=True).to(device)
    result_txt = f"Results/gpt-neo/gpt-neo_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
else:
    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-"+args.model_size)
    model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-"+args.model_size, return_dict_in_generate=True).to(device)
    result_txt = f"Results/bloom/bloom_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"

#preprocess_into_dict(args.input_file, args.dict_file, lang_dict_nltk[args.target_lang], args.lex_size, args.seed)

words_dict = {}
wrong_word_list = []
result_dict = {}
topk_dict = {}

with open(args.dict_file) as json_file:
    words_dict = json.load(json_file)

with open(args.incorrect_words_file, encoding="utf-8") as t:
    words = t.read().splitlines()
    random.seed(args.seed)
    chosen_words = random.choices(words, k=args.incorrect_words_num)
    for word in chosen_words:
        word = word.split(" ")
        # Filter out the English Translations in Non-English Parts
        if (word[0].upper() == word[0].lower()):
            wrong_word_list.append(word[0])



for source_word in words_dict.keys():
    # Each iteration is a sense
    target_word_list = words_dict[source_word][0] + wrong_word_list + words_dict[source_word][2]
    for j in range(0, len(words_dict[source_word]), 2):
        input_string = f"In \"{words_dict[source_word][j+1]}\", the word {source_word} translates into {args.target_lang} as "
        for target_word in target_word_list:
            target_word_ids = tokenizer(target_word, add_special_tokens=False)['input_ids'] 
            input_ids = tokenizer(input_string, add_special_tokens=False, return_tensors='pt')['input_ids']
            with torch.no_grad():
                input_ids = input_ids.to(device)
                output = model(input_ids, use_cache=True)
            model_state_cache = output['past_key_values']
            logits = output['logits'].squeeze()
            if logits.dim() > 1: logits = logits[-1]
            model_probs = F.log_softmax(logits, dim=-1)
            #top1 = torch.argmax(model_probs, dim=-1)
            #decoded_text = tokenizer.decode(top1)

            target_word_subword_scores = []
            for i, subword_id in enumerate(target_word_ids):
                target_word_subword_scores.append(model_probs[subword_id].item())
                if i+1 < len(target_word_ids):
                    x = torch.LongTensor([[subword_id]])
                    x = x.to(device)
                    output = model(x, past_key_values=model_state_cache, use_cache=True)
                    model_cache = output['past_key_values']
                    logits = output['logits'].squeeze()
                    model_probs = F.log_softmax(logits, dim=-1)
            avg_score = round(sum(target_word_subword_scores)/len(target_word_subword_scores), 6)
            if ((source_word, j) not in result_dict): 
                result_dict[(source_word, j)] = [(target_word, avg_score)]
            else:
                result_dict[(source_word, j)].append((target_word, avg_score))
    

# Find 3 metrics

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

# print out the results
with open(result_txt, "w", encoding='utf-8') as r:
    print("Metric 1:", file=r)
    print(f"top1: {round(percent_correct_top1, 6)}; topk: {round(percent_correct_topk, 6)}", file=r)
    print("Metric 2", file=r) 
    print(f"average correct log-likelihood: {avg_log_correct}; average wrong log-likelihood: {avg_log_wrong}", file=r)
    print("Metric 3", file=r)
    for key in top1_dict:
        print(f"{key[0]}\t{key[1]}\t{top1_dict[key][0]}\t{top1_dict[key][1]}\t{correct_dict[key]}", file=r)

print("finish")
"""
with open("testggg.txt", "w", encoding='utf-8') as r:
    for key in result_dict:
        print(f"{key}, {result_dict[key]}", file=r)
"""