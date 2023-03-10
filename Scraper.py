import requests

#Rank is currently hard coded into the web page as a bunch of if statements
#Only possible to get it by doing a full scrape with Selenium (avoiding for now)

#sendQuery currently exits the program if it encounters an error, want to change that later //TODO


def send_query(code):
    '''
    sends a graphQL query to the endpoint
    returns a json response, or None on error
    '''

    code = code.upper()

    url = "https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql"

    variables = {"cc": code, "uid": code}

    query = """fragment userProfilePage on User {
        displayName
        rankedNetplayProfile {
            ratingOrdinal
            wins
            losses
            __typename
        }
        __typename
    }

    query AccountManagementPageQuery($cc: String!, $uid: String!) {
        getUser(fbUid: $uid) {
            ...userProfilePage
            __typename
        }
        getConnectCode(code: $cc) {
            user {
                ...userProfilePage
                __typename
            }
            __typename
        }
    }
    """

    try:
        response = requests.post(url, json = {"query": query, "variables": variables}, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return None # return None to signify an error

    return response.json()
