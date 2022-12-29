import babelnet as bn
from babelnet import Language
import xml.etree.ElementTree as ET
from babelnet.data.source import BabelSenseSource
from nltk.corpus import wordnet as wn
import json

path = "xl-wsd-data/evaluation_datasets/test-zh/test-zh.data.xml"
list_path = "xl-wsd-data/inventories/inventory.zh.txt"
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

for sent in root:
    s = ""
    for word in sent:
        s += f"{word.text}"
        if word.tag == "instance":
            instance_dict[word.attrib["id"]] = word.text
    sent_dict[sent.attrib["id"]] = s


#print(sent_dict)
#print(instance_dict)
key_dict = {}
with open(key_path , "r") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split(" ")
        key = parts[0]
        label = parts[1]
        key_dict[key] = label

with open(list_path , "r") as f:
    lines = f.readlines()
    for line in lines:
        parts = line.split("\t")
        word = parts[0].split("#")[0]
        for label in parts[1:]:
            if word not in word2label:
                word2label[word] = [label]
            else:
                word2label[word].append(label)
            if label not in label2word:
                label2word[label] = [word]
            else:
                label2word[label].append(word)
"""
with open(f"label2word_zh.json", "w") as outfile:
    json.dump(label2word, outfile)
with open(f"word2label_{lang}.json", "w") as outfile:
    json.dump(word2label, outfile)
"""
right_dict = {}
wrong_dict = {}
for key in instance_dict:
    word = instance_dict[key]
    synsets = bn.get_synsets(instance_dict[key], from_langs=[Language.ZH], to_langs=[Language.EN])
    for synset in synsets:
        if synset.id == key_dict[key]:
            right_dict[key] = synset.lemmas(language=Language.EN)
        else:
            if key not in wrong_dict:
                wrong_dict[key] = synset.lemmas(language=Language.EN)
            else:
                wrong_dict[key].extend(synset.lemmas(language=Language.EN))

print(len(right_dict))
print(len(wrong_dict))

with open(f"correct_trans_{lang}_en.json", "w") as outfile:
    json.dump(right_dict, outfile)
with open(f"wrong_trans_{lang}_en.json", "w") as outfile:
    json.dump(wrong_dict, outfile)
