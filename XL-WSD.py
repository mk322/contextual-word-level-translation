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
parser.add_argument('--prompt_type', type=str, default="tran")
parser.add_argument('--test_mode', type=bool, default=False)
parser.add_argument('--candidate_lang', type=str, default="")

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

lang_dict = {
    "Chinese": {"English": "英语", "Spanish": "西班牙语"},
    "Spanish": {"English": "inglés", "Chinese": "Chino"},
    "Catalan": {"English": "a l'anglès", "Chinese": "al xinès", "Spanish": "a l'espanyol"},
    "Basque": {"English": "ingelesera", "Chinese": "txinerera", "Spanish": "gaztelaniara"},
    "German": {"English": "Englische", "Chinese": "Chinesische", "Spanish": "Spanische"},
    "Estonian": {"English": "inglise", "Chinese": "hiina", "Spanish": "hispaania"},
    "French": {"English": "anglais", "Chinese": "chinois", "Spanish": "espagnol"},
    "Bulgarian": {"English": "английски", "Chinese": "китайски", "Spanish": "испански"},
    "Croatian": {"English": "engleski", "Chinese": "kineski", "Spanish": "španjolski"},
    "Danish": {"English": "engelsk", "Chinese": "kinesisk", "Spanish": "spansk"},
    "Dutch": {"English": "Engels", "Chinese": "Chinees", "Spanish": "Spaans"},
    "Galician": {"English": "inglês", "Chinese": "chinês", "Spanish": "español"},
    "Hungarian": {"English": "angolra", "Chinese": "kínaira", "Spanish": "spanyolra"},
    "Italian": {"English": "inglese", "Chinese": "cinese", "Spanish": "spagnolo"},
    "Japanese": {"English": "英語", "Chinese": "中国語", "Spanish": "ペイン語"},
    "Korean": {"English": "영어로", "Chinese": "중국어로", "Spanish": "스페인어로"},
    "Slovenian": {"English": "angleščino", "Chinese": "kitajščino", "Spanish": "španščino"},
    "Chinese": {"Spanish": "西班牙语", "English": "English"}
}


with open(args.correct_file) as json_file:
    correct_dict = json.load(json_file)

with open(args.incorrect_file) as json_file:
    wrong_dict = json.load(json_file)

with open(args.words_file) as json_file:
    words_dict = json.load(json_file)

with open(args.sent_file) as json_file:
    sent_dict = json.load(json_file)

# Contextual WLT
for key in correct_dict.keys():
    if key in wrong_dict:
        target_word_list = list(set(correct_dict[key] + wrong_dict[key]))
    else:
        target_word_list = correct_dict[key]
    if args.test_mode:
        target_word_list.append(words_dict[key])
    sent_id = key[:-5]
    if args.prompt_type == "tran":
        if args.source_lang == "Chinese":
            input_string = f"在\"{sent_dict[sent_id]}\"这句话中, \"{words_dict[key]}\"这个词翻译成{lang_dict['Chinese'][args.target_lang]}为"
        elif args.source_lang == "Spanish":
            input_string = f"En la oración \"{sent_dict[sent_id]}\", la palabra \"{words_dict[key]}\" se traduce al {lang_dict['Spanish'][args.target_lang]} como "
        elif args.source_lang == "Catalan":
            input_string = f"A la frase \"{sent_dict[sent_id]}\", la paraula \"{words_dict[key]}\" es tradueix {lang_dict['Catalan'][args.target_lang]} com a "
        elif args.source_lang == "Basque":
            input_string = f"\"{sent_dict[sent_id]}\" esaldian, \"{words_dict[key]}\" hitza {lang_dict['Basque'][args.target_lang]} "
            for i in range(len(target_word_list)):
                target_word_list[i] += " gisa itzultzen da"
        elif args.source_lang == "German":
            input_string = f"In dem Satz „{sent_dict[sent_id]}“ bedeutet das Wort „{words_dict[key]}“ ins {lang_dict['German'][args.target_lang]} als "
            #for i in range(len(target_word_list)):
                #target_word_list[i] += " übersetzt"
        elif args.source_lang == "Estonian":
            input_string = f"Lauses \"{sent_dict[sent_id]}\" tõlgitakse sõna \"{words_dict[key]}\" {lang_dict['Estonian'][args.target_lang]} keelde kui "
        elif args.source_lang == "French":
            input_string = f"Dans la phrase \"{sent_dict[sent_id]}\", le mot \"{words_dict[key]}\" se traduit en {lang_dict['French'][args.target_lang]} par "
        elif args.source_lang == "Bulgarian":
            input_string = f"В изречението „{sent_dict[sent_id]}“ думата „{words_dict[key]}“ се превежда на {lang_dict['Bulgarian'][args.target_lang]} като " 
        elif args.source_lang == "Croatian":
            input_string = f"U rečenici \"{sent_dict[sent_id]}\", riječ \"{words_dict[key]}\" prevedena je na {lang_dict['Croatian'][args.target_lang]} kao "
        elif args.source_lang == "Danish":
            input_string = f"I sætningen \"{sent_dict[sent_id]}\" oversættes ordet \"{words_dict[key]}\" til {lang_dict['Danish'][args.target_lang]} som "
        elif args.source_lang == "Dutch":
            input_string = f"In de zin \"{sent_dict[sent_id]}\" vertaalt het woord \"{words_dict[key]}\" zich in het {lang_dict['Dutch'][args.target_lang]} als "
        elif args.source_lang == "Galician":
            input_string = f"Na frase \"{sent_dict[sent_id]}\", a palabra \"{words_dict[key]}\" tradúcese ao {lang_dict['Galician'][args.target_lang]} como "
        elif args.source_lang == "Hungarian":
            input_string = f"A \"{sent_dict[sent_id]}\" mondatban fordítsa le a \"{words_dict[key]}\" szót {lang_dict['Hungarian'][args.target_lang]} "
        elif args.source_lang == "Italian":
            input_string = f"Nella frase \"{sent_dict[sent_id]}\", la parola \"{words_dict[key]}\" si traduce in {lang_dict['Italian'][args.target_lang]} come "
        elif args.source_lang == "Japanese":
            input_string = f"「{sent_dict[sent_id]}」という文で、「{words_dict[key]}」という単語は{lang_dict['Japanese'][args.target_lang]}に訳すと " 
            for i in range(len(target_word_list)):
                target_word_list[i] += " となります"
        elif args.source_lang == "Slovenian":
            input_string = f"V stavku \"{sent_dict[sent_id]}\" se beseda \"{words_dict[key]}\" v {lang_dict['Slovenian'][args.target_lang]} prevede kot "
        elif args.source_lang == "Korean":
            input_string = f"\"{sent_dict[sent_id]}\"이라는 문장에서 \"{words_dict[key]}\"이라는 단어는 {lang_dict['Korean'][args.target_lang]} "
            for i in range(len(target_word_list)):
                target_word_list[i] += "로 번역됩니다"

    elif args.prompt_type == "eng":
        input_string = f"In the sentence \" {sent_dict[sent_id]} \", the word {words_dict[key]} is translated into {args.target_lang} as "
    
    elif args.prompt_type == "zh":
        input_string = f"在\"{sent_dict[sent_id]}\"这句话中, \"{words_dict[key]}\"这个词翻译成中文为"

    elif args.prompt_type == "es":
        input_string = f"En la oración \"{sent_dict[sent_id]}\", la palabra \"{words_dict[key]}\" se traduce al español como "

    else:
        raise Exception("Sorry, the prompt type is invalid.")

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
        #if args.source_lang == "German" and args.target_lang == "English":
            #if key not in result_dict: 
                #result_dict[key] = [(target_word[:-10], avg_score)]
            #else:
                #result_dict[key].append((target_word[:-10], avg_score))
        if args.prompt_type == "tran" and args.source_lang == "Basque":
            if key not in result_dict: 
                result_dict[key] = [(target_word[:-18], avg_score)]
            else:
                result_dict[key].append((target_word[:-18], avg_score))
        elif args.prompt_type == "tran" and args.source_lang == "Japanese":
            if key not in result_dict: 
                result_dict[key] = [(target_word[:-6], avg_score)]
            else:
                result_dict[key].append((target_word[:-5], avg_score))
        elif args.prompt_type == "tran" and args.source_lang == "Korean":
            if key not in result_dict: 
                result_dict[key] = [(target_word[:-7], avg_score)]
            else:
                result_dict[key].append((target_word[:-7], avg_score))
        else:
            if key not in result_dict: 
                result_dict[key] = [(target_word, avg_score)]
            else:
                result_dict[key].append((target_word, avg_score))


if not os.path.exists(args.out_path):
    os.makedirs(args.out_path)

if args.test_mode:
    result_txt = f"{args.out_path}output_{args.prompt_type}Prompt_{args.source_lang}_{args.target_lang}_{args.model_size}_{args.candidate_lang}.txt"
else:
    result_txt = f"{args.out_path}output_{args.prompt_type}Prompt_{args.source_lang}_{args.target_lang}_{args.model_size}_WSD.txt"
with open(result_txt, "w") as f:
    f.write(str(result_dict))
    
print("finish")