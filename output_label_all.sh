tlang="en"
declare -A arr
arr["bg"]=Bulgarian
arr+=( ["hr"]=Croatian ["da"]=Danish ["ja"]=Japanese ["nl"]=Dutch ["fr"]=French ["gl"]=Galician ["hu"]=Hungarian ["it"]=Italian)
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

    python -u eval_wsd.py \
        --lemma_file=$lemma_file \
        --words_file=$words_file \
        --invent_file=$invent_file \
        --all_sense_path=$all_sense_path \
        --source_ids_dict_path=$source_ids_dict_path \
        --output_file=WSD_Results/gpt-neo/labels_$prompt_type\Prompt_$source_lang\_$target_lang\_20B.txt \
        --result_dict_path=WSD_Results/gpt-neo/output_$prompt_type\Prompt_$source_lang\_$target_lang\_20B_WSD.txt

    for i in 3b 7b1
    do
    python -u eval_wsd.py \
        --lemma_file=$lemma_file \
        --words_file=$words_file \
        --invent_file=$invent_file \
        --all_sense_path=$all_sense_path \
        --source_ids_dict_path=$source_ids_dict_path \
        --output_file=WSD_Results/bloom/labels_$prompt_type\Prompt_$source_lang\_$target_lang\_$i.txt \
        --result_dict_path=WSD_Results/bloom/output_$prompt_type\Prompt_$source_lang\_$target_lang\_$i\_WSD.txt
    done
    done
done