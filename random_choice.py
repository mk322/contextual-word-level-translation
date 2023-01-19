import random
from argparse import ArgumentParser
def parse_file(path):
    id2ans = dict()
    with open(path) as lines:
        for line in lines:
            fields = line.strip().split(" ")
            id, *answers = fields
            ans = list(set(answers))
            if ans:
                id2ans[id] = random.choice(ans)
            else:
                id2ans[id] = ""
    return id2ans

def print_file(out_path, dic):
    with open(out_path, "w") as f:
        for key in dic:
            print(key, dic[key], file=f)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--answer_file", required=True)
    parser.add_argument("--out_file", required=True)


    args = parser.parse_args()

    answer_file = args.answer_file
    out_file = args.out_file

    id2answer = parse_file(answer_file)
    print_file(out_file, id2answer)
