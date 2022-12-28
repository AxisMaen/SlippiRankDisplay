import json

#Handles a cache for slippi ranked data
#Cache is in the same format as the scraped response, but adds a "lastUpdated" value under "user"
#Cache is a dict where key is a code and value is a dict with response data

#returns True if the code is already in the cache, false otherwise
def isCodeInCache(code):
    return False

#returns True if code needs updated, false otherwise
def isUpdateNeeded(code):
    return True

#updates the given code and its attributes in the cache
def updateCache(code, data):
    #displayName, rating, winCount, lossCount, lastUpdate
    displayName = data["data"]["getConnectCode"]["user"]["displayName"]
    rating = data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingOrdinal"]
    winCount = str(data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["wins"])
    lossCount = str(data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["losses"])

    ### calculate lastUpdate time ###


    #import cache, do cache[code] = newData, write cache
    return

#returns a dict of the cache value for the given code
def readCache(code): 
    return

#Format of a cache value 
'''
{
    'data': {
        'getUser': None, 
        'getConnectCode': {
            'user': {
                'displayName': 'BenSnapeEsports', 
                'rankedNetplayProfile': {
                    'ratingOrdinal': 2008.962215, 
                    'wins': 77, 
                    'losses': 62,
                    '__typename': 'NetplayProfile'
                },
                lastUpdated : dateHere
                '__typename': 'User'
            }, 
        '__typename': 'ConnectCode'
        }
    }
}
'''