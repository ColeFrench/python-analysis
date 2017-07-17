#!/usr/bin/env python3

import sys
import pprint

import weather.data.weather as weather_data
from weather.analysis import weather
from weather.analysis import visualization as vis


def limit_data(data, num_samples):
    """
    Mutates data by removing all except the first num_samples elements.

    data: a list
    num_samples: an int >= 0 and < len(data)
    """
    data[:] = [data[n] for n in range(num_samples)]
    return len(data)


def main():
    data = weather_data.get_weather()
    limit_data(data, int(sys.argv[1]))

    if len(sys.argv) >= 3:
        weather_objs = [weather.Weather(sample) for sample in data]
        vis.plot(weather_objs, [weather_obj.get_data(
            ' '.join(sys.argv[2:])) for weather_obj in weather_objs])
    else:
        pp = pprint.PrettyPrinter()
        pp.pprint(data)


if __name__ == '__main__':
    main()
