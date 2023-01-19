target_lang=Chinese
dict_file="contextual_words_cmn.json"
incorrect_words_file="wrong_words_cmn.txt"
gpt_neo_output="./WSD_Results/gpt-neo/"
bloom_output="./WSD_Results/bloom/"
gpt_j_output="./WSD_Results/gpt-j/"


python -u random_choice.py \
    --answer_file $gpt_neo_outpu"labels2_Chinese_English_20B.txt" \
    --out_file $gpt_neo_output"labels3_Chinese_English_20B.txt"