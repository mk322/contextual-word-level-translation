import random
input_file = "./WiC_dataset/train/train.data.txt"
output_file = "input_words_eng.txt"
#num_words = 2000
chosen_list = []
seed = 666

with open(input_file, "r") as f:
    lines = f.read().splitlines()
    random.seed(seed)
    indices = random.choices(range(len(lines)), k=len(lines))
    for i in indices:
        word = lines[i].split("\t")[0]
        chosen_list.append(word)
    
with open(output_file, "w") as o:
    for word in chosen_list:
        print(word, file=o)