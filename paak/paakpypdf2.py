import os, re, PyPDF2

pdfFileObj = open('DocumentServlet_plinska.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pageObj1 = pdfReader.getPage(0)
textFromPage1 = pageObj1.extractText()
