#!/bin/sh

# Preprocessing
python pre_process.py \
    --input_file "input_words_eng.txt" \
    --output_file "contextual_words_cmn.json" \
    --target_lang cmn \
    --lex_size 1000 \
    --seed 666