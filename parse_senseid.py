import json
from babelnet.language import Language
import babelnet as bn
from babelnet import Language, POS

pos_dict = {
    "VERB": POS.VERB,
    "NOUN": POS.NOUN,
    "ADJ": POS.ADJ,
    "ADV": POS.ADV
}

def parse_source_dict(lemma_file, full_lang, lang, tlang="zh"):
    lemma2label = {}
    inventory_file = f"xl-wsd-data/inventories/inventory.en.txt"
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
        if lemma not in lemma2label:
            byl = bn.get_senses(str(lemma_dict[key][0].lower()), poses=[pos_dict[lemma_dict[key][1]]],from_langs=[Language.EN], sources=[bn.BabelSenseSource.BABELNET])
            for by in set(byl):
                id = by.synset_id
                if id not in source_ids_dict[key]:
                    source_ids_dict[key].append(by.synset_id)
        else:
            for label in lemma2label[lemma]:
                source_ids_dict[key].append(label)
    with open(f"xl-wsd-files/{full_lang}/source_ids_dict_{lang}_{tlang}.txt", "w") as f:
        for key in source_ids_dict:
            s = key
            for label in source_ids_dict[key]:
                s += f" {label}"
            print(s, file=f)
        #f.write(str(source_ids_dict))
    print("stop parsing source dict")

lang="en-coarse"
full_lang="English"
tlang="en"
parse_source_dict(f"xl-wsd-files/{full_lang}/{lang}_{tlang}_lemma.json", full_lang, lang, tlang)