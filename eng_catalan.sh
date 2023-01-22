target_lang=English
lang=ca
tlang=en
source_lang=Catalan
correct_file=xl-wsd-files/$source_lang/correct_trans_$lang\_$tlang.json
incorrect_file=xl-wsd-files/$source_lang/wrong_trans_$lang\_$tlang.json
words_file=xl-wsd-files/$source_lang/$lang\_$tlang\_words.json
sent_file=xl-wsd-files/$source_lang/$lang\_$tlang\_sent.json
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"
prompt_type=eng

for j in 3b 7b1
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
    --out_path $bloom_output \
    --prompt_type $prompt_type
done

for i in 20B
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
    --out_path $gpt_neo_output \
    --prompt_type $prompt_type
done

python -u XL-WSD.py \
    --model_name gpt-j \
    --model_size 6B \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $gpt_j_output \
    --prompt_type $prompt_type
