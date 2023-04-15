from babelnet.language import Language
import babelnet as bn
byl = bn.get_senses('scream', from_langs=[Language.EN], sources=[bn.BabelSenseSource.BABELNET])
ids = set()
for by in set(byl):
    ids.add(by.synset_id)
print(ids)
#print(byl)