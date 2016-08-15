import PyPDF2, re

pdfFileObj = open('DetailedReportPatientZdravkoGlobocnik.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #pdfFileReader object

zadnjaStran = pdfReader.getNumPages() - 1
pageObj1 = pdfReader.getPage(0)
pageObjZadnja = pdfReader.getPage(zadnjaStran)
textFromPage1 = pageObj1.extractText()
textFromPageZadnja = pageObjZadnja.extractText()

#Priimek, ime, model aparata
reObjPriimekImeAparat = re.compile(r'Information([\w]*),\s([\w]*)Device: ([\w\s\d\/]*\([\w\s]*\))')
matchObjPriimekImeAparat = reObjPriimekImeAparat.search(textFromPage1)

priimek = matchObjPriimekImeAparat.group(1)
ime = matchObjPriimekImeAparat.group(2)
aparat = matchObjPriimekImeAparat.group(3)

#ID
reObjID = re.compile(r'Patient ID: ([\d]*) Therapy')
matchObjID = reObjID.search(textFromPageZadnja)
idPacienta = matchObjID.group(1)

#ostalo - ure, nastavitve, ahi, leak...
reObjOstalo = re.compile(r'''(
    Days\swith\sDevice\sUsage(\d*)\sday                       # days with device usage
    .*
    Percent\sDays\swith\sDevice\sUsage(\d+\.\d+)%             # percent days with device usage
    Cumulative\sUsage([\d*\sdays|\shrs\.|\smins\.|\ssecs\.]*) # cumulative usage
    .*
    Average\sUsage\s\(All\sDays\)([\d*\sdays|\shrs\.|\smins\.|\ssecs\.]*) # average usage (all days)
    Average\sUsage\s\(Days\sUsed\)([\d*\sdays|\shrs\.|\smins\.|\ssecs\.]*) # average usage (days used)
    .*
    Percent\sof\sDays\swith\sUsage\s>=\s4\sHours(\d*\.\d*)%Percent # percent of days with usage min. 4 h

)''', re.VERBOSE)
matchObjOstalo = reObjOstalo.search(textFromPageZadnja)
daysWithDeviceUsage = matchObjOstalo.group(2)
percentDaysWithDeviceUsage = matchObjOstalo.group(3)
cumulativeUsage = matchObjOstalo.group(4)
averageUsageAllDays = matchObjOstalo.group(5)
averageUsageDaysUsed = matchObjOstalo.group(6)
percentDaysWithUsageAtLeastFourHours = matchObjOstalo.group(7)


print("priimek: ", priimek) #priimek
print("ime:", ime) #ime
print("id:", idPacienta)
print("aparat:", aparat) #aparat

print("days with device usage: ", daysWithDeviceUsage)
print("percent days with device usage: ", percentDaysWithDeviceUsage)
print("cumulative usage: ", cumulativeUsage)
print("average usage (all days): ", averageUsageAllDays)
print("average usage (days used): ", averageUsageDaysUsed)
print("percent of days with usage >= 4 h: ", percentDaysWithUsageAtLeastFourHours)



print(textFromPageZadnja)
