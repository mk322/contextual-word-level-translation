from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F
import torch
import numpy as np
import json
import argparse
import random
import os
from model_utils import init_gpt_neox

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

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
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-"+args.model_size)
        model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-"+args.model_size, return_dict_in_generate=True).to(device)
        result_txt = f"./Results/gpt-neo/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
    else: 
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")
        model = init_gpt_neox(True)
        result_txt = f"./Results/gpt-neo/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"
elif args.model_name == "bloom":
    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-"+args.model_size)
    model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-"+args.model_size, return_dict_in_generate=True).to(device)
    result_txt = f"./Results/bloom/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"

elif args.model_name == "gpt-J":
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B").to(device)
    result_txt = f"./Results/gpt-j/metrics_{args.target_lang}_{args.model_size}_{args.incorrect_words_num}.txt"

else:
  raise Exception("Sorry, the input model name is invalid.")

print("start")
words_dict = {}
wrong_word_list = []
result_dict = {}
topk_dict = {}
uncontext_dict = {}

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


# Uncontextual WLT
for source_word in words_dict.keys():
    target_word_list = words_dict[source_word][0] + wrong_word_list + words_dict[source_word][2]
    for target_word in target_word_list:
        input_string = f"The word \"{source_word}\" translates into {args.target_lang} as "
        target_word_ids = tokenizer(target_word, add_special_tokens=False)['input_ids'] 
        input_ids = tokenizer(input_string, add_special_tokens=False, return_tensors='pt')['input_ids']
        with torch.no_grad():
            input_ids = input_ids.to(device)
            output = model(input_ids, use_cache=True)
        model_state_cache = output['past_key_values']
        logits = output['logits'].squeeze()
        if logits.dim() > 1: logits = logits[-1]
        model_probs = F.log_softmax(logits, dim=-1)

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
        if (source_word not in uncontext_dict): 
            uncontext_dict[source_word] = [(target_word, avg_score)]
        else:
            uncontext_dict[source_word].append((target_word, avg_score))

if not os.path.exists(args.out_path):
    os.makedirs(args.out_path)

uncontext_txt = f"{args.out_path}{args.target_lang}_{args.model_size}_{args.incorrect_words_num}_uncontext.txt"
with open(uncontext_txt, "w") as f:
    f.write(str(uncontext_dict))
    
print("finish")