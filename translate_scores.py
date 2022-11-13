from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F
import torch
import numpy as np

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

gpt_neo = True
if gpt_neo:
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B", return_dict_in_generate=True).to(device)
    result_txt = "gpt_neo.txt"
else:
    tokenizer = AutoTokenizer.from_pretrained("bigscience/bloom-1b7")
    model = AutoModelForCausalLM.from_pretrained("bigscience/bloom-1b7", return_dict_in_generate=True).to(device)
    result_txt = "bloom.txt"

lex_file = "en-zh.txt"
wrong_word_file = "wrong_words_ch.txt"
target_lang = "Chinese"

if target_lang != "English":
    not_eng = 1
else:
    not_eng = 0
words_dict = {}
wrong_word_list = []
result_dict = {}
topk_dict = {}

with open(lex_file, encoding="utf-8") as t:
    for words in t.read().splitlines()[:300]:
        words = words.split(" ")
        # Filter out the English Translations in Non-English Parts
        if (words[not_eng].upper() == words[not_eng].lower()):
            if words[0] not in words_dict:
                words_dict[words[0]] = [words[1]]
            else:
                words_dict[words[0]].append(words[1])

with open(wrong_word_file, encoding="utf-8") as t:
    for words in t.read().splitlines():
        words = words.split(" ")
        # Filter out the English Translations in Non-English Parts
        if (words[0].upper() == words[0].lower()):
            wrong_word_list.append(words[0])

num_correct_examples = len(words_dict)

for source_word in words_dict.keys():

    target_word_list = words_dict[source_word] + wrong_word_list
    for target_word in target_word_list:
        input_string = f"The word \"{source_word}\" translates into {target_lang} as "
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
        avg_score = sum(target_word_subword_scores)/len(target_word_subword_scores)
        if (source_word not in result_dict): 
            result_dict[source_word] = [(target_word, avg_score)]
        else:
            result_dict[source_word].append((target_word, avg_score))
    

# Find 3 metrics

# Metric 1: calculated percentage of examples that correct translations are on the top k.
for source_word in words_dict.keys():
    topk_translations = sorted(result_dict[source_word], key=lambda key: key[0])[:len(words_dict[source_word])]
    for top_word in topk_translations:
        if top_word not in words_dict[source_word]:
            num_correct_examples -= 1
            break

percent_correct_examples = num_correct_examples / len(words_dict)

# Metric 2: What is the average log likelihood score of the correct translations (across pairs) vs. 
# average across all other word (non correct) pairs
sum_correct_log = 0
num_correct = 0
num_wrong = 0
sum_wrong_log = 0
for source_word in words_dict.keys():
    for pair in result_dict[source_word]:
        if pair[0] in words_dict[source_word]:
            sum_correct_log += pair[1]
            num_correct += 1
        else:
            sum_wrong_log += pair[1]
            num_wrong += 1

avg_log_correct = round(sum_correct_log / num_correct,3)
avg_log_wrong = round(sum_wrong_log / num_wrong ,3)

# Metric 3: For words with multiple correct translations, which translations does the model give a higher log likelihood to?
high = -np.inf
top1_dict = {}
for source_word in words_dict.keys():
    for pair in result_dict[source_word]:
        if (pair[0] in words_dict[source_word]) and (pair[1] > high):
            high = pair[1]
            top1_dict[source_word] = pair
    high = -np.inf




with open(result_txt, "w", encoding='utf-8') as r:
    print(f"Metric 1: {percent_correct_examples}", file=r)
    print(f"Metric 2: correct - {avg_log_correct}; wrong - {avg_log_wrong}", file=r)
    print("Metric 3")
    for key in top1_dict:
        print(f"{key}, {top1_dict[key]}", file=r)

    '''
    for key in result_dict:
        print(f"{key}, {result_dict[key]}", file=r)
        #print(f"{key}, {result_dict[key][0]},  {round(result_dict[key][1], 3)}", file=r)
    '''