from transformers import pipeline
target_lang = "French"
result_txt = "result.txt"
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B', framework="pt")

source_word_list = []
result_list = []
with open("test.txt", encoding="utf-8") as t:
    for word in t.read().splitlines():
        source_word_list.append(word)

with open(result_txt, "w", encoding='cp850') as r:
    for source_word in source_word_list:
        result = generator(f"In {target_lang}, the word '{source_word}' means ", do_sample=False, max_length=1, output_scores=True)
        print(result, file=r)
