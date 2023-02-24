target_lang=Spanish
source_lang=Slovenian
lang=sl
tlang=es
prompt_type=eng



lemma_file=xl-wsd-files/$source_lang/$lang\_$tlang_lemma.json
words_file=xl-wsd-files/$source_lang/$lang\_$tlang_words.json
all_sense_path=xl-wsd-files/$source_lang/all_sense_labels_$lang\_$tlang.txt
invent_file=xl-wsd-data/inventories/inventory.$lang.txt
source_ids_dict_path=xl-wsd-files/$source_lang/source_ids_dict_$lang\_$tlang.txt


for partial in True False
do
    python -u eval_wsd.py \
        --lemma_file=$lemma_file \
        --words_file=$words_file \
        --invent_file=$invent_file \
        --all_sense_path=$all_sense_path \
        --source_ids_dict_path=$source_ids_dict_path \
        --output_file=WSD_Results/gpt-neo/labels_$prompt_type\Prompt_$source_lang\_$target_lang\_20B.txt \
        --result_dict_path=WSD_Results/gpt-neo/output_$prompt_type\Prompt_$source_lang\_$target_lang\_20B_WSD.txt \
        --correct_trans=xl-wsd-files/$source_lang/correct_trans_$lang\_$tlang.json \
        --eng_output=WSD_Results/gpt-neo/output_engPrompt_$source_lang\_English_20B_WSD.txt \
        --eng_sense_path=xl-wsd-files/$source_lang/all_sense_labels_$lang\_en.txt \
        --key_path=xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt \
        --eng_source_id_path=xl-wsd-files/$source_lang/source_ids_dict_$lang\_en.txt \
        --partial=$partial

    for j in 3b 7b1
        do
        python -u eval_wsd.py \
            --lemma_file=$lemma_file \
            --words_file=$words_file \
            --invent_file=$invent_file \
            --all_sense_path=$all_sense_path \
            --source_ids_dict_path=$source_ids_dict_path \
            --output_file=WSD_Results/bloom/labels_$prompt_type\Prompt_$source_lang\_$target_lang\_$j.txt \
            --result_dict_path=WSD_Results/bloom/output_$prompt_type\Prompt_$source_lang\_$target_lang\_$j\_WSD.txt \
            --correct_trans=xl-wsd-files/$source_lang/correct_trans_$lang\_$tlang.json \
            --eng_output=WSD_Results/bloom/output_engPrompt_$source_lang\_English\_$j\_WSD.txt \
            --eng_sense_path=xl-wsd-files/$source_lang/all_sense_labels_$lang\_en.txt \
            --key_path=xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt \
            --eng_source_id_path=xl-wsd-files/$source_lang/source_ids_dict_$lang\_en.txt \
            --partial=$partial
        done
done