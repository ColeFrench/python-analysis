#!/usr/bin/env python3

from datetime import datetime
from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num


def plot(weather_objs, values):
    """
    Averages values per date and then plots them as a function of time.

    weather_objs: a list of Weather objects
    values: a list of values to plot
    """
    dates = [weather_obj.get_data('Full') for weather_obj in weather_objs]
    dates = [datetime.strptime(date, '%m-%d-%Y') for date in dates]
    dates = date2num(dates)
    dates_length = len(dates)
    dates_to_values = OrderedDict.fromkeys(dates, 0.0)
    date_values = []

    for n in range(dates_length):
        date_values.append(values[n])
        if (n == dates_length - 1) or (dates[n] != dates[n + 1]):
            dates_to_values[dates[n]] = sum(date_values) / len(date_values)
            date_values = []

    plt.plot_date(list(dates_to_values.keys()), list(dates_to_values.values()))
    plt.show()
