import nltk
from nltk.corpus import wordnet as wn
import json

print(wn.synsets('dog'))
sense1 = wn.synset('cad.n.01')  
sense2 = wn.synset('dog.n.03')  
  
sense1_def = sense1.definition()  


# 'sloping land (especially the slope beside a body of water)' 
 
sense1_examples = sense1.examples()  
# ['they pulled the canoe up on the bank', 'he sat on the bank of the river and watched the currents'] 

print(sense1_def)
print(sense1_examples)
  
sense1_translations = [x.name() for x in sense1.lemmas(lang='fra')] #french 
#['banque', 'rive']  
sense1_translations =  [x.name() for x in sense1.lemmas(lang='cmn')] #chinese 
#['岸', '河边']

 
sense2_def = sense2.definition()  
# 'a financial institution that accepts deposits and channels the money into lending activities'
 
sense2_examples = sense2.examples()  
 # ['he cashed a check at the bank', 'that bank holds the mortgage on my home']
  
sense2_translations = [x.name() for x in sense2.lemmas(lang='fra')] #french 

sense2_translation = [x.name() for x in sense2.lemmas(lang='cmn')] #chinese  

print(sense1_translations)



with open("contextual_words_dic.json") as json_file:
    data = json.load(json_file)
    print(data)