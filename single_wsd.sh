target_lang="English"
source_lang="Chinese"
correct_file="xl-wsd-data/correct_trans_zh_en.json"
incorrect_file="xl-wsd-data/wrong_trans_zh_en.json"
words_file="zh_en_words.json"
sent_file="zh_en_sent.json"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"

for j in 7b1
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
