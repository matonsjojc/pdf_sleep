import PyPDF2, re, os

paths = open('paths.txt', 'r')
pathInPathOut = paths.readlines()
inPath = pathInPathOut[1][:-1] #pdfs are here
outPath = pathInPathOut[4][:-1] #outputs are

os.chdir(inPath)
reports = os.listdir(inPath)

for report in reports:
    os.chdir(inPath)
    pdfFileObj = open(report, 'rb')
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
    #auto cpap spremenljivke:
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
    timeRange = "ni podatka"
    #bipap vars:
    ipapSetting = "ni podatka"
    epapSetting = "ni podatka"
    backupRate = "ni podatka"


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
        reObjID = re.compile(r'Patient ID: (?P<idPacienta>\d*)')
        matchObjID = reObjID.search(textFromPageZadnja)
        if matchObjID:
            idPacienta = matchObjID.group('idPacienta')
        #days with device usage
        reObjDaysWithDeviceUsage = re.compile(r'Days with Device Usage(?P<daysWithDeviceUsage>\d*) day')
        matchObjDaysWithDeviceUsage = reObjDaysWithDeviceUsage.search(textFromPageZadnja)
        if matchObjDaysWithDeviceUsage:
            daysWithDeviceUsage = matchObjDaysWithDeviceUsage.group('daysWithDeviceUsage')
        #percent days with device usage
        rePercentDaysWithDeviceUsage = re.compile(r'Percent Days with Device Usage(?P<percentDaysWithDeviceUsage>\d+[\.|\,]\d+)%')
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
        rePercentDaysUsageAtLeastFourHours = re.compile(r'Percent of Days with Usage >= 4 Hours(?P<percentDaysWithUsageAtLeastFourHours>\d*[\.|\,]\d*)\%Percent')
        matchPercentDaysUsageAtLeastFourHours = rePercentDaysUsageAtLeastFourHours.search(textFromPageZadnja)
        if matchPercentDaysUsageAtLeastFourHours:
            percentDaysWithUsageAtLeastFourHours = matchPercentDaysUsageAtLeastFourHours.group('percentDaysWithUsageAtLeastFourHours')
        #device mode
        reDeviceMode = re.compile(r'Device Settings as of\d\d?[\/|\.]\d\d?[\/|\.]\d\d\d\d(?P<deviceMode>[\w\s\/\-]*)Device SettingsDevice')
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
        reAhi = re.compile(r'Average AHI(?P<ahi>\d*[\.|\,]\d)')
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
        #date range
        reTimeRange = re.compile(r'Compliance Summary\d\d?[\/|\.]\d\d?[\/|\.]\d\d\d\d - \d\d?[\/|\.]\d\d?[\/|\.]\d\d\d\d \((?P<timeRange>\d*) days')
        timeRangeMatch = reTimeRange.search(textFromPageZadnja)
        if timeRangeMatch:
            timeRange = timeRangeMatch.group('timeRange')

        #output string (cpap):
        output = "Vzrok pregleda: ambulantna kontrola " + kategorija + " terapije. \n" + \
        "Uvedba terapije: \n" + \
        "Veljavnost naročilnice: \n" + \
        "Dobavitelj: \n\n" + \
        "Tip aparata: " + aparat + ".\n" + \
        "Nastavitev:  " + deviceMode + ",\n " + \
        "            "+ minCpapPressure + " - " + maxCpapPressure + " cm vode, \n" + \
        "             A-Flex: " + aFlex + ".\n\n" + \
        "Tip maske: \n\n" + \
        "Podatki o rabi in učinkovitosti v zadnjih " + timeRange + " dneh:\n" + \
        "    - odstotek dni, ko aparat uporablja: " + percentDaysWithDeviceUsage + "%." + "\n" + \
        "    - odstotek dni, ko aparat uporablja več kot 4 h/noč: " + percentDaysWithUsageAtLeastFourHours + "%.\n" + \
        "    - povprečna uporaba (vsi dnevi): " + averageUsageAllDays + "\n" + \
        "    - povprečna uporaba (dnevi, ko aparat uporablja): " + averageUsageDaysUsed + "\n\n" + \
        "    - preveliko uhajanje zraka: " + largeLeak + "/noč.\n" + \
        "    - prekinitve dihanja v eni uri: AHI = " + ahi + "/h.\n\n" + \
        "Težave: \n\n" + \
        "Zaključek: \n\n" + \
        "Predvidena kontrola: \n" + \
        "Ambulantna kontrola, čez dve leti v Laboratoriju za motnje dihanja v spanju. " + \
        "Tri mesece prej nas pokličite, da se dogovorimo za termin. " + \
        "Dosegljivi smo od ponedeljka do petka med 9.00 in 11.00 na telefonski številki 04 2569 234. " + \
        "V primeru vprašanj ali težav nas pokličite predčasno."

    #----------BIPAP---------
    elif "BiPAP" in aparat and "SV" not in aparat:
        kategorija = "bipap"
        #---to do: nastavitev; leak; ahi

        #id pacienta
        reObjID = re.compile(r'Patient ID: (?P<idPacienta>\d*)')
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
        #ipap, epap setting
        reSetPressure = re.compile(r'ParameterValueIPAP Pressure(?P<ipapSetting>\d+) cmH2OEPAP Pressure(?P<epapSetting>\d+) cm')
        matchSetPressure = reSetPressure.search(textFromPageZadnja)
        if matchSetPressure:
            ipapSetting = matchSetPressure.group('ipapSetting')
            epapSetting = matchSetPressure.group('epapSetting')
        #backup rate
        reBackupRate = re.compile(r'Breath Rate(?P<backupRate>\d+)Timed')
        matchBackupRate = reBackupRate.search(textFromPageZadnja)
        if matchBackupRate:
            backupRate = matchBackupRate.group('backupRate')




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
        #date range
        reTimeRange = re.compile(r'Compliance Summary\d\d?\/\d\d?\/\d\d\d\d - \d\d?\/\d\d?\/\d\d\d\d \((?P<timeRange>\d*) days')
        timeRangeMatch = reTimeRange.search(textFromPageZadnja)
        if timeRangeMatch:
            timeRange = timeRangeMatch.group('timeRange')

        #output string - bipap:
        output = "Vzrok pregleda: ambulantna kontrola " + kategorija + " terapije. \n" + \
        "Uvedba terapije: \n" + \
        "Veljavnost naročilnice: \n" + \
        "Dobavitelj: \n\n" + \
        "Tip aparata: " + aparat + ".\n" + \
        "Nastavitev:  " + deviceMode + ",\n" + \
        "             IPAP: " + ipapSetting + " cm\n" + \
        "             EPAP: " + epapSetting + " cm\n" + \
        "             frekvenca: " + backupRate + "/min\n\n" + \
        "Tip maske: \n\n" + \
        "Podatki o rabi in učinkovitosti v zadnjih " + timeRange + " dneh:\n" + \
        "    - odstotek dni, ko aparat uporablja: " + percentDaysWithDeviceUsage + "%." + "\n" + \
        "    - odstotek dni, ko aparat uporablja več kot 4 h/noč: " + percentDaysWithUsageAtLeastFourHours + "%.\n" + \
        "    - povprečna uporaba (vsi dnevi): " + averageUsageAllDays + "\n" + \
        "    - povprečna uporaba (dnevi, ko aparat uporablja): " + averageUsageDaysUsed + "\n\n" + \
        "    - preveliko uhajanje zraka: " + largeLeak + "/noč.\n" + \
        "    - prekinitve dihanja v eni uri: AHI = " + ahi + "/h.\n\n" + \
        "Težave: \n\n" + \
        "Zaključek: \n\n" + \
        "Predvidena kontrola: \n" + \
        "Ambulantna kontrola, čez dve leti v Laboratoriju za motnje dihanja v spanju. " + \
        "Tri mesece prej nas pokličite, da se dogovorimo za termin. " + \
        "Dosegljivi smo od ponedeljka do petka med 9.00 in 11.00 na telefonski številki 04 2569 234. " + \
        "V primeru vprašanj ali težav nas pokličite predčasno."



    #----------ASV-----------
    elif "SV" in aparat:
        kategorija = "asv"

    print(textFromPageZadnja)

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
    print("device mode: ", deviceMode)
    print("cpap mean pressure: ", cpapMeanPressure)
    print("avg. time in large leak per day: ", largeLeak)
    print("avg. AHI: ", ahi)
    print("min CPAP pressure: ", minCpapPressure)
    print("max CPAP pressure: ", maxCpapPressure)
    print("a-flex: ", aFlex)
    print("datum: ", datum)
    print("time range: ", timeRange)
    #bipap:
    print("ipap setting: ", ipapSetting)
    print("epap setting: ", epapSetting)
    print("backup rate: ", backupRate)
    """
    #print(output)
    #write output into a new file:
    outputFileName = priimek + "_" + ime + "_" + idPacienta + ".txt"
    print(outputFileName)
    os.chdir(outPath)
    outputFile = open(outputFileName, 'w')
    outputFile.write(output)
    outputFile.close()

    """
    # todo:
    # - kategorija naj se doloci iz device moda - al pa, ce ne...
    # - asv, bipap kategorija
    # - spimpaj ure
    """
