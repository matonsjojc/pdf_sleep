import os, re, slate

#with open('cilensek_stanislav.pdf','rb') as f:
with open('leben_bernarda.pdf','rb') as f:
    doc = slate.PDF(f) #PDF object (tuple stringov po straneh)

stran2 = doc[1]

#zacetne vrednosti spremenljivk so "ni podatka":
#auto cpap spremenljivke:
priimekIme = "ni podatka"
aparat = "ni podatka"
idPacienta = "ni podatka"
kategorija = "ni podatka" #cpap/bipap/asv...
averageUsage = "ni podatka"
medianUsage = "ni podatka"
percentDaysWithUsageAtLeastFourHours = "ni podatka"
deviceMode = "ni podatka"
cpapMeanPressure = "ni podatka"
leak = "ni podatka"
ahi = "ni podatka" #AHI
minCpapPressure = "ni podatka"
maxCpapPressure = "ni podatka"
epr = "ni podatka"
datum = "ni podatka"
timeRange = "ni podatka"

"""
#bipap vars:
ipapSetting = "ni podatka"
epapSetting = "ni podatka"
backupRate = "ni podatka"
"""

# ---------CPAP--------
kategorija = "CPAP"
#priimek in ime
rePriimekIme = re.compile(r'Name: (?P<priimekIme>[\w\s]*)\n')
matchPriimekIme = rePriimekIme.search(stran2)
if matchPriimekIme:
    priimekIme = matchPriimekIme.group('priimekIme')
#id
reId = re.compile(r'Patient ID: (?P<idPacienta>[\d]*)\n')
matchId = reId.search(stran2)
if matchId:
    idPacienta = matchId.group('idPacienta')
#aparat
reAparat = re.compile(r'Device: (?P<aparat>[\w\d\s]*)\(S/N')
matchAparat = reAparat.search(stran2)
if matchAparat:
    aparat = matchAparat.group('aparat')
#device mode
reDeviceMode = re.compile(r'Therapy Mode: (?P<deviceMode>[\w\s]*)\n')
matchDeviceMode = reDeviceMode.search(stran2)
if matchDeviceMode:
    deviceMode = matchDeviceMode.group('deviceMode')
#min cpap tlak
reMinPr = re.compile(r'Minimum Pressure: (?P<minCpapPressure>\d{1,2}\,\d)')
matchMinPr = reMinPr.search(stran2)
if matchMinPr:
    minCpapPressure = matchMinPr.group('minCpapPressure')
#max cpap tlak
reMaxPr = re.compile(r'Maximum Pressure: (?P<maxCpapPressure>\d{1,2}\,\d)')
matchMaxPr = reMaxPr.search(stran2)
if matchMaxPr:
    maxCpapPressure = matchMaxPr.group('maxCpapPressure')
#epr
reEpr = re.compile(r'EPR Level: (?P<epr>\d{1,2}\,\d)')
matchEpr = reEpr.search(stran2)
if matchEpr:
    epr = matchEpr.group('epr')
#time range
reTimeRange = re.compile(r'Total days: (?P<timeRange>\d+)\n')
matchTimeRange = reTimeRange.search(stran2)
if matchTimeRange:
    timeRange = matchTimeRange.group('timeRange')
#percent days with device usage at least 4 hours
rePercentDaysWithUsageAtLeastFourHours = re.compile(r'\% Used Days >= 4 hrs :  (?P<percentDaysWithUsageAtLeastFourHours>[\d]+)')
matchPercentDaysUsageAtLeastFourHours = rePercentDaysWithUsageAtLeastFourHours.search(stran2)
if matchPercentDaysUsageAtLeastFourHours:
    percentDaysWithUsageAtLeastFourHours = matchPercentDaysUsageAtLeastFourHours.group('percentDaysWithUsageAtLeastFourHours')
#povprecna uporaba
reaverageUsage = re.compile(r'Average daily usage: (?P<averageUsage>\d+\:\d+)')
matchaverageUsage = reaverageUsage.search(stran2)
if matchaverageUsage:
    averageUsage = matchaverageUsage.group('averageUsage')
#mediana uporabe
reMedianUsage = re.compile(r'Median daily usage: (?P<medianUsage>\d+\:\d+)')
matchMedianUsage = reMedianUsage.search(stran2)
if matchMedianUsage:
    medianUsage = matchMedianUsage.group('medianUsage')
#povprecni tlak
reCpapMeanPressure = re.compile(r'Pressure - cmH2O\nMedian: (?P<cpapMeanPressure>\d+\,\d+)')
matchCpapMeanPressure = reCpapMeanPressure.search(stran2)
if matchCpapMeanPressure:
    cpapMeanPressure = matchCpapMeanPressure.group('cpapMeanPressure')
#leak
reLeak = re.compile(r'Leak - L/min\nMedian: (?P<leak>\d+\,\d+)')
matchLeak = reLeak.search(stran2)
if matchLeak:
    leak = matchLeak.group('leak')
#ahi
reAhi = re.compile(r'AHI: (?P<ahi>\d+\,\d+)')
matchAhi = reAhi.search(stran2)
if matchAhi:
    ahi = matchAhi.group('ahi')
#datum izpisa podatkov
reDatum = re.compile(r'Report prepared by: [\w\d]* on (?P<datum>\d{1,2}\.\d{1,2}.\d{4})')
matchDatum = reDatum.search(stran2)
if matchDatum:
    datum = matchDatum.group('datum')

print("priimek, ime: ", priimekIme) #priimek
print("idPacienta: ", idPacienta)
print("aparat: ", aparat) #aparat
print("device mode: ", deviceMode)
print("min CPAP pressure: ", minCpapPressure)
print("max CPAP pressure: ", maxCpapPressure)
print("epr:", epr)
print("time range: ", timeRange)
print("percent of days with usage >= 4 h: ", percentDaysWithUsageAtLeastFourHours)
print("average usage: ", averageUsage)
print("median usage: ", medianUsage)
print("cpap mean pressure: ", cpapMeanPressure)
print("leak(l/min): ", leak)
print("avg. AHI: ", ahi)
print("datum: ", datum)

"""
#bipap:
print("ipap setting: ", ipapSetting)
print("epap setting: ", epapSetting)
print("backup rate: ", backupRate)
"""

#output string (cpap):
output = "Vzrok pregleda: ambulantna kontrola " + kategorija + " terapije. \n" + \
"Uvedba terapije: \n" + \
"Veljavnost naročilnice: \n" + \
"Dobavitelj: \n\n" + \
"Tip aparata: " + aparat + "\n" + \
"Tip maske: \n\n" + \
"Nastavitev:  " + deviceMode + "\n " + \
"            "+ minCpapPressure + " - " + maxCpapPressure + " cm vode \n" + \
"             EPR: " + epr + " cm\n\n" + \
"Podatki o rabi in učinkovitosti v zadnjih " + timeRange + " dneh:\n" + \
"    - odstotek dni, ko aparat uporablja več kot 4 h/noč: " + percentDaysWithUsageAtLeastFourHours + "%.\n" + \
"    - povprečna dnevna uporaba [ure:minute]: " + averageUsage + "\n" + \
"    - mediana dnevna uporaba [ure:minute]:   " + medianUsage + "\n\n" + \
"    - povprečni tlak: " + cpapMeanPressure + " cm vode.\n" + \
"    - preveliko uhajanje zraka: " + leak + " l/min.\n" + \
"    - prekinitve dihanja v eni uri: AHI = " + ahi + "/h.\n\n" + \
"Težave: \n\n" + \
"Zaključek: \n\n" + \
"Predvidena kontrola: \n" + \
"Ambulantna kontrola, čez dve leti v Laboratoriju za motnje dihanja v spanju. " + \
"Tri mesece prej nas pokličite, da se dogovorimo za termin. " + \
"Dosegljivi smo od ponedeljka do petka med 9.00 in 11.00 na telefonski številki 04 2569 234. " + \
"V primeru vprašanj ali težav nas pokličite predčasno."

print(output)
#to do:
#kategorijo ugotovi iz device moda
#bipap, asv
