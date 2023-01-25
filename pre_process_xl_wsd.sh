tlang="en"
declare -A arr

arr["bg"]=Bulgarian

arr+=( ["hr"]=Croatian ["da"]=Danish ["ja"]=Japanese ["nl"]=Dutch ["fr"]=French ["gl"]=Galician ["hu"]=Hungarian ["it"]=Italian)

arr+=( ["ko"]=Korean ["sl"]=Slovenian)
#["de"]=German ["et"]=Estonian 

#for key in ${!arr[@]}; do
    #C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    #C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    #echo ${key} ${arr[${key}]}
#done
git add -A
git commit -am "push all rest languages"
git push
#C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=$lang --full_lang=$full_lang --tlang=$tlang
#C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=$lang --full_lang=$full_lang --tlang=$tlang