from transformers import AutoTokenizer, AutoModelForCausalLM
import torch.nn.functional as F
import torch

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B", return_dict_in_generate=True)

target_lang = "French"
result_txt = "result_gpt_neo_final.txt"
max_token = 2


words_dict = {}
result_dict = {}
with open("test.txt", encoding="utf-8") as t:
    for words in t.read().splitlines():
        words = words.split(", ")
        words_dict[words[0]] = words[1]
    
#print(words_dict)
topk_words = {}

for source_word in words_dict.keys():
    target_word = words_dict[source_word]
    input_string = f"The word \"{source_word}\" translates into {target_lang} as "
    target_word_ids = tokenizer(target_word, add_special_tokens=False)['input_ids'] 
    input_ids = tokenizer(input_string, add_special_tokens=False, return_tensors='pt')['input_ids']
    with torch.no_grad():
        #input_ids = input_ids.to("cuda")
        output = model(input_ids, use_cache=True)
    '''
    print(input_ids.shape[1])
    # TopK words
    result = model.generate(input_ids, do_sample=False, output_scores=True, max_new_tokens=max_token)
    print(result)

    top1_scores = []
    for i in range(len(result.scores)):
        scores = result.scores[i]
        if scores.dim() > 1:
            scores = scores[-1]
        prob = F.log_softmax(scores, dim=-1)
        top1_scores.append(prob[input_ids.shape[1]+i].item())
    avg_prob = sum(top1_scores)/len(top1_scores)
    #avg_prob = torch.mean(prob).item()
    #print(prob)
    decoded_text = tokenizer.decode(result.sequences[0])
    topk_words[source_word] = [(decoded_text, avg_prob)]
    '''

    model_state_cache = output['past_key_values']
    logits = output['logits'].squeeze()
    if logits.dim() > 1: logits = logits[-1]
    model_probs = F.log_softmax(logits, dim=-1)
    top1 = torch.argmax(model_probs, dim=-1)
    decoded_text = tokenizer.decode(top1)
    print(decoded_text)

    target_word_subword_scores = []
    for i, subword_id in enumerate(target_word_ids):
        target_word_subword_scores.append(model_probs[subword_id].item())
        if i+1 < len(target_word_ids):
            x = torch.LongTensor([[subword_id]])
            #x = x.to("cuda")
            output = model(x, past_key_values=model_state_cache, use_cache=True)
            model_cache = output['past_key_values']
            logits = output['logits'].squeeze()
            model_probs = F.log_softmax(logits, dim=-1)

    avg_score = sum(target_word_subword_scores)/len(target_word_subword_scores)
    result_dict[source_word] = (target_word, avg_score)
    print(result_dict)




"""
    #input_ids = tokenizer(, return_tensors="pt").input_ids
    result = model.generate(input_ids, do_sample=False, max_length=1, output_scores=True)
    gen_sequences = result.sequences[:, input_ids.shape[-1]:]
    probs = torch.stack(result.scores, dim=1).softmax(-1)
    gen_probs = torch.gather(probs, 2, gen_sequences[:, :, None]).squeeze(-1)
    decoded_text = tokenizer.decode(result.sequences[0])
"""




'''
with open(result_txt, "w", encoding='utf-8') as r:
    for key in result_dict:
        print(f"{key}, {result_dict[key]}", file=r)
        print(f"{key}, {topk_words[key]}", file=r)
    #print(f"Score: {gen_probs[0][0]}", file=r)
'''