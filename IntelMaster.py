#!/usr/bin/env python
#
# Developed by Pendrak0n
#
# Purpose: Manage updates from source feeds.py
#

import argparse
import os
import feeds
import hunt
from sys import exit


def run_modules():
    feeds.MDL_update()
    feeds.malc0de_update()
    feeds.feodo_update()
    feeds.alienvault_update()
    feeds.dshield_high_update()
    feeds.spyeye_tracker_update()
    feeds.palevo_tracker_update()

def ensure_dir():
    folder = 'intel'
    if not os.path.exists(folder):
        os.makedirs(folder)
        print '[+] Created new directory: intel'

def main():
    ensure_dir()
    os.chdir('intel')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--choice", type=str, choices=['list', 'update'], help="Choose menu option:\n\
    1. Show list of current feeds to update individually\n\
    2. Update all feeds")
    parser.add_argument('--search', type=str, nargs='?', const=1, help='Searches through Intel dir for provided IOCs')

    args = parser.parse_args()

    if args.search:
        ioc_file = args.search
        hunt.search(ioc_file)

    elif args.choice == 'update':
        print '[*] Updating all feeds'
        run_modules()
        print '[+] All Feeds Updated!'

    elif args.choice == 'list':
        print '[*] Please select feed to update:'
        feed_list = dir(feeds)
        newlist = []
        feedcount = 1
        for feed in feed_list:
            if "_update" in feed:
                newlist.append(feed)
                print str(feedcount)+'. '+feed
                feedcount += 1
            else:
                pass

        print '\n'
        choice = raw_input('Select feed by numerical ID (1-%d)\n> ' % (len(newlist)))
        if int(choice) in range(1, len(newlist) + 1):  # condition to check if proper feed was selected.
            mod = newlist[int(choice) - 1]   # Using choice number to locate item in the feed list
            methodToCall = getattr(feeds, mod)  # saving function to call with newlist item as variable
            methodToCall()
        else:
            print '[-] Invalid option. Exiting...'
            exit(0)


if __name__ == '__main__':
    main()
