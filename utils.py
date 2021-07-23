#!/usr/bin/python

import csv
import matplotlib.pyplot as plt
import numpy as np


FILENAME = "results/forza_1.csv"

SNAKEOIL = r"/home/ellbock/Workbench/natcomp2021/comparisons/SnakeOil-Forza.csv"
UNISAOIL = r"/home/ellbock/Workbench/natcomp2021/comparisons/UnisaOil-Forza.csv"

# MAIN 1
KEYS = [
        # 'iteration',
        # 'curLapTime',
        # 'lastLapTime',
        #'raceTime',
        # 'stucktimer',
        #'damage',
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

LABELS = {'speed': 'Speed [km/h]',
          'distRaced': 'Distance [km]',
          'damage': 'Damage',
          'speedFromDist': 'Speed along the track [km/h]',
          'raceTime': 'Time [s]'}



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
    csv_col_dict['lap'] = []
    lap = 1
    csv_col_dict['lap'].append(lap)

    for i in range(1, len(csv_col_dict['curLapTime'])):
        if csv_col_dict['curLapTime'][i] < csv_col_dict['curLapTime'][i-1]:
            delta += csv_col_dict['lastLapTime'][i]
            lap += 1

        csv_col_dict['raceTime'].append(csv_col_dict['curLapTime'][i] + delta)
        csv_col_dict['lap'].append(lap)

    return csv_col_dict

def calculate_speed_by_distance(csv_col_dict: dict):
    space = np.array(csv_col_dict['distRaced'])
    time = np.array(csv_col_dict['raceTime'])

    d_space = space[1:] - space[:len(space)-1]
    d_time = time[1:] - time[:len(time) - 1]

    speed = d_space/d_time
    speed = np.append(0., speed)
    csv_col_dict['speedFromDist'] = list(speed * 3.6)
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


def main1(filename):
    d = csv_to_column_dict(filename)
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

    score = total_time + alpha * damage + beta * offroad
    print(f"Score: {score}")

    i = 0
    for key in KEYS:
        i += 1
        plt.figure(i)
        plt.plot(d['distRaced'], d[key])
        plt.xlabel('distRaced')
        plt.ylabel(key)

    plt.show()



def main2(fname1, fname2, keys, labels):
    """
    Primo snakeoil, secondo Unisaoil
    """
    d = []
    d.append(csv_to_column_dict(fname1))
    d.append(csv_to_column_dict(fname2))

    for i in range(len(d)):
        d[i] = calculate_effective_speed(d[i])
        d[i] = calculate_race_time(d[i])
        d[i] = calculate_speed_by_distance(d[i])

    print(f"Offroad SnakeOil: {calculate_offroad_time(d[0])}")
    print(f"Offroad UnisaOil: {calculate_offroad_time(d[1])}")

    #plt.figure(1)
    #plt.plot(d[0]['distRaced'], d[0]['speed'], label='SnakeOil')
    #plt.plot(d[1]['distRaced'], d[1]['speed'], label='UnisaOil')
    #plt.xlabel(labels['distRaced'])
    #plt.ylabel(labels['speed'])
    #plt.legend()

    plt.figure(2)
    plt.plot(d[0]['raceTime'], d[0]['speedFromDist'], label='SnakeOil')
    plt.plot(d[1]['raceTime'], d[1]['speedFromDist'], label='UnisaOil')
    plt.xlabel(labels['raceTime'])
    plt.ylabel(labels['speedFromDist'])
    plt.legend()
    #plt.savefig('unisavssnake-forza-time.pdf', format='pdf')

    plt.figure(3)
    plt.plot(d[0]['distRaced'], d[0]['speedFromDist'], label='SnakeOil')
    plt.plot(d[1]['distRaced'], d[1]['speedFromDist'], label='UnisaOil')
    plt.xlabel(labels['distRaced'])
    plt.ylabel(labels['speedFromDist'])
    plt.legend()
    #plt.savefig('unisavssnake-etrack4-dist.pdf', format='pdf')

    plt.show()

if __name__ == "__main__":
    #main1(FILENAME)
    main2(SNAKEOIL, UNISAOIL, KEYS, LABELS)
