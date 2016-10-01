import os, re, slate
from io import StringIO

paths = open('paths_plinska.txt', 'r')
pathInPathOut = paths.readlines()
inPath = pathInPathOut[1][:-1] #pdfs are here
outPath = pathInPathOut[4][:-1] #outputs are here

os.chdir(inPath)
reports = os.listdir(inPath)

for report in reports:
    with open(report, 'rb') as f:
        doc = slate.PDF(f)
    textFromPage1 = doc[0] #string iz pdfja
    strPO = StringIO(textFromPage1) #StringIO object
    #print(StringIO.readlines(strPO))
    list_vrstic = StringIO.readlines(strPO) #StringIO object (strPO), pretvorjen v list_vrstic

    counter = 0 #stevilka vrstice -1
    for vrstica in list_vrstic:
        print(counter, ": ", vrstica)
        counter += 1
        if "Plinska analiza arterijske krvi" in vrstica: #preveri, kje se začne izvid PAAK v pdfju; plinska_prva_vrstica = vrstica
            print("kle se začne plinska")
            plinska_prva_vrstica = counter

    #zacetne vrednosti spremenljivk so "ni podatka"
    output = False #string, iz katerega bo nastal txt file
    id_pacienta = "ni podatka"
    priimek_ime = "ni podatka"
    ka_ph = "ni podatka"
    ka_pco2 = "ni podatka"
    sat_o2 = "ni podatka"




    #[:-1] - da je string brez newlina
    #id in priimek in ime so (verjetno) vedno 6., 11. vrstica
    id_pacienta = list_vrstic[7][:-1]
    priimek_ime = list_vrstic[12][:-1]
    #plinska:
    ka_ph = list_vrstic[plinska_prva_vrstica + 9][:-1]
    ka_pco2 = list_vrstic[plinska_prva_vrstica + 10][:-1]
    sat_o2 = list_vrstic[plinska_prva_vrstica + 15][:-1]

    print("id:", id_pacienta)
    print("priimek in ime:", priimek_ime)
    print("Ka-pH:", ka_ph)
    print("Ka-pCO2: ", ka_pco2)
    print("Ka-saturacija O2:", sat_o2)

    output = "Priimek in ime: " + priimek_ime + "\n" + \
    "id: " + id_pacienta + "\n" + \
    "Ka-ph: " + ka_ph + "\n" + \
    "Ka-pCO2: " + ka_pco2 + "\n" + \
    "Ka-saturacija O2: " + sat_o2 + "\n"

    print(output)

    if output:
        outputFileName = priimek_ime + "_" + id_pacienta + ".txt"
        print(outputFileName)
        os.chdir(outPath)
        outputFile = open(outputFileName, 'w')
        outputFile.write(output)
        outputFile.close()
    else:
        print("nekisjeban")


    #to do:
    # - spremenljivke v list al neki drugega?
    # - preveri, ce stevilka vrstice sovpada s tekstom - da ni kaj zamaknjeno
