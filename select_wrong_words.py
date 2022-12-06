import random
input_file = "francais.txt"
output_file = "wrong_words_fra.txt"
num_words = 300
chosen_list = []
seed = 666

with open(input_file, "r") as f:
    lines = f.read().splitlines()
    random.seed(seed)
    indices = random.choices(range(len(lines)), k=num_words)
    for i in indices:
        word = lines[i].split("\t")[0]
        #if len(word) == 2:
        chosen_list.append(word.lower())
    
with open(output_file, "a") as o:
    for word in chosen_list:
        print(word, file=o)