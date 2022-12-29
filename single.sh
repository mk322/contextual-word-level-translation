target_lang=Spanish
dict_file="contextual_words_spa.json"
incorrect_words_file="wrong_words_spa_new.txt"
gpt_neo_output="./Results/gpt-neo/"
bloom_output="./Results/bloom/"
gpt_j_output="./Results/gpt-j/"

python -u evaluate.py \
    --model_name bloom \
    --model_size 7b1 \
    --target_lang $target_lang \
    --dict_file $dict_file \
    --incorrect_words_file $incorrect_words_file \
    --incorrect_words_num 50 \
    --out_path $bloom_output
