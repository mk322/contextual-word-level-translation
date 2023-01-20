target_lang="English"
source_lang="Chinese"
lemma_file="zh_en_lemma.json"
words_file="zh_en_words.json"
all_sense_path="all_sense_label.txt"
invent_file="xl-wsd-data/inventories/inventory.zh.txt"
source_ids_dict_path="source_ids_dict_zh_en.txt"
source_lang="Chinese"
target_lang="English"
#output_file = f"WSD_Results/{model_name}/labels3_{source_lang}_{target_lang}_{model_size}.txt"
#result_dict_path = f"WSD_Results/{model_name}/output_{source_lang}_{target_lang}_{model_size}_WSD.txt"

for i in 7b1
do
python -u eval_wsd.py \
    --lemma_file=$lemma_file \
    --words_file=$words_file \
    --invent_file=$invent_file \
    --all_sense_path=$all_sense_path \
    --source_ids_dict_path=$source_ids_dict_path \
    --output_file=WSD_Results/bloom/labels_$source_lang\_$target_lang\_$i.txt \
    --result_dict_path=WSD_Results/bloom/output_$source_lang\_$target_lang\_$i\_WSD.txt
done

for i in 20B
do
python -u eval_wsd.py \
    --lemma_file=$lemma_file \
    --words_file=$words_file \
    --invent_file=$invent_file \
    --all_sense_path=$all_sense_path \
    --source_ids_dict_path=$source_ids_dict_path \
    --output_file=WSD_Results/gpt-neo/labels_$source_lang\_$target_lang\_$i.txt \
    --result_dict_path=WSD_Results/gpt-neo/output_$source_lang\_$target_lang\_$i\_WSD.txt
done