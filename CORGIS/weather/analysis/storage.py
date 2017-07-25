#!/usr/bin/env python3

import shelve


class Weather:
    db_path = 'locations'

    def __init__(self, *args, **kwargs):
        self._set_data(args[0])
        self._geolocation = None

        if len(args) == 2:
            self.set_location(args[1])

    def _set_data(self, data):
        for (k, v) in data.items():
            if isinstance(v, dict):
                self._set_data(v)
            else:
                setattr(self, '_{}'.format(k.lower().replace(' ', '_')), v)

    def get_data(self, k):
        return getattr(self, '_{}'.format(k.lower().replace(' ', '_')))

    def get_location(self):
        return self._geolocation

    def set_location(self, geolocator):
        location = self.get_data('Location')
        with shelve.open(self.__class__.db_path) as db:
            if location in db:
                self._geolocation = db[location]

            else:
                self._geolocation = geolocator.geocode(location)
                db[location] = self._geolocation


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
