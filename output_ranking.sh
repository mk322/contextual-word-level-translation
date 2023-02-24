#target_lang1=English
source_lang=Japanese
lang=ja
target_lang=Chinese
tlang=zh


python -u output_ranking.py \
    --word_path=xl-wsd-files/$source_lang/$lang\_$tlang\_words.json \
    --enPrompt_eng_path=WSD_Results/gpt-neo/output_engPrompt_$source_lang\_$target_lang\_20B_en.txt \
    --enPrompt_zh_path=WSD_Results/gpt-neo/output_engPrompt_$source_lang\_$target_lang\_20B_WSD.txt \
    --zhPrompt_eng_path=WSD_Results/gpt-neo/output_zhPrompt_$source_lang\_$target_lang\_20B_en.txt \
    --zhPrompt_zh_path=WSD_Results/gpt-neo/output_zhPrompt_$source_lang\_$target_lang\_20B_WSD.txt \
    --tranPrompt_eng_path=WSD_Results/gpt-neo/output_tranPrompt_$source_lang\_$target_lang\_20B_en.txt \
    --tranPrompt_zh_path=WSD_Results/gpt-neo/output_tranPrompt_$source_lang\_$target_lang\_20B_WSD.txt

for j in 7b1
do
python -u output_ranking.py \
    --word_path=xl-wsd-files/$source_lang/$lang\_$tlang\_words.json \
    --enPrompt_eng_path=WSD_Results/bloom/output_engPrompt_$source_lang\_$target_lang\_$j\_en.txt \
    --enPrompt_zh_path=WSD_Results/bloom/output_engPrompt_$source_lang\_$target_lang\_$j\_WSD.txt \
    --zhPrompt_eng_path=WSD_Results/bloom/output_zhPrompt_$source_lang\_$target_lang\_$j\_en.txt \
    --zhPrompt_zh_path=WSD_Results/bloom/output_zhPrompt_$source_lang\_$target_lang\_$j\_WSD.txt \
    --tranPrompt_eng_path=WSD_Results/bloom/output_tranPrompt_$source_lang\_$target_lang\_$j\_en.txt \
    --tranPrompt_zh_path=WSD_Results/bloom/output_tranPrompt_$source_lang\_$target_lang\_$j\_WSD.txt
done
