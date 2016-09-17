import os, re, slate

with open('cilensek_stanislav.pdf','rb') as f:
    doc = slate.PDF(f) #PDF object (tuple stringov po straneh)

stran2 = doc[1]

#print(stran2)
#zacetne vrednosti spremenljivk so "ni podatka":
#auto cpap spremenljivke:
priimek = "ni podatka"
ime = "ni podatka"

priimekIme = "ni podatka"
aparat = "ni podatka"
idPacienta = "ni podatka"
kategorija = "ni podatka" #cpap/bipap/asv...
percentDaysWithDeviceUsage = "ni podatka"
cumulativeUsage = "ni podatka"
averageUsageAllDays = "ni podatka"
averageUsageDaysUsed = "ni podatka"
percentDaysWithUsageAtLeastFourHours = "ni podatka"
deviceMode = "ni podatka"
cpapMeanPressure = "ni podatka"
largeLeak = "ni podatka"
ahi = "ni podatka" #AHI
minCpapPressure = "ni podatka"
maxCpapPressure = "ni podatka"
aFlex = "ni podatka"
datum = "ni podatka"
timeRange = "ni podatka"
#bipap vars:
ipapSetting = "ni podatka"
epapSetting = "ni podatka"
backupRate = "ni podatka"

rePriimekIme = re.compile(r'Name: (?P<priimekIme>[\w ]*)')
matchPriimekIme = rePriimekIme.search(stran2)
if matchPriimekIme:
    priimekIme = matchPriimekIme.group('priimekIme'))
