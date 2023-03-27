declare -A arr
arr["es"]=Spanish

for key in ${!arr[@]}; do
    echo ${key} ${arr[${key}]}
    for tlang in ru fi fr de sv sw
    do
    C:/Users/10494/anaconda3/envs/cse446/python.exe pre_xl_wsd.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    C:/Users/10494/anaconda3/envs/cse446/python.exe print_bn.py --lang=${key} --full_lang=${arr[${key}]} --tlang=$tlang
    done
done
git add -A
git commit -am "Single spanish preprocess done"
git push