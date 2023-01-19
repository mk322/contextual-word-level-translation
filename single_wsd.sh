target_lang="English"
source_lang="Chinese"
correct_file="xl-wsd-data/correct_trans_zh_en_no_under.json"
incorrect_file="xl-wsd-data/wrong_trans_zh_en_no_under.json"
words_file="zh_en_words.json"
sent_file="zh_en_sent.json"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"

python -u XL-WSD.py \
    --model_name gpt-neo \
    --model_size 20B \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $gpt_neo_output


python -u XL-WSD.py \
    --model_name bloom \
    --model_size 7b1 \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $bloom_output

python -u XL-WSD.py \
    --model_name gpt-j \
    --model_size 6B \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $gpt_j_output

python -u XL-WSD.py \
    --model_name bloom \
    --model_size 3b \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $bloom_output