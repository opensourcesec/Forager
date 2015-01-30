__author__ = '0xnix'
#
# Purpose: Import module for pulling and formatting
#          all necessary intelligence feeds
#

from tools import *
from re import search

ip_addr = regex('ip')
hostname = regex('domain')

class FeedModules():
    ## Malc0de
    def malc0de_update(self):
        iocs = gather('http://malc0de.com/bl/IP_Blacklist.txt', ip_addr)
    ## Malc0de Domain
        host_ioc = gather('http://malc0de.com/bl/BOOT', hostname)

        add2file('malc0de_ioc', iocs)
        add2file('malc0de_ioc', host_ioc)

    ## Malware Domain List
    def MDL_update(self):
        url = 'http://mirror1.malwaredomains.com/files/domains.txt'
        r = hostname
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


    ## Feodo Tracker
    def feodo_update(self):
        iocs = gather('https://feodotracker.abuse.ch/blocklist/?download=ipblocklist', ip_addr)
        host_ioc = gather('https://feodotracker.abuse.ch/blocklist/?download=domainblocklist', hostname)

        add2file('feodo_ioc', iocs)
        add2file('feodo_ioc', host_ioc)


    ## reputation.alienvault.com
    def alienvault_update(self):
        iocs = gather('https://reputation.alienvault.com/reputation.generic', ip_addr)
        add2file('alienvault_ioc', iocs)


    ## DShield High Pri suspicious domain list
    def dshieldHigh_update(self):
        host_iocs = gather('http://www.dshield.org/feeds/suspiciousdomains_High.txt', hostname)
        add2file('dShield_high_ioc', host_iocs)


    ## Spyeye Tracker
    def spyeye_update(self):
        iocs = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=hostsdeny', ip_addr)
        host_ioc = gather('https://spyeyetracker.abuse.ch/blocklist.php?download=hostsdeny', hostname)

        add2file('spyeye_ioc', iocs)
        add2file('spyeye_ioc', host_ioc)


    ## Zeus Tracker
    def zeus_update(self):
        iocs = gather('https://zeustracker.abuse.ch/blocklist.php?download=ipblocklist', ip_addr)
        host_ioc = gather('https://zeustracker.abuse.ch/blocklist.php?download=domainblocklist', hostname)

        add2file('zeus_ioc', iocs)
        add2file('zeus_ioc', host_ioc)


    ## Palevo Tracker
    def palevo_tracker_update(self):
        iocs = gather('https://palevotracker.abuse.ch/blocklists.php?download=ipblocklist', ip_addr)
        host_ioc = gather('https://palevotracker.abuse.ch/blocklists.php?download=domainblocklist', hostname)

        add2file('palevo_ioc', iocs)
        add2file('palevo_ioc', host_ioc)


    ## OpenBL
    def openbl_update(self):
        iocs = gather('http://www.openbl.org/lists/base.txt', ip_addr)
        add2file('openbl_ioc', iocs)


    ## MalwareDomains
    def malwaredomains_update(self):
        iocs = gather('http://mirror1.malwaredomains.com/files/domains.txt', hostname)
        add2file('malwaredomains_ioc', iocs)


    ## NoThink Honeypots -- DNS Traffic
    def nothinkDns_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_dns.txt', ip_addr)
        host_ioc = gather('http://www.nothink.org/blacklist/blacklist_malware_dns.txt', hostname)

        add2file('nothink_dns_ioc', iocs)
        add2file('noThink_dns_ioc', host_ioc)


    ## NoThink Honeypots -- HTTP Traffic
    def nothinkHttp_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_http.txt', ip_addr)
        host_iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_http.txt', hostname)

        add2file('nothink_http_ioc', iocs)
        add2file('nothink_http_ioc', host_iocs)


    ## NoThink Honeypots -- IRC Traffic
    def nothinkIrc_update(self):
        iocs = gather('http://www.nothink.org/blacklist/blacklist_malware_irc.txt', ip_addr)
        add2file('nothink_irc_ioc', iocs)
    

    ## MalwaredRU Tracker
    def MalwaredRU_update(self):
        iocs = gather('http://malwared.ru/db/fulllist.php', ip_addr)
        host_iocs = gather('http://malwared.ru/db/fulllist.php', hostname)

        add2file('MalwaredRU_ioc', iocs)
        add2file('MalwaredRU_ioc', host_iocs)


    ## ET-Open BOTCC
    def ETOpenBotCC_update(self):
        iocs = gather('http://rules.emergingthreats.net/blockrules/emerging-botcc.rules', ip_addr)

        add2file('ET_Open_BotCC_ioc', iocs)

    ## ET-Open Emerging CIarmy
    def ETOpenCIArmy_update(self):
        iocs = gather('http://rules.emergingthreats.net/blockrules/emerging-ciarmy.rules', ip_addr)

        add2file('ET_Open_CIArmy_ioc', iocs)

    ## ET-Open Compromised
    def ETOpenCompd_update(self):
        iocs = gather('http://rules.emergingthreats.net/blockrules/emerging-compromised-BLOCK.rules', ip_addr)

        add2file('ET_Open_Compd_ioc', iocs)
