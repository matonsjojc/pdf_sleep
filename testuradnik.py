import PyPDF2, re

def find_matches(groupName, rePattern, tekst):
    #vrne zadetke iz reporta
    reObj = re.compile(rePattern)
    matchObj = reObj.search(tekst)
    if matchObj:
        zadetek = matchObj.group(groupName)
        return zadetek
    else:
        return "ni zadetka"
"""
#pdfFileObj = open('DetailedReportPatientJozeTeropsic.pdf', 'rb')
pdfFileObj = open('DetailedReportPatientFrancBricman.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj) #pdfFileReader object

zadnjaStran = pdfReader.getNumPages() - 1
pageObj1 = pdfReader.getPage(0)
pageObjZadnja = pdfReader.getPage(zadnjaStran)
textFromPage1 = pageObj1.extractText()
textFromPageZadnja = pageObjZadnja.extractText()

rePatternPriimekImeAparat = "r'Information(?<priimek>[\w]*),\s(?<ime>[\w]*)Device: (?<aparat>[\w\s\d\/]*\([\w\s]*\))'"
"""
#tests:
testTekst = "abc123"
testGroupName = "testno_ime"
strng = "a(?P<testno_ime>b)"

reObj = re.compile(r'a(?P<testno_ime>b)')
matchObj = reObj.search(testTekst)
if matchObj:
    zadetek = matchObj.group(testGroupName)
    print(zadetek)
else:
    print("ni zadetka")
