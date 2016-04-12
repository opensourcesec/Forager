__author__ = 'byt3smith'

#
# Generates a dir for carbonblack feeds
# Can also stand up a SimpleHTTPServer to host the feeds
#
#stdlib
from os import chdir, listdir, mkdir, getcwd, path
import http.server
import socketserver
from re import sub, search
from json import dump, loads
from socket import gethostname
#pypi
from colorama import Fore, Back, Style, init
#local
from .feeds import FeedModules
from .tools import regex
from .cb import generate_feed

# Initialize colorama
init(autoreset=True)

def gen_feed_list():
    #generates feed list from FeedModules()
    feed_list = []
    for f in listdir('intel'):
        if f.endswith('_ioc'):
            #strip _update suffix
            f = sub("_ioc", '', f)
            feed_list.append(f)

    return feed_list

def run_feed_server():
    #stands up the feed server, points to the CB/json_feeds dir
    chdir('data/json_feeds/')
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)

    try:
        print((Fore.GREEN + '\n[+]' + Fore.RESET), end=' ')
        print(('Feed Server listening at http://%s:8000' % gethostname()))
        httpd.serve_forever()
    except:
        print((Fore.RED + '\n[-]' + Fore.RESET), end=' ')
        print("Server exited")

    return

def cb_gen(run_mode):
    #cbfeed generator
    #
    feed_list = gen_feed_list()
    print(getcwd())
    # Check for data/cb/ dir
    if path.isdir("cb/"):
        pass
    else:
        try:
            mkdir("cb/")
        except:
            print((Fore.RED + '[-] ' + Fore.RESET + 'Could not create data/cb/ directory'))
            exit()

    # Check for feed_meta dir
    if path.isdir("cb/feed_meta/"):
        feedinfo = listdir("cb/feed_meta/")
    else:
        try:
            mkdir('cb/feed_meta')
            feedinfo = listdir("cb/feed_meta/")
        except:
            print((Fore.RED + '[-] ' + Fore.RESET + 'Error creating feed_meta directory, may need to adjust permissions'))
            exit()

    #Check for JSON_feed dir
    if path.isdir("cb/json_feeds/"):
        pass
    else:
        try:
            mkdir('cb/json_feeds')
        except:
            print((Fore.RED + '[-] ' + Fore.RESET + ' Error creating json_feeds directory, may need to adjust permissions'))
            exit()

    ## Run function based on CLI args
    if run_mode == 'a':
        # run all feeds
        generate_all(feed_list, feedinfo)

    elif run_mode == 'i':
        # list all feeds for selection
        generate_one(feed_list, feedinfo)

    return



def create_json_feed(meta, json_path):
        #Creating JSON feed using scripts in cbfeeds/
        data = generate_feed.create_feed(meta)
        #print data

        #Saving the data to file in json_feeds/
        try:
            print((Fore.YELLOW + '[*]' + Fore.RESET), end=' ')
            print('Saving report to: %s' % json_path)
            dump_data = open(json_path, 'w+').write(data)
        except:
            print((Fore.RED + '[-]' + Fore.RESET), end=' ')
            print('Could not dump report to %s' % json_path)
            exit(0)

        return


def generate_all(feed_list, feedinfo):
    # Check for feed metadata
    print((Fore.YELLOW + '[*] ' + Fore.RESET + 'Checking for existing feed metadata necessary to generate feeds...\n'))
    for f in feed_list:
        #check for feed_info files correlating to feed_list
        json_path = 'cb/json_feeds/%s' % f

        if f in feedinfo:
            print(('\n' + f + ': ' + '[' + Fore.GREEN + ' yes ' + Fore.RESET + ']'))

        else:
            print(('\n' + f + ': ' + '[' + Fore.RED + ' no ' + Fore.RESET + ']'))
            meta = get_feed_info(f)

        #generate json_feed for feed module
        meta_file = 'cb/feed_meta/%s' % f
        meta = open(meta_file, 'r').read()
        try:
            loads(meta)    # checks that meta file is valid JSON string
        except:
            print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
            print(('%s is not valid JSON.\nWould you like to create a valid metadata file?' % meta_file))
            choice = input('> (y/n) ')
            if choice == 'y':
                meta = get_feed_info(f)
                return
            elif choice == 'n':
                print((Fore.YELLOW + '[*] Moving on..'))
                return
            else:
                print((Fore.RED + '[!] Invalid choice. Better luck next time..'))
                exit(0)

        create_json_feed(meta, json_path)


def generate_one(feed_list, feedinfo):
    print((Fore.YELLOW + '[*] ' + Fore.RESET + ' soon to be individual feed generation'))



def get_feed_info(f):
    #interactive prompt for gathering and storing feed info data
    feed_dict = {}
    feedpath = 'cb/feed_meta/%s' % f    # Path for new feed metadata
    meta_file = open(feedpath, 'w+')
    name = ''.join(e for e in f if e.isalnum())
    host = gethostname()
    ioc_file = 'intel/%s_ioc' % f
    feed_link = 'http://%s/%s' % (host, ioc_file)
    report_name = f + '_report'

    # Find URL in feeds.py
    try:
        print(getcwd())
        feedfile = open('../forager/feeds.py', 'r').readlines()
    except:
        print((Fore.RED + '\n[-]' + Fore.RESET), end=' ')
        print('Could not open file')
        exit(0)

    count = 0
    stat = 0
    for line in feedfile:
        line = line.lower()
        fn = f.lower()
        if fn in line:
            loc = feedfile[count+1]
            searches = search(regex('URL'), loc.encode('utf-8'))
            if searches == None:
                pass
            else:
                result = searches.group(0)
                stat=1
        else:
            count+=1

    if stat == 0:
        print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
        print('Provider URL for {}:'.format(f))
        provider_url = input('> ')
    else:
        provider_url = result

    # Choose Display Name
    display_name = f
    print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
    print(("Is '%s' okay for Feed Display Name? ([RETURN], or specify new display name)" % display_name))
    choice = input('\r> ')
    if len(choice) == 0:
        pass
    else:
        display_name = choice

    # Choose Summary
    summary = f
    print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
    print(("Is '%s' okay for Feed Summary? ([RETURN], or specify summary)" % summary))
    choice = input('\r> ')
    if len(choice) == 0:
        pass
    else:
        summary = choice

    # Choose Tech Data
    tech_data = 'There are no requirements to share any data to receive this feed.'
    print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
    print(("Is '%s'\n okay for Tech Data? ([RETURN], or specify new display name)" % tech_data))
    choice = input('\r> ')
    if len(choice) == 0:
        pass
    else:
        tech_data = choice

    # Icon
    icon = ''
    print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
    iconic = input('Do you have an icon to upload? (Y/N)\n> ')
    if iconic.lower() == 'y':
        print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
        icon = input('Please provide the full path to the image here:\n> ')
    elif iconic.lower() == 'n':
        pass
    else:
        print((Fore.YELLOW + '\n[*]' + Fore.RESET), end=' ')
        print('[*] Sorry, did not recognize that. You can add an icon later..')

    # Parsing values into the feed dictionary
    feed_meta = ['name', 'display_name', 'provider_url', 'summary', 'tech_data', 'icon', 'ioc_file', 'feed_link', 'report_name']
    for i in feed_meta:
        feed_dict[i] = str(locals()[i])

    try:
        json_data = dump(feed_dict, meta_file)
        print((Fore.GREEN + '\n[+] Successfully wrote metadata to %s' % feedpath))
        meta_file.close()
        return json_data
    except:
        print((Fore.RED + '\n[-] Could not write JSON stream to file'))
