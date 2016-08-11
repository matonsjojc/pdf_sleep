import PyPDF2, re

pdfFileObj = open('DetailedReportPatientJozeTeropsic.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #pdfFileReader object
# pdfReader.getNumPages())

zadnjaStran = pdfReader.getNumPages() - 1
pageObj1 = pdfReader.getPage(0)
pageObjZadnja = pdfReader.getPage(zadnjaStran)
textFromPage1 = pageObj1.extractText()
textFromPageZadnja = pageObjZadnja.extractText()


#Priimek, ime
#reObjPriimekIme = re.compile(r'Information([\w]*),\s([\w]*)Device:\s(.*)\(')
reObjPriimekIme = re.compile(r'Information([\w]*),\s([\w]*)Device: ([\w\s]*\([\w\s]*\))')
matchObjPriimekIme = reObjPriimekIme.search(textFromPage1)

print(matchObjPriimekIme.group(1))
print(matchObjPriimekIme.group(2))
print(matchObjPriimekIme.group(3))

priimek = matchObjPriimekIme.group(1)
ime = matchObjPriimekIme.group(2)
aparat = matchObjPriimekIme.group(3)

#ID
reObjID = re.compile(r'Phone:Age:([\d]*?)')
matchObjID = reObjID.search(textFromPage1)
idPacienta = matchObjID.group(1)

print(idPacienta)

print(textFromPage1)
