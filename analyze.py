import csv

rdr = csv.DictReader(open('combined-data.csv'))

output = [[
    'county',
    'city',
    'pop change',
    'housing change',
    'units needed to get to 1990 ratio',
    'pct of change'
]]

cities = dict()

def stoi(v):
    return int(v.replace(',', ''))

for row in rdr:
    if row['date'] == '4/1/1990':
        cityKey = '{0}-{1}'.format(row['county'], row['city']).lower()
        cities[cityKey] = row
    elif row['date'] == '1/1/2017':
        cityKey = '{0}-{1}'.format(row['county'], row['city']).lower()
        if cityKey not in cities:
            continue
        pop1990 = stoi(cities[cityKey]['population'])
        hous1990 = stoi(cities[cityKey]['housing units'])
        ratio1990 = float(pop1990) / float(hous1990) if hous1990 > 0 else 0
        popChange = stoi(row['population']) - pop1990
        housChange = stoi(row['housing units']) - hous1990
        unitsNeeded = float(popChange) / ratio1990 if ratio1990 > 0 else 0
        output.append([
            row['county'],
            row['city'],
            popChange,
            housChange,
            unitsNeeded,
            unitsNeeded / float(housChange)
        ])

wrtr = csv.writer(open('ranked.csv', 'w'))
wrtr.writerows(output)
