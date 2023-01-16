target_lang="English"
source_lang="Chinese"
correct_file="xl-wsd-data/correct_trans_zh_en.json"
incorrect_file="xl-wsd-data/wrong_trans_zh_en.json"
words_file="zh_en_words.json"
sent_file="zh_en_sent.json"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"


for i in 125M 1.3B 2.7B 20B
do 
python -u XL-WSD.py \
    --model_name gpt-neo \
    --model_size $i \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $gpt_neo_output
done

python -u XL-WSD.py \
    --model_name gpt-J \
    --model_size 6B \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $gpt_j_output


for j in 560m 1b1 1b7 3b 7b1
do 
python -u XL-WSD.py \
    --model_name bloom \
    --model_size $j \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $bloom_output
done
