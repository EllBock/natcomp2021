#!/usr/bin/python

import multiprocessing
import os
import time
import psutil

CONFIG_FILE = r'single_race_wheel_1.xml'


def start_torcs(config_file, vision=False):
    print("Launch TORCS...")
    # Kill other instances
    if "wtorcs" in (p.name() for p in psutil.process_iter()):
        os.system('tskill wtorcs')

    time.sleep(0.5)

    print("Using " + config_file)
    print("CWD: " + os.getcwd())
    if vision is True:
        os.system('wtorcs.exe -vision -t 100000 -r ' + config_file)
    else:
        os.system('wtorcs -t 100000 -r ' + config_file)
    time.sleep(0.5)


def start_client():
    os.system('python2 client.py')


if __name__ == '__main__':
    # creating multiple processes
    client = multiprocessing.Process(target=start_client)
    torcs = multiprocessing.Process(target=start_torcs, args=(CONFIG_FILE, False))

    # Start processes
    client.start()
    time.sleep(0.5)
    # Change the current working directory
    os.chdir('C:\\Program Files (x86)\\torcs')
    torcs.start()

    # Waiting until client finishes
    client.join()
    torcs.join()
    print("Il client e torcs hanno finito")
