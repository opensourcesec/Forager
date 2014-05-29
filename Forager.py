#!/usr/bin/env python
__author__ = 'pendrak0n'
#
# Purpose: Manage updates from source feeds.py
#

import argparse
import os
import hunt
import feeds
from feeds import *
from sys import exit


def run_modules():
    MDL_update()
    malc0de_update()
    feodo_update()
    alienvault_update()
    dshield_high_update()
    spyeye_tracker_update()
    palevo_tracker_update()
    nothink_malware_dns()
    nothink_malware_http()
    nothink_malware_irc()


def ensure_dir():
    folder = 'intel'
    if not os.path.exists(folder):
        os.makedirs(folder)
        print '[+] Created new directory: intel'


def main():
    ensure_dir()
    os.chdir('intel')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--feeds", type=str, choices=['list', 'update'], help="Manipulates intelligence feeds\n\
    List - Show list of current feeds to update individually\n\
    Update - Update all feeds")
    parser.add_argument('--hunt', action="store_true", help='Searches through the intel dir for matches')
    parser.add_argument('-s', type=str, nargs='?', help="Accepts a single IP address")
    parser.add_argument('-f', type=str, nargs='?', help="Receives a file of indicators to search through.")

    args = parser.parse_args()

    if args.hunt:
        if args.s:
            hunt.single_search(args.s)
        elif args.f:
            hunt.search_file(args.f)

    elif args.feeds == 'update':
        print '[*] Updating all feeds'
        run_modules()
        print '[+] All Feeds Updated!'

    elif args.feeds == 'list':
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

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
