import babelnet as bn
from babelnet import Language, POS
import xml.etree.ElementTree as ET
from babelnet import BabelSynsetID
from babelnet.data.lemma import BabelLemmaType
import json
import os
import argparse


lang_dict = {
    "en": Language.EN,
    "zh": Language.ZH,
    "es": Language.ES,
    "ru": Language.RU,
    "fi": Language.FI,
    "de": Language.DE,
    "fr": Language.FR,
    "sv": Language.SV,
    "ja": Language.JA,
    "sw": Language.SW,
    "ga": Language.GA,
    "ar": Language.AR
}

# parse an xml file by name
def process(lang, full_lang, tlang="zh"):
    path = f"xl-wsd-data/evaluation_datasets/test-{lang}/test-{lang}.data.xml"
    inventory_path = f"xl-wsd-data/inventories/inventory.{lang}.txt"
    key_path = f"xl-wsd-data/evaluation_datasets/test-{lang}/test-{lang}.gold.key.txt"
    file = ET.parse(path)
    bot_root = file.getroot()
    if not os.path.exists(f"xl-wsd-files/{full_lang}"):
        os.makedirs(f"xl-wsd-files/{full_lang}")

    pos_dict = {
        "VERB": POS.VERB,
        "NOUN": POS.NOUN,
        "ADJ": POS.ADJ,
        "ADV": POS.ADV
    }
    sent_dict = {}
    instance_dict = {}
    word2label = {}
    label2word = {}
    word_dict = {}
    
    for root in bot_root:
        for sent in root:
            s = ""
            for word in sent:
                #s += f"{str(word.text).replace("_", " ")} "
                if word.tag == "instance":
                    ins_word = str(word.text).replace("_", " ")
                    s += f"{ins_word} "
                    instance_dict[word.attrib["id"]] = (word.attrib['lemma'], word.attrib["pos"])
                    word_dict[word.attrib["id"]] = ins_word
                else:
                    ins_word = str(word.text).replace("_", " ")
                    s += f"{ins_word} "
                sent_id = sent.attrib["id"]
                if sent_id.startswith("semeval2010.d002.s"):
                    sent_id = "semeval2010.d002.s" + f"{int(sent_id[-3:])-109:03}"
                elif sent_id.startswith("semeval2010.d003"):
                    sent_id = "semeval2010.d003.s" + f"{int(sent_id[-3:])-184:03}"
                sent_dict[sent_id] = s[:-1]

    with open(f"xl-wsd-files/{full_lang}/{lang}_{tlang}_words.json", "w") as outfile:
        json.dump(word_dict, outfile)
    with open(f"xl-wsd-files/{full_lang}/{lang}_{tlang}_lemma.json", "w") as outfile:
        json.dump(instance_dict, outfile)
    with open(f"xl-wsd-files/{full_lang}/{lang}_{tlang}_sent.json", "w") as outfile:
        json.dump(sent_dict, outfile)



    key_dict = {}
    with open(key_path , "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            parts = line.split(" ")
            key = parts[0]
            labels = []
            for label in parts[1:]:
                labels.append(label)
            key_dict[key] = labels

    with open(inventory_path , "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split("\t")
            word = parts[0].split("#")[0]
            pos_ = str(parts[0].split("#")[1])
            for label in parts[1:]:
                if label.endswith("\n"):
                    label = label[:-1]
                if (word, pos_) not in word2label:
                    word2label[(word, pos_)] = [str(label)]
                else:
                    word2label[(word, pos_)].append(str(label))
                if label not in label2word:
                    label2word[label] = [word]
                else:
                    label2word[label].append(word)


    right_dict = {}
    wrong_dict = {}
    print("start finding synsets")
    for key in instance_dict:
        word = instance_dict[key][0].lower()
        pos_str = instance_dict[key][1]
        if (word, pos_str) in word2label.keys():
            for label in word2label[(word, pos_str)]:
                pos_ = pos_dict[pos_str]
                synsets = bn.get_synsets(BabelSynsetID(label), to_langs=[lang_dict[tlang]], poses=[pos_])
                for synset in synsets:
                    if str(label) in key_dict[key]:
                        if key not in right_dict:
                            right_dict[key] = set([str(i).replace("_", " ").replace("\n", "") for i in synset.lemmas(lang_dict[tlang], BabelLemmaType.HIGH_QUALITY) if (str(i) and str(i) != "%")])
                        else:
                            right_dict[key].update(set([str(i).replace("_", " ").replace("\n", "") for i in synset.lemmas(lang_dict[tlang], BabelLemmaType.HIGH_QUALITY) if (str(i) and str(i) != "%")]))
                    else:
                        if key not in wrong_dict:
                            wrong_dict[key] = set([str(i).replace("_", " ").replace("\n", "") for i in synset.lemmas(lang_dict[tlang], BabelLemmaType.HIGH_QUALITY) if (str(i) and str(i) != "%")])
                        else:
                            wrong_dict[key].update(set([str(i).replace("_", " ").replace("\n", "") for i in synset.lemmas(lang_dict[tlang], BabelLemmaType.HIGH_QUALITY) if (str(i) and str(i) != "%")]))
            if (key in right_dict) and (len(right_dict[key]) == 0):
                del right_dict[key]
                if key in wrong_dict:
                    del wrong_dict[key]
            if (key in right_dict):
                right_dict[key] = list(right_dict[key])
                if key in wrong_dict:
                    wrong_dict[key] = list(wrong_dict[key])

    print(len(right_dict), len(right_dict) / len(instance_dict))
    with open(f"xl-wsd-files/{full_lang}/correct_trans_{lang}_{tlang}.json", "w") as outfile:
        json.dump(right_dict, outfile)
    with open(f"xl-wsd-files/{full_lang}/wrong_trans_{lang}_{tlang}.json", "w") as outfile:
        json.dump(wrong_dict, outfile)

def parse_source_dict(lemma_file, full_lang, lang, tlang="zh"):
    lemma2label = {}
    inventory_file = f"xl-wsd-data/inventories/inventory.{lang}.txt"
    with open(inventory_file , "r", encoding="utf-8") as f:
        lines = f.readlines()
        print("start parsing source dict")
        for line in lines:
            parts = line.split("\t")
            word = parts[0].split("#")[0]
            pos_ = str(parts[0].split("#")[1])
            for label in parts[1:]:
                if label.endswith("\n"):
                    label = label[:-1]
                if (word, pos_) not in lemma2label:
                    lemma2label[(word, pos_)] = [str(label)]
                else:
                    lemma2label[(word, pos_)].append(str(label))

    with open(lemma_file) as json_file:
        lemma_dict = json.load(json_file)
    source_ids_dict = {}
    for key in lemma_dict:
        source_ids_dict[key] = []
        lemma = (lemma_dict[key][0].lower(), lemma_dict[key][1])
        #lemma = tuple(lemma_dict[key])
        for label in lemma2label[lemma]:
            source_ids_dict[key].append(label)
    with open(f"xl-wsd-files/{full_lang}/source_ids_dict_{lang}_{tlang}.txt", "w") as f:
        f.write(str(source_ids_dict))
    print("stop parsing source dict")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--full_lang', type=str, required=True)
    parser.add_argument('--lang', type=str, required=True)
    parser.add_argument('--tlang', type=str, required=True)
    args = parser.parse_args()
    process(args.lang, args.full_lang, args.tlang)
    parse_source_dict(f"xl-wsd-files/{args.full_lang}/{args.lang}_{args.tlang}_lemma.json", args.full_lang, args.lang, args.tlang)