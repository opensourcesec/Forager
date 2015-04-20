class CbException(Exception):
    pass

class CbIconError(CbException):
    pass

class CbInvalidFeed(CbException):
    pass

class CbInvalidReport(CbException):
    pass

#from feed import CbFeed
#from feed import CbFeedInfo
#from feed import CbReport