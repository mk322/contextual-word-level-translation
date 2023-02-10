declare -A arr
arr["bg"]=Bulgarian
arr+=( ["hr"]=Croatian ["da"]=Danish ["ja"]=Japanese ["nl"]=Dutch ["fr"]=French ["gl"]=Galician ["hu"]=Hungarian ["it"]=Italian)
arr+=( ["ko"]=Korean ["sl"]=Slovenian ["de"]=German ["et"]=Estonian ["zh"]=Chinese ["eu"]=Basque ["ca"]=Catalan)

tlang=es
for key in ${!arr[@]}; do
    echo ${key} ${arr[${key}]}
    C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
done
git add -A
git commit -am "Chinese target language"
git push