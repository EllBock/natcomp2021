#!/usr/bin/python

import multiprocessing
import os
import time

CONFIG_FILE = r'single_race_wheel_1.xml'
STAGE = 2
TRACK = "forzawin"
TORCSDIR = r"C:\torcs"

def start_torcs(config_file, vision=False):
    print("Launch TORCS...")
    # Kill other instances
    #if "wtorcs" in (p.name() for p in psutil.process_iter()):
    #    os.system('tskill wtorcs')

    #time.sleep(0.5)

    print("Using " + config_file)
    print("CWD: " + os.getcwd())
    if vision is True:
        ret = os.system('wtorcs.exe -vision -t 100000 -r ' + config_file)
    else:
        ret = os.system('wtorcs -t 100000 -r ' + config_file)

    exit(ret)


def start_client(track, results=None):
    if results is None:
        ret = os.system(f"python2 client.py -s 2 -t {track}")
    else:
        ret = os.system(f"python2 client.py -s 2 -t {track} -R {results}")

    exit(ret)


if __name__ == '__main__':
    # creating multiple processes
    client = multiprocessing.Process(target=start_client, args=(TRACK))
    torcs = multiprocessing.Process(target=start_torcs, args=(CONFIG_FILE, False))

    # Start processes
    client.start()
    time.sleep(0.5)
    # Change the current working directory
    cwd = os.getcwd()
    os.chdir(TORCSDIR)
    torcs.start()
    os.chdir(cwd)
    # Waiting until client finishes
    torcs.join()
    print(torcs.exitcode)
    #if torcs.exitcode == TORCS_ERROR:
    #    client.kill()
    #    raise Exception("Server cannot start!")
    client.join()

    print("Il client e torcs hanno finito")
