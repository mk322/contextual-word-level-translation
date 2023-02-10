import json
import argparse

def cal_num_instances(lang, full_lang, tlang):
    with open(f"xl-wsd-files/{full_lang}/correct_trans_{lang}_{tlang}.json", "r") as outfile:
        right_dict = json.load(outfile)

    with open(f"xl-wsd-files/{full_lang}/correct_trans_{lang}_en.json", "r") as outfile:
        full_dict = json.load(outfile)

    print(full_lang)
    print(len(right_dict), len(full_dict))

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--full_lang', type=str, required=True)
    parser.add_argument('--lang', type=str, required=True)
    parser.add_argument('--tlang', type=str, required=True)
    args = parser.parse_args()
    cal_num_instances(args.lang, args.full_lang, args.tlang)
    #parse_source_dict(f"xl-wsd-files/{args.full_lang}/{args.lang}_{args.tlang}_lemma.json", args.full_lang, args.lang, args.tlang)