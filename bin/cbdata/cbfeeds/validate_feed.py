import re
import sys
import time
import json
import urllib
import socket
import base64
from feed import *
import optparse

def build_cli_parser():
    """
    generate OptionParser to handle command line switches
    """

    usage = "usage: %prog [options]"
    desc = "Validate a Carbon Black feed"

    parser = optparse.OptionParser(usage=usage, description=desc)
    
    parser.add_option("-f", "--feedfile", action="store", type="string", dest="feed_filename",
                      help="Feed Filename to validate")
    parser.add_option("-p", "--pedantic", action="store_true", default=False, dest="pedantic",
                      help="Validates that no non-standard JSON elements exist")
    parser.add_option("-e", "--exclude", action="store", default=None, dest="exclude",
                      help="Filename of 'exclude' list - newline delimited indicators to consider invalid")
    parser.add_option("-i", "--include", action="store", default=None, dest="include",
                      help="Filename of 'include' list - newline delimited indicators to consider valid")

    return parser

def validate_file(feed_filename):
    """
    validate that the file exists and is readable
    """
    f = open(feed_filename)
    contents = f.read()
    return contents

def validate_json(contents):
    """
    validate that the file is well-formed JSON
    """
    return json.loads(contents)

def validate_feed(feed, pedantic=False):
    """
    validate that the file is valid as compared to the CB feeds schema
    """
     
    # verify that we have both of the required feedinfo and reports elements
    #
    if not feed.has_key("feedinfo"):
        raise Exception("No 'feedinfo' element found!")
    if not feed.has_key("reports"):
        raise Exception("No 'reports' element found!")

    # set up the cbfeed object
    #
    feed = CbFeed(feed["feedinfo"], feed["reports"])

    # validate the feed
    # this validates that all required fields are present, and that
    #   all required values are within valid ranges
    #
    feed.validate(pedantic) 
    
    return feed

def validate_against_include_exclude(feed, include, exclude):
    """
    ensure that no feed indicators are 'excluded' or blacklisted
    """
    for ioc in feed.iter_iocs():
        if ioc["ioc"] in exclude and not ioc["ioc"] in include:
            raise Exception(ioc)

def gen_include_exclude_sets(include_filename, exclude_filename):
    """
    generate an include and an exclude set of indicators by
    reading indicators from a flat, newline-delimited file
    """
    include = set()
    exclude = set()

    if include_filename:
        for indicator in open(include_filename).readlines():
            include.add(indicator.strip())
    if exclude_filename:
        for indicator in open(exclude_filename).readlines():
            exclude.add(indicator.strip())

    return include, exclude

if __name__ == "__main__":

    parser = build_cli_parser()
    options, args = parser.parse_args(sys.argv)

    if not options.feed_filename:
        print "-> Must specify a feed filename to validate; use the -f switch or --help for usage"
        sys.exit(0)

    # generate include and exclude (whitelist and blacklist) sets of indicators
    # feed validation will fail if a feed ioc is blacklisted unless it is also whitelisted
    #
    include, exclude = gen_include_exclude_sets(options.include, options.exclude)

    try:
        contents = validate_file(options.feed_filename)
        print "-> Validated that file exists and is readable"
    except Exception, e:
        print "-> Unable to validate that file exists and is readable"
        print "-> Details:"
        print
        print e
        sys.exit(0)

    try:
        feed = validate_json(contents)
        print "-> Validated that feed file is valid JSON"
    except Exception, e:
        print "-> Unable to validate that file is valid JSON"
        print "-> Details:"
        print
        print e
        sys.exit(0)

    try:
        feed = validate_feed(feed, pedantic=options.pedantic)
        print "-> Validated that the feed file includes all necessary CB elements"
        print "-> Validated that all element values are within CB feed requirements"
        if options.pedantic:
            print "-> Validated that the feed includes no non-CB elements"
    except Exception, e:
        print "-> Unable to validate that the file is a valid CB feed"
        print "-> Details:"
        print
        print e
        sys.exit(0)

    if len(exclude) > 0 or len(include) > 0:
        try:
            validate_against_include_exclude(feed, include, exclude)
            print "-> Validated against include and exclude lists"
        except Exception, e:
            print "-> Unable to validate against the include and exclude lists"
            print e 
