#!/usr/bin/env python
__author__ = '0xnix'

#
# Main
#

#stdlib
import argparse
import os
from sys import exit
from threading import Thread, activeCount
from time import sleep
#local
from bin.hunt import single_search, search_file
from bin.feeds import FeedModules
from bin.tools import extract, update_progress
from bin.cb_tools import CB_gen, run_feed_server


def run_modules():
    x = FeedModules()
    threads = []
    for i in dir(x):
        if i.endswith('_update'):
            mod = getattr(x, i)
            threads.append(Thread(target=mod, name='%s' % i))
        else:
            pass

    for t in threads:
        t.start()
        print 'Initialized: %s' % t.name

    sleep(3)
    stat = 0.0
    total = float(len(threads))

    tcount = activeCount()
    while tcount > 1:
        stat = total - float(activeCount()) + 1.0
        prog = stat/total
        update_progress(prog)
        tcount = activeCount()
        sleep(1)
    print '[+] Feed collection finished!'


def ensure_dir():
    folder = 'intel'
    if not os.path.exists(folder):
        os.makedirs(folder)
        print '[+] Created new directory: intel'


def main():
    banner = '''     ______  ______   ______   ______   ______   ______   ______
    /\  ___\/\  __ \ /\  == \ /\  __ \ /\  ___\ /\  ___\ /\  == \\
    \ \  __\\\\ \ \/\ \\\\ \  __< \ \  __ \\\\ \ \__ \\\\ \  __\\ \\ \\  __<
     \ \_\   \ \_____\\\\ \_\ \_\\\\ \_\ \_\\\\ \_____\\\\ \_____\\\\ \\_\\ \\_\\
      \/_/    \/_____/ \/_/ /_/ \/_/\/_/ \/_____/ \/_____/ \/_/ /_/
    '''

    print banner


    feedmods = FeedModules()
    ensure_dir()
    os.chdir('intel')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--feeds", type=str, choices=['list', 'update'], help="Manipulates intelligence feeds\n\
    List - Show list of current feeds to update individually\n\
    Update - Update all feeds")
    parser.add_argument('--hunt', action="store_true", help='Searches through the intel dir for matches')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-s', type=str, nargs='?', help="Accepts a single IP address")
    group2.add_argument('-f', type=str, nargs='?', help="Receives a file of indicators to search through.")
    parser.add_argument("--extract", type=str, nargs=1, help="Extracts indicators from a given file")
    parser.add_argument("--cbgen", action="store_true", help="Generates alliance feeds for CarbonBlack. (Requires cbfeeds be present in bin dir)")
    parser.add_argument('--srv', type=str, choices=['thr', 'daemon'], help="Runs feed server\n\
    daemon - Daemonizes server process")


    args = parser.parse_args()

    if args.hunt:
        if args.s:
            single_search(args.s)
        elif args.f:
            search_file(args.f)

    elif args.feeds == 'update':
        print '[*] Updating all feeds'
        run_modules()

    elif args.feeds == 'list':
        print '[*] Please select feed to update:'
        feed_list = dir(FeedModules)
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
            methodToCall = getattr(feedmods, mod)  # saving the function with newlist argument as variable
            methodToCall()
        else:
            print '[-] Invalid option. Exiting...'
            exit(0)

    elif args.extract:
        os.chdir('../')
        filename = args.extract[0]
        print '[*] Extracting indicators from %s' % filename
        extract(filename)

    elif args.cbgen:
        os.chdir('../')
        CB_gen()
        if args.srv:
            http_thr = Thread(target=run_feed_server(), name='Feed_server')
            if args.daemon:
                http_thr.daemon = True
            http_thr.start()
        exit(0)

    elif args.srv:
        if args.srv == 'thr':
            thr = Thread(target=run_feed_server(), name='Feed_server')
            thr.start()
            thr.join()
        elif args.srv == 'daemon':
            thr = Thread(target=run_feed_server(), name='Feed_server')
            if args.daemon:
                thr.daemon = True
            thr.start()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
