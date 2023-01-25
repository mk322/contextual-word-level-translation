tlang="en"
declare -A arr

arr["bg"]=Bulgarian

arr+=( ["hr"]=Croatian ["da"]=Danish ["ja"]=Japanese ["nl"]=Dutch ["et"]=Estonian ["fr"]=French ["gl"]=Galician ["hu"]=Hungarian ["de"]=German ["it"]=Italian)

arr+=( ["ko"]=Korean ["sl"]=Slovenian)

for key in ${!arr[@]}; do
    C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    echo ${key} ${arr[${key}]}
done
git commit -m "push all_senses file" all_sense_label.txt
git push
#C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=$lang --full_lang=$full_lang --tlang=$tlang
#C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=$lang --full_lang=$full_lang --tlang=$tlang