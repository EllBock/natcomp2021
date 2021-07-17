#!/usr/bin/python

import multiprocessing
import os
import time
from config import PROJECTDIR, TORCSDIR

CONFIG_FILE = os.path.join(PROJECTDIR, "raceconfigs", "forza", "forza-inferno-0.xml")
TRACK = "forzawin"
STAGE = 2
TORCS_ERROR = 1

def start_torcs(config_file, vision=False):
    print("Launch TORCS.")
    print("Using " + config_file)

    # Change the current working directory
    os.chdir(TORCSDIR)

    if vision is True:
        ret = os.system('wtorcs.exe -vision -p 3002 -t 100000 -r ' + config_file)
    else:
        ret = os.system('wtorcs -t 100000 -p 3002 -r ' + config_file)

    exit(ret)


def start_client(track, results=None):
    print("Launch Client.")
    if results is None:
        ret = os.system(f"python2 client.py -p 3002 -s 2 -t {track}")
    else:
        ret = os.system(f"python2 client.py -p 3002 -s 2 -t {track} -R {results}")
    exit(ret)


if __name__ == '__main__':
    # creating multiple processes
    client = multiprocessing.Process(target=start_client, args=(TRACK, ))
    client.start()

    torcs = multiprocessing.Process(target=start_torcs, args=(CONFIG_FILE, False), name='primoTorcs')
    torcs.start()

    # Waiting until TORCS finishes
    torcs.join()
    if torcs.exitcode == TORCS_ERROR:
        client.kill()
        raise Exception("Server cannot start!")

    # Waiting until client finishes
    client.join()

    print("Il client e torcs hanno finito")
