#!/usr/bin/env python3

import sys
import matplotlib.pyplot as plt


def main():
    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    years = []
    changes = []

    with open('GLB.Ts.txt') as data:
        reading = False
        for line in data:
            if reading:
                if line.find('Divide') == 0:
                    break

                split = line.split()
                if len(split) >= 2 and line.find('Year') != 0:
                    years.append(split[0])
                    changes.append(split[months[sys.argv[1]]])

            elif line.find('Year') == 0:
                reading = True

    plt.plot(years, changes)
    plt.title('Changes in Temperature by Hundredths of Degrees Celsius in {} Over Time'.format(
        sys.argv[1]))
    plt.xlabel('Year')
    plt.ylabel('Change in Temperature\n(Hundredth of a Degree Celsius)')
    plt.savefig('nasa_{}.png'.format(sys.argv[1].lower()), transparent=True, bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    main()
