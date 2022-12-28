import json
from datetime import datetime

#Handles a cache for slippi ranked data
#Cache is in the same format as the scraped response, but adds a "lastUpdated" value under "user"
#Cache is a dict where key is a code and value is a dict with response data

#returns True if the code is already in the cache, false otherwise
def isCodeInCache(code):
    cache = readCache()
    
    if(cache and code in cache.keys()):
        return True
    else:
        return False

#returns True if it is passed the lastUpdated date for the given code or if code is not in cache
#returns False if it has not passed the lastUpdated date
def isUpdateNeeded(code):
    if(isCodeInCache(code)):
        cache = readCache()
        lastUpdateDayString = cache[code]["data"]["getConnectCode"]["user"]["lastUpdate"]
        lastUpdateDay = datetime.strptime(lastUpdateDayString, '%Y-%m-%d').date()
        currentDate = datetime.now().date()

        #if we are on a different date then the lastUpdated date, then midnight has passed
        if(currentDate > lastUpdateDay):
            return True
        else:
            return False
    else:
        return True

#updates the given code and its attributes in the cache
def updateCache(code, data):
    displayName = data["data"]["getConnectCode"]["user"]["displayName"]
    rating = data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingOrdinal"]
    winCount = str(data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["wins"])
    lossCount = str(data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["losses"])
    currentDate = str(datetime.now().date())

    data = {
        'data': {
            'getUser': None, 
            'getConnectCode': {
                'user': {
                    'displayName': displayName, 
                    'rankedNetplayProfile': {
                        'ratingOrdinal': rating, 
                        'wins': winCount, 
                        'losses': lossCount,
                        '__typename': 'NetplayProfile'
                    },
                    'lastUpdate' : currentDate,
                    '__typename': 'User'
                }, 
            '__typename': 'ConnectCode'
            }
        }
    }

    cache = readCache()
    cache[code] = data

    with open("files/cache.json", "w") as file:
        json.dump(cache, file)

#returns a dict of the cache
#if cache is not found, make a new one
def readCache():
    try:
        with open("files/cache.json", "r") as file:
            cache = json.load(file)  
            return cache  
    except:
        #if cache not found, make new one and return it
        with open("files/cache.json", "w") as file:
            json.dump({}, file)
            return {}

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
                lastUpdate : dateHere,
                '__typename': 'User'
            }, 
        '__typename': 'ConnectCode'
        }
    }
}
'''