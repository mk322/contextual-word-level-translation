declare -A arr
arr["bg"]=Bulgarian
arr+=( ["hr"]=Croatian ["da"]=Danish ["ja"]=Japanese ["nl"]=Dutch ["fr"]=French ["gl"]=Galician ["hu"]=Hungarian ["it"]=Italian)
arr+=( ["ko"]=Korean ["sl"]=Slovenian ["de"]=German ["et"]=Estonian ["es"]=Spanish ["eu"]=Basque ["ca"]=Catalan)

tlang=zh
for key in ${!arr[@]}; do
    echo ${key} ${arr[${key}]}
    C:/Users/10494/anaconda3/envs/cse446/python.exe cover_issue.py --lang=${key} --full_lang=${arr[${key}]} --tlang=zh
done