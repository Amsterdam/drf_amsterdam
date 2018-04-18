import os
from datetime import datetime
from decimal import Decimal

from datasets.models.temperature import WeatherStation, TemperatureRecord


def read_csv(filename):
    parsed_data = []
    station_numbers = set()

    with open(filename, 'r', encoding='cp1252') as f:
        # look for start of data
        for line in f:
            split_line = line.split(',')
            if split_line[0] == 'STN':
                break

        # grab temperature records
        for line in f:
            split_line = line.split()
            if len(split_line) != 3:
                continue

            station_number = int(split_line[0])
            date = datetime.strptime(split_line[1], '%Y%m%d').date()
            temperature = Decimal(split_line[2])

            station_numbers.add(station_number)
            parsed_data.append((station_number, date, temperature))

    return parsed_data, station_numbers


def import_temperature(data_dir):
    """
    Parse a KNMI weather station data file.
    """
    temperature_csv = os.path.join(data_dir, 'tg_hom_mnd260.txt')
    parsed_data, station_numbers = read_csv(temperature_csv)

    # create weather station instances
    cache = {}
    for n in station_numbers:
        s, created = WeatherStation.objects.get_or_create(number=n)
        cache[n] = s

    # create temperature records
    try:
        temperature_records = []
        for station_number, date, temperature in parsed_data:
            station = cache[station_number]
            temperature_records.append(TemperatureRecord(
                station=station,
                date=date,
                temperature=temperature
            ))
        qs = TemperatureRecord.objects.bulk_create(
            temperature_records, batch_size=499)
    except:
        raise
