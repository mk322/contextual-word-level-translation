target_lang=English
lang=zh
source_lang=Chinese
correct_file=xl-wsd-files/$source_lang/correct_trans_$lang\_en_no_under.json
incorrect_file=xl-wsd-files/$source_lang/wrong_trans_$lang\_en_no_under.json
words_file=xl-wsd-files/$source_lang/$lang\_en_words.json
sent_file=xl-wsd-files/$source_lang/$lang\_en_sent.json
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"
prompt_type=tran

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