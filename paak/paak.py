import os, re, slate
from io import StringIO

with open('DocumentServlet_plinska.pdf', 'rb') as f:
    doc = slate.PDF(f)

textFromPage1 = doc[0] #string iz pdfja
strPO = StringIO(textFromPage1) #StringIO object

#print(StringIO.readlines(strPO))
list_vrstic = StringIO.readlines(strPO) #StringIO object (strPO) pretvori v list_vrstic

counter = 0 #stevilka vrstice 
    for vrstica in list_vrstic:
    print(counter, ": ", vrstica)
    counter += 1
    if "Plinska analiza arterijske krvi" in vrstica:
        print("aaaaaaaaaaaaaa")
        plinska_prva_vrstica = counter

#[:-1] - da je string brez newlina
id_pacienta = list_vrstic[7][:-1]
priimek_ime = list_vrstic[12][:-1]
ka_ph = list_vrstic[plinska_prva_vrstica + 9][:-1]
ka_pco2 = list_vrstic[plinska_prva_vrstica + 10][:-1]
sat_o2 = list_vrstic[plinska_prva_vrstica + 15]

print("id:", id_pacienta)
print("priimek in ime", priimek_ime)
print("Ka-pH:", ka_ph)
print("Ka-pCO2: ", ka_pco2)
print("Ka-saturacija O2:", sat_o2)
