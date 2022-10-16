from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B", return_dict_in_generate=True)

target_lang = "French"
result_txt = "result_gpt_neo.txt"

source_word_list = []
result_list = []
with open("test.txt", encoding="utf-8") as t:
    for word in t.read().splitlines():
        source_word_list.append(word)

with open(result_txt, "w", encoding='cp850') as r:
    for source_word in source_word_list:
        input_ids = tokenizer(f"In {target_lang}, the word '{source_word}' means ", return_tensors="pt").input_ids
        result = model.generate(input_ids, do_sample=False, max_length=1, output_scores=True)
        gen_sequences = result.sequences[:, input_ids.shape[-1]:]
        probs = torch.stack(result.scores, dim=1).softmax(-1)
        gen_probs = torch.gather(probs, 2, gen_sequences[:, :, None]).squeeze(-1)
        decoded_text = tokenizer.decode(result.sequences[0])
        print(decoded_text, file=r)
        print(f"Score: {gen_probs[0][0]}", file=r)
