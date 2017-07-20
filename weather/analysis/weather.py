#!/usr/bin/env python3

import pickle


class Weather:
    # cache = 'locations.txt'

    def __init__(self, *args, **kwargs):
        self._set_data(args[0])
        self._location = None

        if len(args) == 2:
            location = self.get_data('Location')
            # with open(self.__class__.cache, 'a+') as cache:
            #     cache.seek(0)
            #     for line in cache:
            #         if location in line:
            #             self._location = args[1].geocode(
            #                 line[line.index(':') + 1:])
            #             break
            #     else:
            #         cache.write('{}: ')

            self._location = args[1].geocode(location)

    def _set_data(self, data):
        for (k, v) in data.items():
            if isinstance(v, dict):
                self._set_data(v)
            else:
                setattr(self, '_{}'.format(k.lower().replace(' ', '_')), v)

    def get_data(self, k):
        return getattr(self, '_{}'.format(k.lower().replace(' ', '_')))

    def get_location(self):
        return self._location


# def get_by_location_attr(weather_objs, location_attr, value):
#     new_weather_objs = []
#     for weather_obj in weather_objs:
#         if value == getattr(weather_obj.get_location(), location_attr):
#             new_weather_objs.append(weather_obj)
#
#     return new_weather_objs


def get_by_coords(weather_objs, latitude=0, latitude_tolerance=90, longitude=0,
                  longitude_tolerance=180):
    new_weather_objs = []
    for weather_obj in weather_objs:
        location = weather_obj.get_location()
        if (latitude - latitude_tolerance <= location.latitude <= latitude
            + latitude_tolerance and longitude - longitude_tolerance
                <= location.longitude <= longitude + longitude_tolerance):
            new_weather_objs.append(weather_obj)

    return new_weather_objs
