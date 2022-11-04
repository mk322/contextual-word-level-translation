from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F
import torch

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B", return_dict_in_generate=True).to(device)
lex_file = "en-zh.txt"
rare_word_file = "rare_word_ch.txt"
result_txt = "gpt_neo.txt"
target_lang = "Chinese"

if target_lang != "English":
    not_eng = 1
else:
    not_eng = 0
words_dict = {}
rare_word_list = []
result_dict = {}
with open(lex_file, encoding="utf-8") as t:
    for words in t.read().splitlines()[:300]:
        words = words.split(" ")
        # Filter out the English Translations in Non-English Parts
        if (words[not_eng].upper() == words[not_eng].lower()):
            if words[0] not in words_dict:
                words_dict[words[0]] = [words[1]]
            else:
                words_dict[words[0]].append(words[1])

with open(rare_word_file, encoding="utf-8") as t:
    for words in t.read().splitlines():
        words = words.split(" ")
        # Filter out the English Translations in Non-English Parts
        if (words[0].upper() == words[0].lower()):
            rare_word_list.append(words[0])

for source_word in words_dict.keys():
    target_word_list = words_dict[source_word] + rare_word_list
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
            #or (avg_score > result_dict[source_word][1]):
        else:
            result_dict[source_word].append((target_word, avg_score))




with open(result_txt, "w", encoding='utf-8') as r:
    for key in result_dict:
        print(f"{key}, {result_dict[key]}", file=r)
        #print(f"{key}, {result_dict[key][0]},  {round(result_dict[key][1], 3)}", file=r)