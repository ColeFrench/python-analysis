#!/usr/bin/env python3

from datetime import datetime
from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import date2num


def plot_over_time(weather_objs, key, fit_line=False):
    """
    Plots weather data against time and optionally a linear line of best fit.

    weather_objs: an iterable of Weather objects
    key: the key of the desired values to be plotted; a string
    fit_line: whether a line of best fit should be plotted
    """
    data = np.array([weather_obj.get_data(key)
                     for weather_obj in weather_objs])
    dates = [weather_obj.get_data('Full') for weather_obj in weather_objs]
    dates = [datetime.strptime(date, '%m-%d-%Y') for date in dates]
    dates = np.array(date2num(dates))

    plt.plot_date(dates, data)
    plt.title('{} Over Time'.format(key))
    plt.xlabel('Date')
    plt.ylabel('Value')

    if fit_line:
        plt.plot(dates, np.poly1d(np.polyfit(dates, data, 1))(dates), 'r')

    plt.savefig('corgis_{}.png'.format(key.replace(' ', '_').lower()), transparent=True, bbox_inches='tight')
    plt.show()
