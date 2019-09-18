import csv
import os

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

############################################################
############# ETL pre 2010 files #############
############################################################

def addPre2010Row(filename, county, city, row):
    output.append([
        county,
        city,
        row[1],
        row[2],
        row[5],
        row[6],
        row[7],
        row[8],
        row[9],
        row[10 if filename == '1990-2000.csv' else 11]
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
############# ETL post 2010 files #############
############################################################

def addPost2010Row(county, year, row):
    output.append([
        county,
        row[0].strip().replace('Incorporated Total', 'Incorporated'),
        "1/1/{0}".format(year),
        row[1],
        row[4],
        int(row[5].replace(',', '')) + int(row[6].replace(',', '')),
        int(row[7].replace(',', '')) + int(row[8].replace(',', '')),
        row[9],
        row[10],
        row[11]
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
                addPost2010Row(curCounty, year, row)
            elif row[0].strip() == '':
                continue
            else:
                addPost2010Row(curCounty, year, row)
        else:
            if row[0] == '':
                continue
            else:
                collectingCountyData = True
                curCounty = row[0].strip().replace(' County', '')

# write all data to one file
wrtr = csv.writer(open('combined-data.csv', 'w'))
wrtr.writerows(output)