import csv
import os

############################################################
# This script processes the extracted csv data and outputs
# the data into the combined-data.csv file.
############################################################

output = [[
    "county",
    "city",
    "date",
    "population",
    "housing units",
    "single family",
    "Multi-family",
    "mobile homes",
    "occupied",
    "vacancy rate"
]]

def parseNumberWithCommas(s):
    return int(s.replace(',', ''))

############################################################
############# ETL pre 2010 files #############
############################################################

def addPre2010Row(filename, county, city, row):
    if (row[1] == '1/1/2010'):
        return
    output.append([
        county, # county
        city, # city
        row[1], # date
        row[2], # population
        row[5], # housing units
        row[6], # single family
        row[7], # multi family
        row[8], # mobile homes
        row[9], # occupied
        row[10 if filename == '1990-2000.csv' else 11] # vacancy rate
    ])

for file in ['1990-2000.csv', '2000-2010.csv']:
    rdr = csv.reader(open(os.path.join('extracted-to-csv', file)))

    searchingForFirstCity = True
    lastRowWasNewCity = False

    curCity = ''
    curCounty = ''

    for row in rdr:
        if searchingForFirstCity:
            if row[0] == 'California':
                searchingForFirstCity = False
            else:
                continue

        if curCounty == '' and row[0] != curCounty:
            lastRowWasNewCity = True
            curCounty = row[0]
        elif row[0] == '':
            if row[1] == '':
                curCounty = ''
                lastRowWasNewCity = False
                continue
            elif row[1].find('4/1/2') > -1:
                continue
            else:
                addPre2010Row(file, curCounty, curCity, row)
        elif lastRowWasNewCity:
            lastRowWasNewCity = False
            curCity = row[0]
            if lastRow[1].find('4/1/2') == -1:
                addPre2010Row(file, curCounty, curCity, lastRow)
            addPre2010Row(file, curCounty, curCity, row)

        lastRow = row

############################################################
############# ETL 2010-2019 files #############
############################################################

def add2010sRow(county, year, row):
    output.append([
        county, # county
        row[0].strip().replace('Incorporated Total', 'Incorporated'), # city
        "1/1/{0}".format(year), # date
        row[1], # population
        row[4], # housing units
        parseNumberWithCommas(row[5]) + parseNumberWithCommas(row[6]), # single family
        parseNumberWithCommas(row[7]) + parseNumberWithCommas(row[8]), # multi family
        row[9], # mobile homes
        row[10], # occupied
        row[11] # vacancy rate
    ])

for n in range(0, 10):
    year = '201{0}'.format(n)
    file = os.path.join('extracted-to-csv', '201{0}.csv'.format(n))
    rdr = csv.reader(open(file))

    searchingForFirstCity = True
    collectingCountyData = False

    curCounty = ''

    for row in rdr:
        if searchingForFirstCity:
            if row[0] == 'Alameda County':
                searchingForFirstCity = False
                curCounty = row[0].strip().replace(' County', '')
                collectingCountyData = True
                continue
            else:
                continue

        if collectingCountyData:
            if row[0].strip() == 'County Total' or row[0].strip() == 'San Francisco':
                collectingCountyData = False
                add2010sRow(curCounty, year, row)
            elif row[0].strip() == '':
                continue
            else:
                add2010sRow(curCounty, year, row)
        else:
            if row[0] == '':
                continue
            else:
                collectingCountyData = True
                curCounty = row[0].strip().replace(' County', '')

############################################################
############# ETL post 2020 files #############
############################################################

for year in range(2020, 2022):
    file = os.path.join('extracted-to-csv', '{0}.csv'.format(year))
    rdr = csv.reader(open(file))

    searchingForFirstCity = True

    for row in rdr:
        if searchingForFirstCity:
            if row[0] == 'Alameda ':
                searchingForFirstCity = False
            else:
                continue

        if row[0] == '':
            continue

        output.append([
            row[0].strip(), # county
            row[1].strip(), # city
            "1/1/{0}".format(year), # date
            row[2], # population
            row[5], # housing units
            parseNumberWithCommas(row[6]) + parseNumberWithCommas(row[7]), # single family
            parseNumberWithCommas(row[8]) + parseNumberWithCommas(row[9]), # multi family
            row[10], # mobile homes
            row[11], # occupied
            row[12] # vacancy rate
        ])

# write all data to one file
wrtr = csv.writer(open('combined-data.csv', 'w'))
wrtr.writerows(output)