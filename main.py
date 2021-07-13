#!/usr/bin/python

import csv
import matplotlib.pyplot as plt
import numpy as np

FILENAME = "results/210712-154723.csv"
KEYS = [
        # 'iteration',
        # 'curLapTime',
        # 'lastLapTime',
        'raceTime',
        # 'stucktimer',
        'damage',
        # 'distRaced',
        # 'distFromStart',
        # 'racePos',
        # 'z',
        # 'speedZ',
        # 'speedY',
        # 'speedX',
        'speed',
        # 'targetSpeed',
        # 'rpm',
        # 'skid',
        # 'slip',
        # 'trackPos',
        # 'angle',
        ]


def csv_to_column_dict(filename: str):

    out = {}

    with open(filename, "r") as csvfile:
        rdr = csv.reader(csvfile)

        first_row = True
        keys = None

        for row in rdr:
            # Gets the keys for the dictionary
            if first_row:
                keys = row
                for key in keys:
                    out[key] = []
                first_row = False
            # Adds values to the lists in the dictionary
            else:
                for j in range(len(keys)):
                    key = keys[j]
                    value = float(row[j])
                    out[key].append(value)

    return out


def calculate_effective_speed(csv_col_dict: dict):
    csv_col_dict['speed'] = []
    for i in range(len(csv_col_dict['speedX'])):
        # velocity in the three cartesian components
        v_comp = [csv_col_dict['speedX'][i],
                  csv_col_dict['speedY'][i],
                  csv_col_dict['speedZ'][i]]
        v = np.linalg.norm(v_comp)
        csv_col_dict['speed'].append(v)
    return csv_col_dict


def calculate_race_time(csv_col_dict: dict):
    delta = .0
    csv_col_dict['raceTime'] = []
    csv_col_dict['raceTime'].append(csv_col_dict['curLapTime'][0])

    for i in range(1, len(csv_col_dict['curLapTime'])):
        if csv_col_dict['curLapTime'][i] < csv_col_dict['curLapTime'][i-1]:
            delta += csv_col_dict['lastLapTime'][i]
        csv_col_dict['raceTime'].append(csv_col_dict['curLapTime'][i] + delta)

    return csv_col_dict


def calculate_offroad_time(csv_col_dict: dict):
    trackPos = np.array(csv_col_dict['trackPos'])
    time = np.array(csv_col_dict['raceTime'])

    mask = np.greater(np.abs(trackPos), np.ones_like(trackPos)).astype('uint8')
    mask[-1] = 0
    rshift_mask = mask.take(np.insert(np.arange(mask.shape[0]-1), 0, 0))

    mask = np.abs(mask - rshift_mask)
    indices = list(np.nonzero(mask)[0])
    offroad_time = 0
    while len(indices) > 0:
        a = indices.pop()
        b = indices.pop()
        offroad_time += time[a] - time[b]

    return offroad_time


if __name__ == "__main__":
    d = csv_to_column_dict(FILENAME)
    d = calculate_effective_speed(d)
    d = calculate_race_time(d)

    total_time = d['raceTime'][-1]
    damage = d['damage'][-1]
    offroad = calculate_offroad_time(d)
    print(f"Time: {total_time}")
    print(f"Damage: {damage}")
    print(f"Offroad: {offroad}")

    alpha = 0.25
    beta = 1
    score = total_time + alpha*damage + beta*offroad
    print(f"Score: {score}")

    i = 0
    for key in KEYS:
        i += 1
        plt.figure(i)
        plt.plot(d['distRaced'], d[key])
        plt.xlabel('distRaced')
        plt.ylabel(key)

    plt.show()

