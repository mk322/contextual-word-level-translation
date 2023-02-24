declare -A arr
arr+=( ["hu"]=Hungarian)
tlang=es
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"

target_lang=Spanish
echo Catalan

for key in ${!arr[@]}; do
    echo ${key} ${arr[${key}]}
    lang=${key}
    source_lang=${arr[${key}]}
    correct_file=xl-wsd-files/$source_lang/correct_trans_$lang\_$tlang.json
    incorrect_file=xl-wsd-files/$source_lang/wrong_trans_$lang\_$tlang.json
    words_file=xl-wsd-files/$source_lang/$lang\_$tlang\_words.json
    sent_file=xl-wsd-files/$source_lang/$lang\_$tlang\_sent.json
    for prompt_type in tran
    do
    python -u XL-WSD.py \
    --model_name gpt-neo \
    --model_size 20B \
    --source_lang $source_lang \
    --target_lang $target_lang \
    --correct_file $correct_file \
    --words_file $words_file \
    --sent_file $sent_file \
    --incorrect_file $incorrect_file \
    --out_path $gpt_neo_output \
    --prompt_type $prompt_type

done
done