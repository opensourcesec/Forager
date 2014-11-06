  Forager
============

Threat Intelligence hunter-gatherer CLI tool: Provides searching, fetching, extracting, and storage of various indicators, which can then be taken from the new-line formatted files and input into security devices or other tools as watchlists, or queried for identification of malicious traffic in network logs.

NOTE:
The script creates a file for EACH indicator type for EACH feed in feeds.py, and then places them in a folder entitled "intel". This will (most likely) be updated in the near future to consist of a database/index, which will be easier to reference than the filesystem alone.

* Dependencies: 
  * xlrd 
  * pdfminer


Feeds
--------

(Invoked with --feeds)

* 'list' -- Lists all feeds and allows user to choose a single feed to update. 
* 'update' -- Updates all feed modules listed in Forager

Hunting 
---------

(Invoked with --hunt)

* '-f [file path]' Provides the capability to search through the intel directory results for a specific list of indicators
* '-s [IPv4 address]' Searches through intel directory for a single IP address

Extraction
----------

(Invoked with --extract)

* Reads in a file and extracts IP address, domain, and MD5 hash indicators
* Places the extracted indicators into the intel directory 
* Currently supported filetypes:
  * TXT
  * PDF
  * XLS/XLSX
  * XML

_____

