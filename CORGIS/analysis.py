#!/usr/bin/env python3

import sys
from pprint import PrettyPrinter

from weather.data import weather
from weather.analysis import storage
from weather.analysis import visualization as vis

from geopy.geocoders import GoogleV3

raw_data = []
data = []
weather_objs = []
pprinter = PrettyPrinter()
geolocator = GoogleV3()

raw_data = weather.get_weather()
data = raw_data
weather_objs = [storage.Weather(datum) for datum in data]


def restrict_to_range(start=None, stop=None, step=None):
    data[:] = raw_data[start:stop:step]
    weather_objs[:] = [storage.Weather(datum) for datum in data]
    return len(data)


def restrict_by_latitude(latitude, tolerance=0):
    for weather_obj in weather_objs:
        if weather_obj.get_location() == None:
            weather_obj.set_location(geolocator)

    weather_objs[:] = storage.get_by_coords(weather_objs, latitude, tolerance)


def restrict_by_longitude(longitude, tolerance=0):
    for weather_obj in weather_objs:
        if weather_obj.get_location() == None:
            weather_obj.set_location(geolocator)

    storage.get_by_coords(weather_objs, longitude=longitude,
                          longitude_tolerance=tolerance)


def restrict_by_location(latitude, longitude, latitude_tolerance=0, longitude_tolerance=0):
    restrict_by_latitude(latitude, latitude_tolerance)
    restrict_by_longitude(longitude, longitude_tolerance)
    # for weather_obj in weather_objs:
    #     weather_obj.set_location(geolocator)
    #
    # storage.get_by_coords(weather_objs, latitude,
    #                       latitude_tolerance, longitude, longitude_tolerance)


def print_data():
    pprinter.pprint(data)


def plot_data(key, fit_line=True):
    vis.plot_over_time(weather_objs, key, fit_line)


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

    restrict_to_range(stop=int(sys.argv[2]))

    if command == 'struct':
        print_data()

    elif command == 'plot':
        plot_data(' '.join(sys.argv[3:]))

    elif command == 'loc':
        restrict_by_location(float(
            sys.argv[-4]), float(sys.argv[-2]), float(sys.argv[-3]), float(sys.argv[-1]))
        plot_data(' '.join(sys.argv[3:-4]))

    else:
        if command == 'lat':
            restrict_by_latitude(float(sys.argv[-2]), float(sys.argv[-1]))

        else:  # if command == 'long'
            restrict_by_longitude(float(sys.argv[-2]), float(sys.argv[-1]))

        plot_data(' '.join(sys.argv[3:-2]))


if __name__ == '__main__':
    main()
