python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels_Chinese_English_20B.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-j/labels_Chinese_English_6B.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels_Chinese_English_2.7B.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/bloom/labels_Chinese_English_1b7.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/bloom/labels2_Chinese_English_1b7.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/bloom/labels2_Chinese_English_3b.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt

python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels2_Chinese_English_20B.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-zh/test-zh.gold.key.txt