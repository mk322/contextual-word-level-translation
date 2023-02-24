
target_lang=Spanish
dict_file="contextual_words_spa.json"
incorrect_words_file="wrong_words_spa_new.txt"
gpt_neo_output="./Results/gpt-neo/"
bloom_output="./Results/bloom/"
gpt_j_output="./Results/gpt-j/"

for i in 125M 1.3B 2.7B 20B
do 
    python -u evaluate.py \
        --model_name bloom \
        --model_size $i \
        --target_lang $target_lang \
        --dict_file $dict_file \
        --incorrect_words_file $incorrect_words_file \
        --incorrect_words_num 50 \
        --out_path $gpt_neo_output
done


python -u evaluate.py \
    --model_name gpt-J \
    --model_size 6B \
    --target_lang $target_lang \
    --dict_file $dict_file \
    --incorrect_words_file $incorrect_words_file \
    --incorrect_words_num 50 \
    --out_path $gpt_j_output

for j in 560m 1b1 1b7 3b 7b1
do 
    python -u evaluate.py \
        --model_name bloom \
        --model_size $j \
        --target_lang $target_lang \
        --dict_file $dict_file \
        --incorrect_words_file $incorrect_words_file \
        --incorrect_words_num 50 \
        --out_path $bloom_output
done