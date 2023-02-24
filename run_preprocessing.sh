#!/bin/sh

# Preprocessing
python pre_process.py \
    --input_file "xl-wsd-data/inventories/inventory.en.txt" \
    --output_file "contextual_words_cmn_mfs.json" \
    --target_lang cmn \
    --seed 666

python pre_process.py \
    --input_file "xl-wsd-data/inventories/inventory.en.txt" \
    --output_file "contextual_words_heb_mfs.json" \
    --target_lang heb \
    --seed 666

python pre_process.py \
    --input_file "xl-wsd-data/inventories/inventory.en.txt" \
    --output_file "contextual_words_spa_mfs.json" \
    --target_lang spa \
    --seed 666