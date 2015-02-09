Forager  ![alt tag](img/Forager.png)
=======

Threat Intelligence hunter-gatherer CLI tool. 
Features:

* Fetch domain and IPv4 indicators which can then be taken from the new-line formatted files and input into security devices or other tools as watchlists.
* Extract domain and IPv4 indicators from Whitepapers
* Search through the indicator set by single IP or with an IOC file
* Generate JSON feeds for consumption by CarbonBlack

NOTE:
The script creates a file for malicious IP addresses and a file for malicious domains for EACH feed in feeds.py, and then places them in a folder entitled "intel" 


Requirements:
-------
* argparse
* xlrd
* pdfminer

You can install all requirements with the included requirements.txt file
```
pip install -r requirements.txt
```

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

* Reads in a file and extracts IP address and domain indicators
* Places the extracted indicators into the intel directory 
* Currently supported filetypes:
  * TXT
  * PDF
  * XLS/XLSX

Note:

* Prone to false positives when extracting indicators from PDF as whitepapers with indicators will normally also contain URL references

CarbonBlack Feed Generator
-----------------

(Invoked with --cbgen)

* Generates JSON feeds of all of the IOCs in the intel dir
* Utilizes an interactive CLI prompt to allow the user to provide feed metadata the first time CBgen is run

CB Feed Future:

* Build in feed server so that the CarbonBlack server can automatically ingest the feeds
