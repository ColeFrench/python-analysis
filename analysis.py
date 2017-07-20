#!/usr/bin/env python3

import sys
import pprint

import weather.data.weather as weather_data
from weather.analysis import weather
from weather.analysis import visualization as vis

from geopy.geocoders import Nominatim


def limit_data(data, num_samples):
    data[:] = [data[n] for n in range(num_samples)]
    return len(data)


def main():
    data = weather_data.get_weather()
    limit_data(data, int(sys.argv[2]))
    cmd = sys.argv[1]

    if cmd == 'plot':
        weather_objs = [weather.Weather(sample) for sample in data]
        trait = ' '.join(sys.argv[3:])
        vis.plot_over_time(weather_objs, [weather_obj.get_data(trait)
                                          for weather_obj in weather_objs], trait, True)
    elif cmd == 'latitude':
        geolocator = Nominatim()
        weather_objs = [weather.Weather(sample, geolocator) for sample in data]
        trait = ' '.join(sys.argv[3:-2])
        weather_objs = weather.get_by_coords(
            weather_objs, int(sys.argv[-2]), float(sys.argv[-1]))
        vis.plot_over_time(weather_objs, [weather_obj.get_data(trait)
                                          for weather_obj in weather_objs], trait, True)

    elif cmd == 'structure':
        pp = pprint.PrettyPrinter()
        pp.pprint(data)


if __name__ == '__main__':
    main()
