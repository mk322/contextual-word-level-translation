from nltk.corpus import wordnet as wn
import json 

input_file = "experiment_words.txt"
output_file = "contextual_words_dic.json"

target_lang = "cmn"

input_dict = {}
with open(input_file, "r") as f:
    for word in f.read().splitlines():
        all_sense = wn.synsets(word)
        for i in range(len(all_sense) - 1):
            sense1 = all_sense[i]
            sense2 = all_sense[i+1]
            sense1_examples = sense1.examples()  
            sense2_examples = sense2.examples()  
            sense1_translations = [x.name() for x in sense1.lemmas(lang=target_lang)]
            sense2_translations = [x.name() for x in sense2.lemmas(lang=target_lang)]
            if (len(sense1_examples) != 0) and (len(sense2_examples) != 0) and (len(sense1_translations) != 0) and (len(sense2_translations) != 0):
                break
        if (len(sense1_examples) == 0) or (len(sense2_examples) == 0) or (len(sense1_translations) == 0) or (len(sense2_translations) == 0):
            print(word)
            continue
        sense1_examples_sent = ""
        sense1_examples_sent = ""
        for j in range(len(sense1_examples)):
            if word in sense1_examples[j]:
                sense1_examples_sent = sense1_examples[j]
                break
        for k in range(len(sense2_examples)):
            if word in sense2_examples[k]:
                sense2_examples_sent = sense2_examples[k]
                break
        if (sense1_examples_sent == "") or (sense2_examples_sent == ""):
            print(word)
            continue
        input_dict[word] = [sense1_translations, sense1_examples_sent, sense2_translations, sense2_examples_sent]
    
with open(output_file, "w") as outfile:
    json.dump(input_dict, outfile)
            
