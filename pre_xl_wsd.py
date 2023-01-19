#import babelnet as bn
from babelnet import Language, pos
import xml.etree.ElementTree as ET
#from babelnet.data.source import BabelSenseSource
from babelnet import BabelSynsetID

from babelnet.data.lemma import BabelLemmaType

#from nltk.corpus import wordnet as wn
import json

path = "xl-wsd-data/evaluation_datasets/test-zh/test-zh.data.xml"
list_path = "xl-wsd-data/inventories/inventory.zh.txt"
target_path = "xl-wsd-data/inventories/inventory.en.txt"
key_path = "xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt"
# parse an xml file by name
file = ET.parse(path)
lang = "zh"
#use getElementsByTagName() to get tag
root = file.getroot()[0]
print(len(root))


res_dic = {}
sent_dict = {}
instance_dict = {}
word2label = {}
label2word = {}
word_dict = {}

word2label_t = {}
label2word_t = {}
for sent in root:
    s = ""
    for word in sent:
        s += f"{word.text}"
        if word.tag == "instance":
            instance_dict[word.attrib["id"]] = (word.attrib['lemma'], word.attrib["pos"])
            word_dict[word.attrib["id"]] = word.text
        sent_dict[sent.attrib["id"]] = s

with open(f"{lang}_en_words.json", "w") as outfile:
    json.dump(word_dict, outfile)
with open(f"{lang}_en_lemma.json", "w") as outfile:
    json.dump(instance_dict, outfile)
#with open(f"{lang}_en_sent.json", "w") as outfile:
    #json.dump(sent_dict, outfile)
'''
pos_dict = {
    "VERB": pos.POS.VERB,
    "NOUN": pos.POS.NOUN,
    "ADJ": pos.POS.ADJ,
    "ADV": pos.POS.ADV
}

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

with open(list_path , "r", encoding="utf-8") as f:
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

with open(target_path , "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split("\t")
        word = parts[0].split("#")[0]
        pos_ = parts[0].split("#")[1]
        for label in parts[1:]:
            if label.endswith("\n"):
                label = label[:-1]
            if word not in word2label_t:
                word2label_t[word] = [str(label)]
            else:
                word2label_t[word].append(str(label))
            if label not in label2word_t:
                label2word_t[label] = [word]
            else:
                label2word_t[label].append(word)
"""
with open(f"label2word_zh.json", "w") as outfile:
    json.dump(label2word, outfile)
with open(f"word2label_{lang}.json", "w") as outfile:
    json.dump(word2label, outfile)
"""
#print(key_dict)
right_dict = {}
wrong_dict = {}
"""
for key in instance_dict:
    word = instance_dict[key]
    tran_synsets = bn.get_synsets(instance_dict[key], from_langs=[Language.ZH], to_langs=[Language.EN])

    for synset in tran_synsets:
        if str(synset.id) == key_dict[key]:
            right_dict[key] = [str(i) for i in synset.lemmas(language=Language.EN)]
        else:
            if key not in wrong_dict:
                wrong_dict[key] = [str(i) for i in synset.lemmas(language=Language.EN)]
            else:
                wrong_dict[key].extend([str(i) for i in synset.lemmas(language=Language.EN)])
"""


right_dict = {}
wrong_dict = {}
for key in instance_dict:
    word = instance_dict[key][0]
    pos_str = instance_dict[key][1]
    if (word, pos_str) in word2label.keys():
        for label in word2label[(word, pos_str)]:
            pos_ = pos_dict[pos_str]
            synsets = bn.get_synsets(BabelSynsetID(label), to_langs=[Language.EN], poses=[pos_])
            for synset in synsets:
                synset2 = label2word_t[label]
                if str(label) in key_dict[key]:
                    if key not in right_dict:
                        right_dict[key] = set([str(i) for i in synset.lemmas(Language.EN, BabelLemmaType.HIGH_QUALITY)])
                    else:
                        right_dict[key].update(set([str(i) for i in synset.lemmas(Language.EN, BabelLemmaType.HIGH_QUALITY)]))
                else:
                    if key not in wrong_dict:
                        wrong_dict[key] = set([str(i) for i in synset.lemmas(Language.EN, BabelLemmaType.HIGH_QUALITY)])
                    else:
                        wrong_dict[key].update(set([str(i) for i in synset.lemmas(Language.EN, BabelLemmaType.HIGH_QUALITY)]))
        right_dict[key] = list(right_dict[key])
        if key in wrong_dict:
            wrong_dict[key] = list(wrong_dict[key])


print(len(right_dict))
print(len(wrong_dict))


with open(f"correct_trans_{lang}_en.json", "w") as outfile:
    json.dump(right_dict, outfile)
with open(f"wrong_trans_{lang}_en.json", "w") as outfile:
    json.dump(wrong_dict, outfile)
'''

