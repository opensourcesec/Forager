__author__ = 'pendrak0n'
#
# When called, will search through Intel directory for each
# indicator in provided CSV or New-line formatted file.
#

import sys
import re
import os
from time import sleep

def search(ioc):
    os.chdir('../')
    patt = re.compile('[\b\w](?:[0-9]{1,3}\.){3}[0-9]{1,3}[\b\w]')

    print '[*] Searching for indicators from %s' % ioc
    if ioc[-3:] == 'csv':
        print '[*] Pulling indicators as CSV values'
    else:
        print '[*] Assuming new-line formatted file'
        try:
            f = open(ioc, 'r').readlines()
        except:
            print '[!] Cannot locate file: %s. \n\
            Please provide the full path.' % ioc
            exit(0)

        ioc_list = []
        for line in f:
            for match in patt.findall(line):
                ioc_list.append(match)

        sleep(2)
        os.chdir('intel')
        dir = os.listdir('.')

        total = float(len(f))
        oneperc = 1.0/total
        perc = 0.0
        matched = {}

        for item in ioc_list:
            for i in dir:
                contents = open(i, 'r').readlines()
                if item in contents:
                    matched.update(item, i)
                else:
                    pass
            perc += oneperc
            update_progress(perc)

        matched.items()


def update_progress(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rProgress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()