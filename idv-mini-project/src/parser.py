import requests
import csv
import io
import datetime
import pickle
import os

# ONLY FOR DEVELOPMENT!
# uses pickle to load an old data version instead of downloading the csv
# 4-5 times faster
use_lazy_load = False

data = {}


def _load_data():
    """
    Downloads and processes the CSV data.
    """
    for row in _get_csv_reader('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv'):
        code = row['CountryCode']
        del row['CountryCode']
        date = row['Date']
        del row['Date']
        name = row['CountryName']
        del row['CountryName']

        _add(code, date, name, row)

    for row in _get_csv_reader('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'):
        code = row['iso_code']
        del row['iso_code']
        date = ''.join(row['date'].split('-'))
        del row['date']
        name = row['location']
        del row['location']
        del row['continent']

        _add(code, date, name, row)


def _get_csv_reader(url):
    """
    Get the CSV from the url and return a CSV DictReader.
    """

    data_raw = requests.get(url).content.decode()
    data_file_obj = io.StringIO(data_raw)
    return csv.DictReader(data_file_obj)


def _add(code, date, name, row):
    """
    Adds the row to the data object.
    It follows the following format:
    data = {
        '<country-code>': {
            'name': '<country-name>',
            'rows': {
                '<date-string>': {
                    # whatever data we have
                }
            }
        }
    }
    The data is sanitized so that no empty-string data is saved.
    """

    row = {k: v for k, v in row.items() if v != ''}

    if data.get(code) == None:
        data[code] = {'rows': {}, 'name': name}

    if data[code]['rows'].get(date) == None:
        data[code]['rows'][date] = row
    else:
        _old_row = data[code]['rows'][date]
        data[code]['rows'][date] = {**_old_row, **row}


def _get_dates():
    """
    Returns an array of date object.
    The first date is the earliest for which data exists in the datasets,
    the last date is the latest (normally today).
    This ensures, that every day (between min and max) is present,
    even though there might be no data.
    """
    all_dates = set()

    for country in data:
        all_dates |= set(data[country]['rows'].keys())

    all_dates = sorted([int(x) for x in all_dates])

    def _get_date_from_int(d):
        year = int(str(d)[:4])
        month = int(str(d)[4:6])
        day = int(str(d)[6:])
        return datetime.date(year, month, day)

    min_date = _get_date_from_int(all_dates[0])
    max_date = _get_date_from_int(all_dates[-1])

    single_day = datetime.timedelta(days=1)

    result = []

    _current_date = min_date
    while _current_date <= max_date:
        result.append(_current_date)
        _current_date += single_day

    return result


def _get_date_key(date):
    """
    Returns a date object in the format the dates are used as keys in the data dict.
    """
    return date.strftime('%Y%m%d')


if use_lazy_load:
    if os.path.isfile('data.pkl'):
        with open('data.pkl', 'rb') as file:
            data = pickle.load(file)
            all_dates = pickle.load(file)
    else:
        _load_data()
        all_dates = _get_dates()
        with open('data.pkl', 'wb') as file:
            pickle.dump(data, file, pickle.HIGHEST_PROTOCOL)
            pickle.dump(all_dates, file, pickle.HIGHEST_PROTOCOL)
else:
    _load_data()
    all_dates = _get_dates()

number_of_dates = len(all_dates)
all_country_codes = list(data.keys())
number_of_countries = len(all_country_codes)
policy_names = [
    'School closing',
    'Workplace closing',
    'Cancel public events',
    'Restrictions on gatherings',
    'Close public transport',
    'Stay at home requirements',
    'Restrictions on internal movement',
    'International travel controls'
]


def get_countries():
    """
    Return all countries for which data exists.
    Returns a dict with:
    {
        '<country-code>': '<country-name>'
    }
    """
    result = {}

    for country_code in data:
        result[country_code] = data[country_code]['name']

    return result


def get_stringency_index_data_per_country():
    """
    Returns a dict with:
    {
        'dates': [<date_obj>, ...],
        'countries': {
            '<country-code>': [<stringency_index-value>, ...]
        }
    }
    For example, to plot the index (y-axis) over the date (x-axis) for Germany,
    you'd have arrays x and y as:
    ```
        data = get_worldmap_data()
        x = data['dates']
        y = data['countries']['DEU']
    ```
    The 'stringency_index' array always has the same length as the 'dates' array.
    Non-exitstent values in the 'stringency_index' are `None`.
    """
    result = {'dates': all_dates, 'countries': {}}

    for country_code in data:
        result['countries'][country_code] = [None] * number_of_dates

        for i, date_obj in enumerate(all_dates):
            _data_row = data[country_code]['rows'].get(_get_date_key(date_obj))
            if _data_row != None:
                _index = _data_row.get('StringencyIndex')
                if _index != None:
                    result['countries'][country_code][i] = float(_index)

    return result


def get_stringency_index_data_per_date():
    """
    Returns a dict with:
    {
        'dates': [<date_obj>, ...],
        'countries': [<country_code>, ...]
        'index_values': [
            [<index_for_country[0]>, ...] # indizes for dates[0]
            ...
        ]
    }
    """
    result = {
        'dates': all_dates,
        'countries': all_country_codes,
        'index_values': []
    }

    for date in all_dates:
        index_array = [None] * number_of_countries
        for j, country_code in enumerate(all_country_codes):
            _data_row = data[country_code]['rows'].get(_get_date_key(date))
            if _data_row != None:
                _index = _data_row.get('StringencyIndex')
                if _index != None:
                    index_array[j] = float(_index)
        result['index_values'].append(index_array)

    return result


def get_policy_data(country_code):
    """
    Returns a dict with:
    {
        'dates': [<date_obj>, ...],
        'policy_names': [<string>, ...],

        'policy_values': [
            [<policy_value>, ...] # value for each date (columns)
        ], # number of policies rows

        'total cases': [<value>, ...],
        'new cases': [<value>, ...],
        'total deaths': [<value>, ...],
        'new deaths': [<value> ...],
    }

    For example, to plot the total cases (y-axis) over the date (x-axis) for Germany,
    you'd have arrays x and y as:
    ```
        data = get_policy_data('DEU')
        x = data['dates']
        y = data['total cases']
    ```
    """
    policy_names_internal = [(f'C{i+1}_{name}', f'C{i+1}_Flag') for i, name in enumerate(policy_names)]

    other_properties = ['total cases', 'new cases', 'total deaths', 'new deaths']
    other_properties_internal = [name.replace(' ', '_') for name in other_properties]

    result = {
        'dates': all_dates,
        'policy_names': policy_names,
        'policy_values': [[None]*number_of_dates for _ in range(len(policy_names))]
    }

    for key in other_properties:
        result[key] = [None] * number_of_dates

    def to_number(x):
        if x == None:
            return
        if '.' in str(x):
            return float(x)
        else:
            return int(x)

    for i, date_obj in enumerate(all_dates):
        _data_row = data[country_code]['rows'].get(_get_date_key(date_obj))
        if _data_row != None:
            for j, (internal_name, _) in enumerate(policy_names_internal):
                result['policy_values'][j][i] = to_number(_data_row.get(internal_name))
            for key, internal_name in zip(other_properties, other_properties_internal):
                result[key][i] = to_number(_data_row.get(internal_name))

    return result


def get_policy_list():
    return policy_names
