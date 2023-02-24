tlang="en"
declare -A arr
arr["bg"]=Bulgarian
arr+=( ["hr"]=Croatian ["da"]=Danish ["ja"]=Japanese ["nl"]=Dutch ["et"]=Estonian ["fr"]=French ["gl"]=Galician ["hu"]=Hungarian ["it"]=Italian)
arr+=( ["ko"]=Korean ["sl"]=Slovenian)
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"

target_lang=English

for prompt_type in tran
do
#for key in ${!arr[@]}; do
for key in "nl" "gl" "hr" "hu"
do
    lang=${key}
    source_lang=${arr[${key}]}
    lemma_file=xl-wsd-files/$source_lang/$lang\_$tlang\_lemma.json
    words_file=xl-wsd-files/$source_lang/$lang\_$tlang\_words.json
    all_sense_path=xl-wsd-files/$source_lang/all_sense_labels_$lang\_$tlang.txt
    invent_file=xl-wsd-data/inventories/inventory.$lang.txt
    source_ids_dict_path=xl-wsd-files/$source_lang/source_ids_dict_$lang\_$tlang.txt

    echo "gpt-neo"
    python -u xl-wsd-data/evaluate_answers.py \
        --answer_file WSD_Results/gpt-neo/labels_$prompt_type\Prompt\_$source_lang\_$target_lang\_20B.txt \
        --gold_file xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt

    echo "bloom"
    for k in 3b 7b1
    do
        python -u xl-wsd-data/evaluate_answers.py \
            --answer_file WSD_Results/bloom/labels_$prompt_type\Prompt\_$source_lang\_$target_lang\_$k.txt \
            --gold_file xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt
    done
    done
done