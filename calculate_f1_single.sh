echo "gpt-neo"

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels_Chinese_English_20B.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt


echo "bloom"

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/bloom/labels_engPrompt_Chinese_English_7b1.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/bloom/labels_Chinese_English_7b1.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt