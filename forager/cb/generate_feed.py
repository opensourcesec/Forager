__author__ = 'CarbonBlack, byt3smith'

# stdlib imports
import re
import sys
import time
import urllib.request, urllib.parse, urllib.error
import json
import optparse
import socket
import base64
import hashlib

# cb imports
sys.path.insert(0, "../../")
from .cbfeeds.feed import CbReport
from .cbfeeds.feed import CbFeed
from .cbfeeds.feed import CbFeedInfo

#pypi
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)


def gen_report_id(iocs):
    """
    a report id should be unique
    because generate_feed_from_raw may be run repeatedly on the same data, it should
    also be deterministic.
    this routine sorts all the indicators, then hashes in order to meet these criteria
    """
    md5 = hashlib.md5()

    # sort the iocs so that a re-order of the same set of iocs results in the same report id
    iocs.sort()

    for ioc in iocs:
        md5.update(ioc.strip().encode('utf-8'))

    return md5.hexdigest()

def build_reports(options):

    reports = []

    ips = []
    domains = []
    md5s = []

    # read all of the lines (of text) from the provided
    # input file (of IOCs)
    #
    iocs = options['ioc_file']
    try:
        raw_iocs = open(iocs).readlines()
    except:
        print((Fore.RED + '\n[-]' + Fore.RESET), end=' ')
        print('Could not open %s' % iocs)
        exit(0)

    # iterate over each of the lines
    # attempt to determine if each line is a suitable
    # ipv4 address, dns name, or md5
    #
    for raw_ioc in raw_iocs:

        # strip off any leading or trailing whitespace
        # skip any empty lines
        #
        raw_ioc = raw_ioc.strip()
        if len(raw_ioc) == 0:
            continue

        try:
            # attempt to parse the line as an ipv4 address
            #
            socket.inet_aton(raw_ioc)

            # parsed as an ipv4 address!
            #
            ips.append(raw_ioc)
        except Exception as e:

            # attept to parse the line as a md5 and, if that fails,
            # as a domain.  use trivial parsing
            #
            if 32 == len(raw_ioc) and \
               re.findall(r"([a-fA-F\d]{32})", raw_ioc):
                md5s.append(raw_ioc)
            elif -1 != raw_ioc.find("."):
                domains.append(raw_ioc)

    fields = {'iocs': {
                      },
              'timestamp': int(time.mktime(time.gmtime())),
              'link': options['feed_link'],
              'title': options['report_name'],
              'id': gen_report_id(ips + domains + md5s),
              'score': 100}

    if len(ips) > 0:
        fields['iocs']['ipv4'] = ips
    if len(domains) > 0:
        fields['iocs']['dns'] = domains
    if len(md5s) > 0:
        fields['iocs']['md5'] = md5s

    reports.append(CbReport(**fields))

    return reports

def create_feed(options):
    feed_meta = json.loads(options)

    # generate the required feed information fields
    # based on command-line arguments
    #
    feedinfo = {'name': feed_meta['name'],
                'display_name': feed_meta['display_name'],
                'provider_url': feed_meta['provider_url'],
                'summary': feed_meta['summary'],
                'tech_data': feed_meta['tech_data']}

    # if an icon was provided, encode as base64 and
    # include in the feed information
    #
    if feed_meta['icon']:
        try:
            bytes = base64.b64encode(open(feed_meta['icon']).read())
            feedinfo['icon'] = bytes
        except:
            print((Fore.RED + '\n[-]' + Fore.RESET), end=' ')
            print('Could not open %s. Make sure file still exists.\n' % feed_meta['icon'])

    # build a CbFeedInfo instance
    # this does field validation
    #
    feedinfo = CbFeedInfo(**feedinfo)

    # build a list of reports (always one report in this
    # case).  the single report will include all the IOCs
    #
    reports = build_reports(feed_meta)

    # build a CbFeed instance
    # this does field validation (including on the report data)
    #
    feed = CbFeed(feedinfo, reports)

    return feed.dump()
