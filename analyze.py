import csv

rdr = csv.DictReader(open('combined-data.csv'))

header_row = [
    'county',
    'city',
    'end year population',
    'pop change',
    'housing change',
    'additional people per additional housing unit',
    'units needed to get to begin year population to housing unit ratio',
    'pct of change'
]

output_1990_to_present = [header_row]
output_most_recent_year = [header_row]

cities1990 = dict()
cities_last_year = dict()

last_year_date = '1/1/2017'
most_recent_date = '1/1/2018'

def stoi(v):
    return int(v.replace(',', ''))

def compare_years (city_key, lookup, current_year, output):
    if city_key in lookup:
        past_year = lookup[city_key]
    else:
        return
    pop_past = stoi(past_year['population'])
    hous_past = stoi(past_year['housing units'])
    ratio_past = float(pop_past) / float(hous_past) if hous_past > 0 else 0
    pop_cur_year = stoi(current_year['population'])
    pop_change = pop_cur_year - pop_past
    housing_unit_change = stoi(current_year['housing units']) - hous_past
    unitsNeeded = float(pop_change) / ratio_past - housing_unit_change if ratio_past > 0 else 0
    output.append([
        current_year['county'],
        current_year['city'],
        pop_cur_year,
        pop_change,
        housing_unit_change,
        pop_change / float(housing_unit_change) if housing_unit_change != 0 else 0,
        unitsNeeded,
        unitsNeeded / float(housing_unit_change) if housing_unit_change > 0 else 999999
    ])

for row in rdr:
    city_key = '{0}-{1}'.format(row['county'], row['city']).lower()
    if row['date'] == '4/1/1990':
        cities1990[city_key] = row
    elif row['date'] == last_year_date:
        cities_last_year[city_key] = row
    elif row['date'] == most_recent_date:
        compare_years(city_key, cities1990, row, output_1990_to_present)
        compare_years(city_key, cities_last_year, row, output_most_recent_year)

wrtr = csv.writer(open('ranked-1990-2018.csv', 'w'))
wrtr.writerows(output_1990_to_present)

wrtr = csv.writer(open('ranked-most-recent-year.csv', 'w'))
wrtr.writerows(output_most_recent_year)
