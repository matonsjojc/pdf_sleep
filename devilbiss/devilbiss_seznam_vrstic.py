import os, re, slate
from io import StringIO

#with open('devilbiss1.pdf','rb') as f:
with open('devilbiss_grabljevec_ciril.pdf','rb') as f:
    doc = slate.PDF(f)

textFromPage1 = doc[0]
strPO = StringIO(textFromPage1)
list_vrstic = StringIO.readlines(strPO)

counter = 0

seznam_vrstic = open('seznam_vrstic.txt','w')
for vrstica in list_vrstic:
    cifra_in_vsebina_vrstice = str(counter) + ": " + vrstica
    print(cifra_in_vsebina_vrstice)    # - preveri, ce stevilka vrstice sovpada s tekstom - da ni kaj zamaknjeno
    seznam_vrstic.write(cifra_in_vsebina_vrstice)
    counter += 1
seznam_vrstic.close()





#print(list_vrstic)
