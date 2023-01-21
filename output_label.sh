target_lang=English
source_lang=Chinese
lemma_file="xl-wsd-files/$source_lang/zh_en_lemma.json"
words_file="xl-wsd-files/$source_lang/zh_en_words.json"
all_sense_path="xl-wsd-files/$source_lang/all_sense_label.txt"
invent_file="xl-wsd-data/inventories/inventory.zh.txt"
source_ids_dict_path="xl-wsd-files/$source_lang/source_ids_dict_zh_en.txt"

prompt_type=tran

#output_file = f"WSD_Results/{model_name}/labels3_{source_lang}_{target_lang}_{model_size}.txt"
#result_dict_path = f"WSD_Results/{model_name}/output_{source_lang}_{target_lang}_{model_size}_WSD.txt"



for i in 125M 1.3B 2.7B 20B
do
python -u eval_wsd.py \
    --lemma_file=$lemma_file \
    --words_file=$words_file \
    --invent_file=$invent_file \
    --all_sense_path=$all_sense_path \
    --source_ids_dict_path=$source_ids_dict_path \
    --output_file=WSD_Results/gpt-neo/labels_$prompt_type\Prompt_$source_lang\_$target_lang\_$i.txt \
    --result_dict_path=WSD_Results/gpt-neo/output_$prompt_type\Prompt_$source_lang\_$target_lang\_$i\_WSD.txt
done

python -u eval_wsd.py \
    --lemma_file=$lemma_file \
    --words_file=$words_file \
    --invent_file=$invent_file \
    --all_sense_path=$all_sense_path \
    --source_ids_dict_path=$source_ids_dict_path \
    --output_file=WSD_Results/gpt-j/labels_$prompt_type\Prompt_$source_lang\_$target_lang\_6B.txt \
    --result_dict_path=WSD_Results/gpt-j/output_$prompt_type\Prompt_$source_lang\_$target_lang\_6B_WSD.txt

for i in 560m 1b1 1b7 3b 7b1
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