import babelnet as bn
from babelnet import Language, POS
import json
import argparse

pos_dict = {
    "VERB": POS.VERB,
    "NOUN": POS.NOUN,
    "ADJ": POS.ADJ,
    "ADV": POS.ADV
}
def output_sense_label(correct_dict, wrong_dict, output_file, t_lang=Language.EN):
    word_label_dict= {}
    print("start finding sense labels")
    with open(output_file, "a", buffering=1, encoding='utf-8') as o:
        #index = list(correct_dict.keys()).index("d000.s9052.t000")
        for key in list(correct_dict.keys()):
            target_list = []
            if key in wrong_dict:
                target_list = wrong_dict[key]
            for word in set(target_list+correct_dict[key]):
                key_word = word.replace("", "_")
                if key_word not in word_label_dict:
                    s = key_word
                    word_label_dict[key_word] = set()
                    for synset in bn.get_synsets(word, from_langs=[t_lang]):
                        word_label_dict[key_word].add(str(synset.id))
                        s += f" {str(synset.id)}"
                    print(s, file=o)
    print("finish")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--full_lang', type=str, required=True)
    parser.add_argument('--lang', type=str, required=True)
    args = parser.parse_args()
    out_path = f"xl-wsd-files/{args.full_lang}/all_sense_labels_{args.lang}.txt"
    correct_tran = f"xl-wsd-files/{args.full_lang}/correct_trans_{args.lang}_en.json"
    wrong_tran = f"xl-wsd-files/{args.full_lang}/wrong_trans_{args.lang}_en.json"
    with open(args.correct_tran, "r") as f1:
        correct_trans_dict = json.load(f1)
    with open(args.wrong_tran, "r") as f2:
        wrong_trans_dict = json.load(f2)
    output_sense_label(correct_trans_dict, wrong_trans_dict, args.out_path)