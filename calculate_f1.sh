prompt_type=tranPrompt
source_lang=Chinese
target_lang=English

echo "gpt-neo"
for i in 125M 1.3B 2.7B 20B
do
python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels_$prompt_type\_$source_lang\_$target_lang\_$i.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt
done

echo "gpt-j"
python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-j/labels_$prompt_type\_$source_lang\_$target_lang\_6B.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

echo "bloom"
for k in 560m 1b1 1b7 3b 7b1
do
    python -u xl-wsd-data/evaluate_answers.py \
        --answer_file WSD_Results/bloom/labels_$prompt_type\_$source_lang\_$target_lang\_$k.txt \
        --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt
done