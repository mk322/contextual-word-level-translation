from nltk.corpus import wordnet as wn
import json 
import random
import argparse
parser = argparse.ArgumentParser()

def pre_input_file(file):
    word_list = set()
    with open(file , "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split("\t")
            word = parts[0].split("#")[0]
            pos_ = str(parts[0].split("#")[1])
                
            word_list.add(word.replace("_", " "))
    return list(word_list)


def output_file(words):
    input_dict = {}
    random.seed(args.seed)
    random.shuffle(words)
    print(len(words))
    fil = 0
    for word in words:
        all_sense = wn.synsets(word)
        if (len(all_sense) > 0):
            MFS_sense = all_sense[0]
            MFS_tran = [x.name() for x in MFS_sense.lemmas(lang=args.target_lang)]
            MFS_example = MFS_sense.examples()

            other_tran = None
            other_sense = None
            other_example = None

            if (len(all_sense) > 1 and len(MFS_example) != 0) and (len(MFS_tran) != 0):
                i = 1
                while (other_sense is None and i < len(all_sense)):
                    cur_sense = all_sense[i]
                    cur_example = cur_sense.examples()
                    cur_tran = [x.name() for x in cur_sense.lemmas(lang=args.target_lang)]
                    if (len(cur_example) != 0) and (len(cur_tran) != 0 and (len(set(MFS_tran) & set(cur_tran)) == 0)):
                        other_sense = cur_sense
                        other_tran = cur_tran
                        other_example = cur_example
                    i += 1

                if ((other_sense is not None) and (other_tran is not None)):
                    input_dict[word] = [MFS_tran, MFS_example[0], other_tran, other_example[0]]


    print(len(input_dict))
    with open(args.output_file, "w") as outfile:
        json.dump(input_dict, outfile)

if __name__ == "__main__":
    parser.add_argument('-i', '--input_file', type=str, default="input_words_eng.txt")
    parser.add_argument('-d', '--output_file', type=str, default="contextual_words_dic.json")
    parser.add_argument('-t', '--target_lang', type=str, default="cmn")
    #parser.add_argument('--lex_size', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=666)
    args = parser.parse_args()

    word_list = pre_input_file(args.input_file)
    #print(word_list[:50])
    output_file(word_list)

