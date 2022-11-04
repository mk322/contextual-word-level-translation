
lex_file = "eng_chinese.txt"

with open(lex_file, encoding="utf-8") as t:
    for words in t.read().splitlines():
        words = words.split(" ")
        print(words[0], words[1])