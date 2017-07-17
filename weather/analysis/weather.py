#!/usr/bin/env python3


class Weather:
    def __init__(self, data):
        self._set_data(data)

    def _set_data(self, data):
        for (k, v) in data.items():
            if isinstance(v, dict):
                self._set_data(v)
            else:
                setattr(self, '_{}'.format(k.lower().replace(' ', '_')), v)

    def get_data(self, k):
        return getattr(self, '_{}'.format(k.lower().replace(' ', '_')))
