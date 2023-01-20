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
parser.add_argument('-c', '--correct_file', type=str, default="xl-wsd-data/correct_trans_zh_en.json")
parser.add_argument('--source_lang', type=str, default="Chinese")
parser.add_argument('--target_lang', type=str, default="English")
parser.add_argument('-i', '--incorrect_file', type=str, default="xl-wsd-data/correct_trans_zh_en.json")
parser.add_argument('--words_file', type=str, default="zh_en_words.json")
parser.add_argument('--sent_file', type=str, default="zh_en_sent.json")
parser.add_argument('--seed', type=int, default=666)
parser.add_argument('--out_path', type=str, default="./Results/gpt-neo/", required=True)

args = parser.parse_args()

if args.model_name == "gpt-neo":
    if args.model_size != "20B":
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-"+args.model_size)
        model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-"+args.model_size, return_dict_in_generate=True).to(device)
    else: 
        tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")
        model = init_gpt_neox(True)
elif args.model_name == "bloom":
    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-"+args.model_size)
    model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-"+args.model_size, return_dict_in_generate=True).to(device)

elif args.model_name == "gpt-j":
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B", return_dict_in_generate=True).to(device)

else:
  raise Exception("Sorry, the input model name is invalid.")

print("start")
correct_dict = {}
wrong_dict = {}
words_dict = {}
sent_dict = {}
result_dict = {}
topk_dict = {}
uncontext_dict = {}

with open(args.correct_file) as json_file:
    correct_dict = json.load(json_file)

with open(args.incorrect_file) as json_file:
    wrong_dict = json.load(json_file)

with open(args.words_file) as json_file:
    words_dict = json.load(json_file)

with open(args.sent_file) as json_file:
    sent_dict = json.load(json_file)


# Contextual WLT
for key in words_dict.keys():
    if key in wrong_dict:
        target_word_list = list(set(correct_dict[key] + wrong_dict[key]))
    else:
        target_word_list = correct_dict[key]
    sent_id = key[:-5]
    input_string = f"在\"{sent_dict[sent_id]}\"这句话中, \"{words_dict[key]}\"这个词翻译成英语为 "
    #input_string = f"In the sentence \"{sent_dict[sent_id]}\", the word {words_dict[key]} translates into {args.target_lang} as "
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
        if key not in result_dict: 
            result_dict[key] = [(target_word, avg_score)]
        else:
            result_dict[key].append((target_word, avg_score))


if not os.path.exists(args.out_path):
    os.makedirs(args.out_path)

result_txt = f"{args.out_path}output_chnPrompt_{args.source_lang}_{args.target_lang}_{args.model_size}_WSD.txt"
with open(result_txt, "w") as f:
    f.write(str(result_dict))
    
print("finish")