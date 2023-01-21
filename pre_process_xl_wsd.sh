lang="zh"
full_lang="Chinese"

python -u pre_xl_wsd.py \
    --lang=$lang \
    --full_lang=$full_lang

python -u print_bn.py \
    --lang=$lang \
    --full_lang=$full_lang