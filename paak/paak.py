import os, re, slate
from io import StringIO

numbered_lines = "" #string "st.vrstice - 1: vrstica"; zbrisi to na koncu


paths = open('paths_plinska.txt', 'r')
pathInPathOut = paths.readlines()
inPath = pathInPathOut[1][:-1] #pdfs are here
outPath = pathInPathOut[4][:-1] #outputs are here

os.chdir(inPath)
reports = os.listdir(inPath)

#regex:
def re_ka_ph(vrstica):
    #sprejme vsebino vrstice, ce ustreza obliki za Ka-pH (7.ddd), vrne vrednost, sicer False
    reKa_ph = re.compile(r'(?P<ka_ph>7\.\d\d\d)')
    matchKa_ph = reKa_ph.search(vrstica)
    if matchKa_ph:
        ka_ph = matchKa_ph.group('ka_ph')
        return ka_ph
    return False

def re_ka_pco2(vrstica):
    #sprejme vsebino vrstice, ce ustreza obliki za pCO2 (d.dd), vrne vrednost, sicer False
    re_ka_Pco2 = re.compile(r'(?P<ka_pco2>\d\.\d\d)')
    match_ka_Pco2 = re_ka_Pco2.search(vrstica)
    if match_ka_Pco2:
        ka_pco2 = match_ka_Pco2.group('ka_pco2')
        return ka_pco2
    return False

def re_ka_presezek_baze(vrstica):
    #sprejme vsebino vrstice, ce ustreza obliki za presezek baze (d{1,2}.d), vrne vrednost, sicer False
    re_ka_presezek_baze = re.compile(r'(?P<ka_presezek_baze>\d{1,2}\.\d)')
    match_ka_presezek_baze = re_ka_presezek_baze.search(vrstica)
    if match_ka_presezek_baze:
        ka_presezek_baze = match_ka_presezek_baze.group('ka_presezek_baze')
        return ka_presezek_baze
    return False

def re_ka_standardni_hco3(vrstica):
    #sprejme: vsebino vrstice; ce ustreza obliki za std. hco3 (dd.d), vrne vrednost, sicer False
    re_ka_standardni_hco3 = re.compile(r'(?P<ka_standardni_hco3>\d\d\.\d)')
    match_ka_standardni_hco3 = re_ka_standardni_hco3.search(vrstica)
    if match_ka_standardni_hco3:
        ka_standardni_hco3 = match_ka_standardni_hco3.group('ka_standardni_hco3')
        return ka_standardni_hco3
    return False

def re_sat_o2(vrstica):
    #sprejme: vsebino vrstice, ce ustreza obliki za sat. o2 (0.[5-9]dd), vrne vredost, sicer False
    re_sat_o2 = re.compile(r'(?P<sat_o2>0\.[5-9]\d\d)')
    match_sat_o2 = re_sat_o2.search(vrstica)
    if match_sat_o2:
        sat_o2 = match_sat_o2.group('sat_o2')
        return sat_o2
    return False

def re_ka_po2(vrstica):
    #sprejme: vsebino vrstice, ce ustreza obliki za p02(d{1,2}.d)
    re_ka_po2 = re.compile(r'(?P<ka_po2>\d{1,2}\.\d)')
    match_ka_po2 = re_ka_po2.search(vrstica)
    if match_ka_po2:
        ka_po2 = match_ka_po2.group('ka_po2')
        return ka_po2
    return False

for report in reports:
    with open(report, 'rb') as f:
        doc = slate.PDF(f)
    textFromPage1 = doc[0] #string iz pdfja
    strPO = StringIO(textFromPage1) #StringIO object
    list_vrstic = StringIO.readlines(strPO) #StringIO object (strPO), pretvorjen v list_vrstic

    #zacetne vrednosti spremenljivk so "ni podatka" ali False
    output = False #string, iz katerega bo nastal txt file
    id_pacienta = "ni podatka"
    priimek_ime = "ni podatka"
    dodatek_kisika = "ni podatka"
    ka_ph = "ni podatka"
    ka_pco2 = "ni podatka"
    ka_presezek_baze = "ni podatka"
    ka_standardni_hco3 = "ni podatka"
    sat_o2 = "ni podatka"
    ka_po2 = "ni podatka"

    #stevilke vrstic
    plinska_prva_vrstica = False    #stevilka vrstice, v kateri mora pisati: "Plinska analiza arterijske krvi"
    ka_ph_stevilka_vrstice = False  #stevilka vrstice, v kateri mora biti Ka-pH
    counter = 0 #stevilka vrstice (0 = prva), ki je trenutno v obdelavi

    for vrstica in list_vrstic:
        #preveri, kje se začne izvid PAAK v pdfju; plinska_prva_vrstica = vrstica
        if "Plinska analiza arterijske krvi" in vrstica:
            plinska_prva_vrstica = counter
            counter +=1
        #ce najde zacetek paak izvida, med 5 - 15 vrstic po tem isce, dokler ne najde prve vrednosti, ki ustreza Ka_pH:
        elif plinska_prva_vrstica and ka_ph == "ni podatka" and (15 > (counter - plinska_prva_vrstica) > 5):
            if re_ka_ph(vrstica):
                ka_ph = re_ka_ph(vrstica)
                ka_ph_stevilka_vrstice = counter
                counter += 1
        #ko najde ka_ph, po vrsti izpolnjuje ostale - ce en manjka, ne nadaljuje:
        elif ka_ph_stevilka_vrstice:
            if ka_pco2 == "ni podatka" and re_ka_pco2(vrstica):
                ka_pco2 = re_ka_pco2(vrstica)
            elif ka_pco2 != "ni podatka" and ka_presezek_baze == "ni podatka" and re_ka_presezek_baze(vrstica):
                ka_presezek_baze = re_ka_presezek_baze(vrstica)
            elif ka_pco2 != "ni podatka" and ka_presezek_baze != "ni podatka" and ka_standardni_hco3 == "ni podatka" and re_ka_standardni_hco3(vrstica):
                ka_standardni_hco3 = re_ka_standardni_hco3(vrstica)
            elif ka_pco2 != "ni podatka" and ka_presezek_baze != "ni podatka" and ka_standardni_hco3 != "ni podatka" and sat_o2 == "ni podatka" and re_sat_o2(vrstica):
                sat_o2 = re_sat_o2(vrstica)
            elif ka_pco2 != "ni podatka" and ka_presezek_baze != "ni podatka" and ka_standardni_hco3 != "ni podatka" and sat_o2 != "ni podatka" and ka_po2 == "ni podatka" and re_ka_po2(vrstica):
                ka_po2 = re_ka_po2(vrstica)
            counter += 1
        else:
            counter += 1

    #id in priimek in ime so (verjetno) vedno 6., 11. vrstica; [:-1] - da je string brez newlina
    id_pacienta = list_vrstic[7][:-1]
    priimek_ime = list_vrstic[12][:-1]

    #vdihana kolicina O2 (% ali l):
    dodatek_kisika = list_vrstic[plinska_prva_vrstica + 5][:-1]

    output = "Priimek in ime: " + priimek_ime + "\n" + \
    "id: " + id_pacienta + "\n" + \
    "pH: " + ka_ph + "\n" + \
    "pCO2: " + ka_pco2 + "\n" + \
    "presežek baze: " + ka_presezek_baze + "\n" + \
    "standardni HCO3: " + ka_standardni_hco3 + "\n" + \
    "saturacija O2: " + sat_o2 + "\n" + \
    "pO2: " + ka_po2

    print(output)

    if output:
        outputFileName = priimek_ime + "_" + id_pacienta + ".txt"
        print("zapisujem: ", outputFileName)
        os.chdir(outPath)
        outputFile = open(outputFileName, 'w')
        outputFile.write(output)
        #outputFile.write(numbered_lines) #txt file oblike: st. vrstice -1: vrstica"
        outputFile.close()
    else:
        print("nekisjeban")


    #to do:
    # - spremenljivke v list al neki drugega?
    # - preveri, ce stevilka vrstice sovpada s tekstom - da ni kaj zamaknjeno
