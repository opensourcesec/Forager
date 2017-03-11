__author__ = 'byt3smith'
#
# Purpose: Import module for pulling and formatting
#          all necessary intelligence feeds
#

from .tools import *
from re import search

ip_rex = regex('ip')
domain_rex = regex('domain')

# Feed Module
#######################
class Feed():
    def __init__(self, url, name, altpattern=None):
        self.url = url
        self.name = name
        self.expattern = altpattern

    def run(self):
        if self.altpattern is not None:
            # use alternate
            pass
        else:
            ip_iocs = gather(self.url, ip_rex)
            host_iocs = gather(self.url, domain_rex)

        add2file(name + '_ioc', ip_iocs)
        add2file(name + '_ioc', domain_rex)


'''
malc0de_ip = Feed('http://malc0de.com/bl/IP_Blacklist.txt', 'malc0de')
malc0de_domains = Feed('http://malc0de.com/bl/BOOT', 'malc0de')
'''
######################
class FeedModules():
    ## Malc0de
    def malc0de_update(self):
        iocs = gather('http://malc0de.com/bl/IP_Blacklist.txt', ip_rex)
    ## Malc0de Domain
        host_ioc = gather('http://malc0de.com/bl/BOOT', domain_rex)

        add2file('malc0de_ioc', iocs)
        add2file('malc0de_ioc', host_ioc)

    ## Malware Domain List
    def MDL_update(self):
        url = 'http://mirror1.malwaredomains.com/files/domains.txt'
        r = domain_rex
        ioc_list = []
        count = 0
        f = connect(url)
        sleep(2)
        for line in f:
            rex = search(r, line)
            if rex == None:
                pass
            else:
                ioc = rex.group(0)
                if ioc in ioc_list:
                    pass
                else:
                    ioc_list.append(ioc)
                    count += 1

        add2file('MDL_ioc', ioc_list)


    ## Ransomware Tracker
    def ransomware_update(self):
        host_ioc = gather('https://ransomwaretracker.abuse.ch/downloads/RW_DOMBL.txt', domain_rex)

        add2file('ransomware_ioc', host_ioc)


    ## Feodo Tracker
    def feodo_update(self):
        iocs = gather('https://feodotracker.abuse.ch/blocklist/?download=ipblocklist', ip_rex)
        host_ioc = gather('https://feodotracker.abuse.ch/blocklist/?download=domainblocklist', domain_rex)

        add2file('feodo_ioc', iocs)
        add2file('feodo_ioc', host_ioc)


    ## reputation.alienvault.com
    def alienvault_update(self):
        iocs = gather('https://reputation.alienvault.com/reputation.generic', ip_rex)
        add2file('alienvault_ioc', iocs)


    ## DShield High Pri suspicious domain list
    def dshieldHigh_update(self):
        host_iocs = gather('http://www.dshield.org/feeds/suspiciousdomains_High.txt', domain_rex)
        add2file('dShieldHigh_ioc', host_iocs)


    ## Spyeye Tracker
    def spyeye_update(self):
        iocs = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=hostsdeny', ip_rex)
        host_ioc = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=hostsdeny', domain_rex)

        add2file('spyeye_ioc', iocs)
        add2file('spyeye_ioc', host_ioc)


    ## Zeus Tracker
    def zeus_update(self):
        iocs = gather('https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist', ip_rex)
        host_ioc = gather('https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist', domain_rex)

        add2file('zeus_ioc', iocs)
        add2file('zeus_ioc', host_ioc)


    ## Palevo Tracker
    def palevo_tracker_update(self):
        iocs = gather('https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist', ip_rex)
        host_ioc = gather('https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist', domain_rex)

        add2file('palevo_ioc', iocs)
        add2file('palevo_ioc', host_ioc)


    ## OpenBL
    def openbl_update(self):
        iocs = gather('http://www.openbl.org/lists/base.txt', ip_rex)
        add2file('openbl_ioc', iocs)


    ## MalwareDomains
    def malwaredomains_update(self):
        iocs = gather('http://mirror1.malwaredomains.com/files/domains.txt', domain_rex)
        add2file('malwaredomains_ioc', iocs)


    ## NoThink Honeypots -- DNS Traffic
    def nothinkDns_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_dns.txt', ip_rex)
        host_ioc = gather('http://www.nothink.org/blacklist/blacklist_malware_dns.txt', domain_rex)

        add2file('nothinkDNS_ioc', iocs)
        add2file('noThinkDNS_ioc', host_ioc)


    ## NoThink Honeypots -- HTTP Traffic
    def nothinkHttp_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_http.txt', ip_rex)
        host_iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_http.txt', domain_rex)

        add2file('nothinkHTTP_ioc', iocs)
        add2file('nothinkHTTP_ioc', host_iocs)


    ## NoThink Honeypots -- IRC Traffic
    def nothinkIrc_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_irc.txt', ip_rex)
        add2file('nothinkIRC_ioc', iocs)


    ## MalwaredRU Tracker
    def MalwaredRU_update(self):
        iocs = gather('http://malwared.ru/db/fulllist.php', ip_rex)
        host_iocs = gather('http://malwared.ru/db/fulllist.php', domain_rex)

        add2file('MalwaredRU_ioc', iocs)
        add2file('MalwaredRU_ioc', host_iocs)


    ## ET-Open BOTCC
    def ETOpenBotCC_update(self):
        iocs = gather('http://rules.emergingthreats.net/blockrules/emerging-botcc.rules', ip_rex)

        add2file('ETOpenBotCC_ioc', iocs)

    ## ET-Open Emerging CIarmy
    def ETOpenCIArmy_update(self):
        iocs = gather('http://rules.emergingthreats.net/blockrules/emerging-ciarmy.rules', ip_rex)

        add2file('ETOpenCIArmy_ioc', iocs)

    ## ET-Open Compromised
    def ETOpenCompd_update(self):
        iocs = gather('http://rules.emergingthreats.net/blockrules/emerging-compromised-BLOCK.rules', ip_rex)

        add2file('ETOpenCompd_ioc', iocs)
