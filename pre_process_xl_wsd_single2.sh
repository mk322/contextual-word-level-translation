declare -A arr

arr+=(["bg"]=Bulgarian ["hr"]=Croatian  ["ja"]=Japanese ["gl"]=Galician ["hu"]=Hungarian ["it"]=Italian)

for key in ${!arr[@]}; do
    echo ${key} ${arr[${key}]}
    for tlang in sv sw
    do
    C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    done
done
git add -A
git commit -am "rest target langs preprocessing done"
git push