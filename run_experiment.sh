#!/bin/sh


for i in 125M 1.3B 2.7B
do 
    python experiment_with_contexts.py \
        --model_name gpt-neo \
        --model_size $i
done

for j in 560m 1b1 1b7 3b
do 
    python experiment_with_contexts.py \
        --model_name bloom \
        --model_size $j
done


