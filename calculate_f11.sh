target_lang=Spanish
source_lang=Chinese
lang=zh
tlang=es
prompt_type=tran

echo "gpt-neo"
for i in 20B
do
python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels_$prompt_type\Prompt\_$source_lang\_$target_lang\_$i.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt
done

echo "bloom"
for k in 3b 7b1
do
    python -u xl-wsd-data/evaluate_answers.py \
        --answer_file WSD_Results/bloom/labels_$prompt_type\Prompt\_$source_lang\_$target_lang\_$k.txt \
        --gold_file xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt
done

echo "full"
echo "gpt-neo"
for i in 20B
do
python -u xl-wsd-data/evaluate_answers.py \
    --answer_file WSD_Results/gpt-neo/labels_$prompt_type\Prompt\_$source_lang\_$target_lang\_$i\_full.txt \
    --gold_file xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt
done

echo "bloom"
for k in 3b 7b1
do
    python -u xl-wsd-data/evaluate_answers.py \
        --answer_file WSD_Results/bloom/labels_$prompt_type\Prompt\_$source_lang\_$target_lang\_$k\_full.txt \
        --gold_file xl-wsd-data/evaluation_datasets/test-$lang/test-$lang.gold.key.txt
done