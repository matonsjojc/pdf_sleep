import PyPDF2, re

pdfFileObj = open('DetailedReportPatientJozeTeropsic.pdf', 'rb')      #cpap
#pdfFileObj = open('DetailedReportPatientZdravkoGlobocnik.pdf', 'rb') #bipap
#pdfFileObj = open('DetailedReportPatientFrancBricman.pdf', 'rb')     #asv
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #pdfFileReader object

#stevilka predzadnje in zadnje strani
predzadnjaStran = pdfReader.getNumPages() -2
zadnjaStran = pdfReader.getNumPages() - 1

pageObj1 = pdfReader.getPage(0)
pageObjPredzadnja = pdfReader.getPage(predzadnjaStran)
pageObjZadnja = pdfReader.getPage(zadnjaStran)

textFromPage1 = pageObj1.extractText()
textFromPagePredzadnja = pageObjPredzadnja.extractText()
textFromPageZadnja = pageObjZadnja.extractText()

#zacetne vrednosti spremenljivk so "ni podatka":
priimek = "ni podatka"
ime = "ni podatka"
aparat = "ni podatka"
idPacienta = "ni podatka"
kategorija = "ni podatka" #cpap/bipap/asv...
percentDaysWithDeviceUsage = "ni podatka"
cumulativeUsage = "ni podatka"
averageUsageAllDays = "ni podatka"
averageUsageDaysUsed = "ni podatka"
percentDaysWithUsageAtLeastFourHours = "ni podatka"

#Priimek, ime, model aparata
reObjPriimekImeAparat = re.compile(r'Information(?P<priimek>[\w]*),\s(?P<ime>[\w]*)Device: (?P<aparat>[\w\s\d\/]*\([\w\s]*\))')
matchObjPriimekImeAparat = reObjPriimekImeAparat.search(textFromPage1)
if matchObjPriimekImeAparat:
    priimek = matchObjPriimekImeAparat.group('priimek')
    ime = matchObjPriimekImeAparat.group('ime')
    aparat = matchObjPriimekImeAparat.group('aparat')
else:
    print('no matches')

# ---------CPAP--------
if "REMstar" in aparat:
    kategorija = "CPAP"
    #id pacienta
    reObjID = re.compile(r'Patient ID: (?P<idPacienta>\d*) Therapy')
    matchObjID = reObjID.search(textFromPageZadnja)
    if matchObjID:
        idPacienta = matchObjID.group('idPacienta')
    #days with device usage
    reObjDaysWithDeviceUsage = re.compile(r'Days with Device Usage(?P<daysWithDeviceUsage>\d*) day')
    matchObjDaysWithDeviceUsage = reObjDaysWithDeviceUsage.search(textFromPageZadnja)
    if matchObjDaysWithDeviceUsage:
        daysWithDeviceUsage = matchObjDaysWithDeviceUsage.group('daysWithDeviceUsage')
    #percent days with device usage
    rePercentDaysWithDeviceUsage = re.compile(r'Percent Days with Device Usage(?P<percentDaysWithDeviceUsage>\d+\.\d+)%')
    matchPercentDaysWithDeviceUsage = rePercentDaysWithDeviceUsage.search(textFromPageZadnja)
    if matchPercentDaysWithDeviceUsage:
        percentDaysWithDeviceUsage = matchPercentDaysWithDeviceUsage.group('percentDaysWithDeviceUsage')
    #cumulative usage
    reCumulativeUsage = re.compile(r'Cumulative Usage(?P<cumulativeUsage>[\d* days| hrs\.| mins\.| secs\.]*)')
    matchCumulativeUsage = reCumulativeUsage.search(textFromPageZadnja)
    if matchCumulativeUsage:
        cumulativeUsage = matchCumulativeUsage.group('cumulativeUsage')
    #average usage - all days
    reAverageUsageAllDays = re.compile(r'Average Usage \(All Days\)(?P<averageUsageAllDays>[\d* days| hrs\.| mins\.| secs\.]*)')
    matchAverageUsageAllDays = reAverageUsageAllDays.search(textFromPageZadnja)
    if matchAverageUsageAllDays:
        averageUsageAllDays = matchAverageUsageAllDays.group('averageUsageAllDays')
    #average usage - days used
    reAverageUsageDaysUsed = re.compile(r'Average Usage \(Days Used\)(?P<averageUsageDaysUsed>[\d* days| hrs\.| mins\.| secs\.]*)')
    matchAverageUsageDaysUsed = reAverageUsageDaysUsed.search(textFromPageZadnja)
    if matchAverageUsageDaysUsed:
        averageUsageDaysUsed = matchAverageUsageDaysUsed.group('averageUsageDaysUsed')
    #percent days with usage at least four hours
    rePercentDaysUsageAtLeastFourHours = re.compile(r'Percent of Days with Usage >= 4 Hours(?P<percentDaysWithUsageAtLeastFourHours>\d*\.\d*)\%Percent')
    matchPercentDaysUsageAtLeastFourHours = rePercentDaysUsageAtLeastFourHours.search(textFromPageZadnja)
    if matchPercentDaysUsageAtLeastFourHours:
        percentDaysWithUsageAtLeastFourHours = matchPercentDaysUsageAtLeastFourHours.group('percentDaysWithUsageAtLeastFourHours')




#----------BIPAP---------
elif "BiPAP" in aparat and "SV" not in aparat:
    kategorija = "bipap"

#----------ASV-----------
elif "SV" in aparat:
    kategorija = "asv"

"""
#ostalo - ure, nastavitve, ahi, leak...
reObjOstalo = re.compile(r'''(


    Percent\sof\sDays\swith\sUsage\s>=\s4\sHours(\d*\.\d*)%Percent # percent of days with usage min. 4 h
    .*
    Device\sSettings\sas\sof[\d\/]*([\w\s\/\-]*)Device\sSettingsDevice         # device mode

)''', re.VERBOSE)
matchObjOstalo = reObjOstalo.search(textFromPageZadnja)
daysWithDeviceUsage = matchObjOstalo.group(2)
percentDaysWithDeviceUsage = matchObjOstalo.group(3)
cumulativeUsage = matchObjOstalo.group(4)
averageUsageAllDays = matchObjOstalo.group(5)
averageUsageDaysUsed = matchObjOstalo.group(6)
percentDaysWithUsageAtLeastFourHours = matchObjOstalo.group(7)
deviceMode = matchObjOstalo.group(8)
"""

print("priimek: ", priimek) #priimek
print("ime: ", ime) #ime
print("aparat: ", aparat) #aparat
print("idPacienta: ", idPacienta)

print("days with device usage: ", daysWithDeviceUsage)
print("percent days with device usage: ", percentDaysWithDeviceUsage)
print("cumulative usage: ", cumulativeUsage)
print("average usage (all days): ", averageUsageAllDays)
print("average usage (days used): ", averageUsageDaysUsed)
print("percent of days with usage >= 4 h: ", percentDaysWithUsageAtLeastFourHours)
"""
print("device mode: ", deviceMode)

"""
#print(textFromPage1)
#print(textFromPageZadnja)

# todo:
# kategorija naj se doloci iz
