from nltk.corpus import wordnet as wn
import json 
import random
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input_file', type=str, default="input_words_eng.txt")
parser.add_argument('-d', '--output_file', type=str, default="contextual_words_dic.json")
parser.add_argument('-t', '--target_lang', type=str, default="cmn")
parser.add_argument('--lex_size', type=int, default=1000)
parser.add_argument('--seed', type=int, default=666)
args = parser.parse_args()


input_dict = {}
with open(args.input_file, "r") as f:
    words = f.read().splitlines()
    random.seed(args.seed)
    random.shuffle(words)
    print(len(words))
    fil = 0
    sfd = 0
    for word in words:
        all_sense = wn.synsets(word)
        sense1_success = False
        sense2_success = False
        i = 0
        while (not sense1_success) and (i < len(all_sense) - 1):
            sense1 = all_sense[i]
            sense1_examp = sense1.examples()
            sense1_trans = [x.name() for x in sense1.lemmas(lang=args.target_lang)]
            if (len(sense1_examp) != 0) and (len(sense1_trans) != 0):
                for j in range(len(sense1_examp)):
                    if word in sense1_examp[j]:
                        sense1_translations = sense1_trans
                        sense1_examples_sent = sense1_examp[j]
                        sense1_success = True
                        break
            i += 1
        
        while (sense1_success) and (not sense2_success) and (i < len(all_sense)):
            sense2 = all_sense[i]
            sense2_examp = sense2.examples()
            sense2_trans = [x.name() for x in sense2.lemmas(lang=args.target_lang)]
            if (len(sense2_examp) != 0) and (len(sense2_trans) != 0):
                for trans2 in sense2_trans:
                    if trans2 in sense1_translations:
                        continue


                for j in range(len(sense2_examp)):
                    if word in sense2_examp[j]:
                        sense2_translations = sense2_trans
                        sense2_examples_sent = sense2_examp[j]
                        sense2_success = True
                        break
            i += 1

        if (not sense2_success) or (not sense1_success):
            #print(word)
            fil += 1
            continue
        input_dict[word] = [sense1_translations, sense1_examples_sent, sense2_translations, sense2_examples_sent]
        if len(input_dict.keys()) == args.lex_size: break

print(len(input_dict))

        
with open(args.output_file, "w") as outfile:
    json.dump(input_dict, outfile)
        
