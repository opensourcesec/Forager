#!/usr/bin/env python
__author__ = 'byt3smith'
#
# Main

# Check for Python3
import sys
if sys.version_info[0] != 3:
    print("[-] Forager requires Python 3")
    exit()

#stdlib
import argparse
import os
from sys import exit
from threading import Thread, activeCount
from time import sleep
#pypi
from colorama import Fore, init
#local
from forager.hunt import single_search, search_file
from forager.feeds import FeedModules
from forager.tools import extract, update_progress
from forager.cb_tools import cb_gen, run_feed_server


def run_modules():
    x = FeedModules()
    threads = []
    for i in dir(x):
        if i.endswith('_update'):
            mod = getattr(x, i)
            threads.append(Thread(target=mod, name='{}'.format(i)))
        else:
            pass

    for t in threads:
        t.start()
        print('Initialized: {}'.format(t.name))

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
    print((Fore.GREEN + '\n[+]' + Fore.RESET + ' Feed collection finished!'))


def ensure_dir():
    folder = 'data/intel'
    if not os.path.exists(folder):
        os.makedirs(folder)
        print((Fore.YELLOW + '\n[*]' + Fore.RESET))
        print('Created new directory: intel')


def main():
    init(autoreset=True) ## Initialize colorama
    banner = '''     ______  ______   ______   ______   ______   ______   ______
    /\  ___\/\  __ \ /\  == \ /\  __ \ /\  ___\ /\  ___\ /\  == \\
    \ \  __\\\\ \ \/\ \\\\ \  __< \ \  __ \\\\ \ \__ \\\\ \  __\\ \\ \\  __<
     \ \_\   \ \_____\\\\ \_\ \_\\\\ \_\ \_\\\\ \_____\\\\ \_____\\\\ \\_\\ \\_\\
      \/_/    \/_____/ \/_/ /_/ \/_/\/_/ \/_____/ \/_____/ \/_/ /_/
    '''

    print((Fore.CYAN + banner))

    feedmods = FeedModules()
    ensure_dir()
    os.chdir('data/intel/')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--feeds", type=str, choices=['list', 'update'], help="Manipulates intelligence feeds\n\
    List - Show list of current feeds to update individually\n\
    Update - Update all feeds")
    parser.add_argument('--hunt', action="store_true", help='Searches through the intel dir for matches')
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('-s', type=str, nargs='?', help="Accepts a single IP address")
    group2.add_argument('-f', type=str, nargs='?', help="Receives a file of indicators to search through.")
    parser.add_argument("--extract", type=str, nargs=1, help="Extracts indicators from a given file")
    parser.add_argument("--cbgen", type=str, choices=['all', 'one'], help="Generates alliance feeds for CarbonBlack. (Requires cbfeeds be present in bin dir)")
    parser.add_argument('--srv', action="store_true", help="Runs feed server")


    args = parser.parse_args()

    if args.hunt:
        if args.s:
            single_search(args.s)
        elif args.f:
            search_file(args.f)

    elif args.feeds == 'update':
        print((Fore.YELLOW + '\n[*]' + Fore.RESET + ' Updating all feeds'))
        run_modules()

    elif args.feeds == 'list':
        print((Fore.YELLOW + '[*]' + Fore.RESET + ' Please select feed to update:'))
        feed_list = dir(FeedModules)
        newlist = []
        feedcount = 1
        for feed in feed_list:
            if "_update" in feed:
                newlist.append(feed)
                print(str(feedcount)+'. '+feed)
                feedcount += 1
            else:
                pass

        print('\n')
        choice = input('Select feed by numerical ID (1-{})\n> '.format(len(newlist)))
        if int(choice) in range(1, len(newlist) + 1):  # condition to check if proper feed was selected.
            mod = newlist[int(choice) - 1]   # Using choice number to locate item in the feed list
            methodToCall = getattr(feedmods, mod)  # saving the function with newlist argument as variable
            methodToCall()
        else:
            print((Fore.RED + '[-]' + Fore.RESET + ' Invalid option. Exiting...'))
            exit(0)

    elif args.extract:
        os.chdir('../')
        filename = args.extract[0]
        base = os.path.basename(filename)
        print((Fore.YELLOW + '[*]' + Fore.RESET + ' Extracting indicators from {}'.format(base)))
        extract(filename)

    elif args.cbgen:
        try:
            ioc = os.listdir('.')
            for i in ioc:
                if '_ioc' in i:
                    raise StopIteration()
            print((Fore.RED + '[-] ' + Fore.RESET + ' No IOC files found.'))
            print((Fore.YELLOW + '\r\n[*] ' + Fore.RESET + ' Please gather IOCs through --feeds update, or --extract for local files'))
            exit(0)
        except StopIteration:
            print((Fore.GREEN + '[+] ' + Fore.RESET + 'IOCs found, continuing to feed generation\n'))
            pass


        os.chdir('../')
        if args.cbgen.lower() == 'all':
            cb_gen('a')
        elif args.cbgen.lower() == 'one':
            cb_gen('i')

        exit(0)

    elif args.srv:
        thr = Thread(target=run_feed_server(), name='Feed_server')
        thr.start()
        thr.join()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
