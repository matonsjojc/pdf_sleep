import PyPDF2, re

#pdfFileObj = open('DetailedReportPatientJozeTeropsic.pdf', 'rb')      #cpap
pdfFileObj = open('DetailedReportPatientMarijaMeglic.pdf', 'rb')

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
#-za auto cpap
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
deviceMode = "ni podatka"
cpapMeanPressure = "ni podatka"
largeLeak = "ni podatka"
ahi = "ni podatka" #AHI
minCpapPressure = "ni podatka"
maxCpapPressure = "ni podatka"
aFlex = "ni podatka"
datum = "ni podatka"

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
    #device mode
    reDeviceMode = re.compile(r'Device Settings as of[\d\/]*(?P<deviceMode>[\w\s\/\-]*)Device SettingsDevice')
    matchDeviceMode = reDeviceMode.search(textFromPageZadnja)
    if matchDeviceMode:
        deviceMode = matchDeviceMode.group('deviceMode')
    #cpap mean pressure
    reMeanPressure = re.compile(r'CPAP Mean Pressure(?P<cpapMeanPressure>\d+\.\d+) cmH2O')
    matchMeanPressure = reMeanPressure.search(textFromPageZadnja)
    if matchMeanPressure:
        cpapMeanPressure = matchMeanPressure.group('cpapMeanPressure')
    #average time in large leak per day:
    reLargeLeak = re.compile(r'Average Time in Large Leak Per Day(?P<largeLeak>[\d* hrs\.| mins\.| secs.]*)')
    matchLargeLeak = reLargeLeak.search(textFromPageZadnja)
    if matchLargeLeak:
        largeLeak = matchLargeLeak.group('largeLeak')
    #average AHI
    reAhi = re.compile(r'Average AHI(?P<ahi>\d+\.\d+)')
    matchAhi = reAhi.search(textFromPageZadnja)
    if matchAhi:
        ahi = matchAhi.group('ahi')
    #min in max tlak
    reMinMaxPr = re.compile(r'Min Pressure(?P<minCpapPressure>\d*) cmH2OMax Pressure(?P<maxCpapPressure>\d*) cmH2O')
    matchMinMaxPr = reMinMaxPr.search(textFromPageZadnja)
    if matchMinMaxPr:
        minCpapPressure = matchMinMaxPr.group('minCpapPressure')
        maxCpapPressure = matchMinMaxPr.group('maxCpapPressure')
    #a-flex
    reAflex = re.compile(r'A-Flex Setting(?P<aFlex>\d*)A-Flex Lock')
    matchAflex = reAflex.search(textFromPageZadnja)
    if matchAflex:
        aFlex = matchAflex.group('aFlex')
    #datum
    reDatum = re.compile(r'Printed By\:(?P<datum>\d\d?\/\d\d?\/\d\d\d\d)')
    matchDatum = reDatum.search(textFromPageZadnja)
    if matchDatum:
        datum = matchDatum.group('datum')

#----------BIPAP---------
elif "BiPAP" in aparat and "SV" not in aparat:
    kategorija = "bipap"

#----------ASV-----------
elif "SV" in aparat:
    kategorija = "asv"


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
print("device mode: ", deviceMode)
print("cpap mean pressure: ", cpapMeanPressure)
print("avg. time in large leak per day: ", largeLeak)
print("avg. AHI: ", ahi)
print("min CPAP pressure: ", minCpapPressure)
print("max CPAP pressure: ", maxCpapPressure)
print("a-flex: ", aFlex)
print("datum: ", datum)

#print(textFromPage1)
#print(textFromPageZadnja)
"""
# todo:
# kategorija naj se doloci iz device moda
"""
