import json
from datetime import datetime
import os

#Handles a cache for slippi ranked data
#Cache is in the same format as the scraped response, but adds a "lastUpdated" value under "user"
#Cache is a dict where key is a code and value is a dict with response data

FILENAME = "files/cache.json"

def is_code_in_cache(code):
    '''
    returns True if the code is already in the cache, false otherwise
    '''

    cache = read_cache()

    if cache and (code in cache.keys()):
        return True

    return False


def is_update_needed(code):
    '''
    returns True if it is passed the lastUpdated date for the given code or if code is not in cache
    returns False if it has not passed the lastUpdated date
    '''

    if is_code_in_cache(code):
        cache = read_cache()
        last_update_day_string = cache[code]["data"]["getConnectCode"]["user"]["lastUpdate"]
        last_update_day = datetime.strptime(last_update_day_string, '%Y-%m-%d').date()
        current_date = datetime.now().date()

        #if we are on a different date then the lastUpdated date, then midnight has passed
        if current_date > last_update_day:
            return True
        return False
    else:
        return True


def update_cache(code, data):
    '''
    #updates the given code and its attributes in the cache
    #the data given does NOT have rating history updated, that is handled here
    #returns the updated data for the given code
    '''

    cache = read_cache()

    display_name = data["data"]["getConnectCode"]["user"]["displayName"]
    rating = data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingOrdinal"]
    win_count = str(data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["wins"])
    loss_count = str(data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["losses"])
    current_date = str(datetime.now().date())

    #if code is in cache, get old rating history, otherwise init a new rating history
    if is_code_in_cache(code):
        rating_history = cache[code]["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingHistory"]
    else:
        rating_history = []

    #update rating history
    #rank is currently None since we don't pull that info yet
    rating_history.append((current_date, rating, str(None)))

    data = {
        'data': {
            'getUser': None,
            'getConnectCode': {
                'user': {
                    'displayName': display_name,
                    'rankedNetplayProfile': {
                        'ratingOrdinal': rating,
                        'wins': win_count,
                        'losses': loss_count,
                        'ratingHistory' : rating_history,
                        '__typename': 'NetplayProfile'
                    },
                    'lastUpdate' : current_date,
                    '__typename': 'User'
                },
            '__typename': 'ConnectCode'
            }
        }
    }

    cache[code] = data

    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
    with open(FILENAME, "w", encoding='UTF8') as file:
        json.dump(cache, file)

    return data


def read_cache():
    '''
    returns a dict of the cache
    if cache is not found, make a new one
    '''
    try:
        with open(FILENAME, "r", encoding='UTF8') as file:
            cache = json.load(file)
            return cache
    except: #pylint: disable=bare-except
        #if cache not found, make new one and return it
        os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
        with open(FILENAME, "w", encoding='UTF8') as file:
            json.dump({}, file)
            return {}

#Format of a cache value
#pylint: disable=pointless-string-statement
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
                    'ratingHistory' : (date, rating, rank)
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
