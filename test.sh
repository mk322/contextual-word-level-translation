target_lang=French
dict_file="contextual_words_fra.json"
incorrect_words_file="wrong_words_fra.txt"
gpt_neo_output="./Results_test/gpt-neo/"
bloom_output="./Results_test/bloom/"
gpt_j_output="./Results_test/gpt-j/"

python experiment_with_contexts.py \
    --model_name gpt-neo \
    --model_size 125M \
    --target_lang $target_lang \
    --dict_file $dict_file \
    --incorrect_words_file $incorrect_words_file \
    --incorrect_words_num 5 \
    --out_path $gpt_neo_output