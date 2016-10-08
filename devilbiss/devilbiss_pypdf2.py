import os, re, PyPDF2

f = open('devilbiss_grabljevec_ciril.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(f)
pageObj1 = pdfReader.getPage(0)
textFromPage1 = pageObj1.extractText()

print(textFromPage1)
