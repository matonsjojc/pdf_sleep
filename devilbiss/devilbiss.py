import os, re, slate
from io import StringIO

#with open('devilbiss1.pdf','rb') as f:
with open('devilbiss_grabljevec_ciril.pdf','rb') as f:
    doc = slate.PDF(f)

textFromPage1 = doc[0]
strPO = StringIO(textFromPage1)
list_vrstic = StringIO.readlines(strPO)

counter = 0

for vrstica in list_vrstic:
    print(counter, ": ", vrstica)
    counter +=1

print(list_vrstic)
