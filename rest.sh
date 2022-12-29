target_lang=Chinese
dict_file="contextual_words_cmn.json"
incorrect_words_file="wrong_words_cmn.txt"
gpt_neo_output="./Results/gpt-neo/"
bloom_output="./Results/bloom/"
gpt_j_output="./Results/gpt-j/"


for j in 7b1
#560m 1b1 1b7 3b 7b1
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