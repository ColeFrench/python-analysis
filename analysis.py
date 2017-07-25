#!/usr/bin/env python3

import sys

from weather.data import weather
from weather.analysis import storage
from weather.analysis import visualization as vis

from geopy.geocoders import GoogleV3


def limit_data(data, num_samples):
    data[:] = [data[n] for n in range(num_samples)]
    return len(data)


def main():
    if len(sys.argv) < 2:
        raise SyntaxError('too few program arguments')

    # A dictionary of commands mapped to the additional arguments they require.
    commands = {
        'plot': 2,
        'loc': 6,
        'lat': 4,
        'long': 4,
        'struct': 1
    }

    command = sys.argv[1]
    if command not in commands:
        raise SyntaxError('invalid command')

    if len(sys.argv) < commands[command] + 2:
        raise SyntaxError('too few command arguments')

    data = weather.get_weather()
    limit_data(data, int(sys.argv[2]))

    if command == 'struct':
        from pprint import PrettyPrinter
        PrettyPrinter().pprint(data)

    elif command == 'plot':
        weather_objs = [storage.Weather(sample) for sample in data]
        key = ' '.join(sys.argv[3:])
        vis.plot_over_time(weather_objs, key, True)

    else:
        geolocator = GoogleV3()
        weather_objs = [storage.Weather(sample, geolocator) for sample in data]

        if command == 'loc':
            key = ' '.join(sys.argv[3:-4])
            weather_objs = storage.get_by_coords(weather_objs, float(
                sys.argv[-4]), float(sys.argv[-3]), float(sys.argv[-2]), float(sys.argv[-1]))

        else:
            key = ' '.join(sys.argv[3:-2])
            if command == 'lat':
                weather_objs = storage.get_by_coords(
                    weather_objs, float(sys.argv[-2]), float(sys.argv[-1]))

            else:  # if command == 'long'
                weather_objs = storage.get_by_coords(weather_objs, longitude=float(
                    sys.argv[-2]), longitude_tolerance=float(sys.argv[-1]))

        vis.plot_over_time(weather_objs, key, True)


if __name__ == '__main__':
    main()
