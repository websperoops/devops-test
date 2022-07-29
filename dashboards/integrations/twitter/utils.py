from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from dashboards.models import Integrations_Twitter_Mentions
import tweepy

def twitter_auth(uid):
    account_id = SocialAccount.objects.get(provider='twitter', user_id=uid).id
    twitterApp = SocialApp.objects.get(provider='twitter')
    twitterToken = SocialToken.objects.get(app_id=twitterApp.id, account_id=account_id)

    consumer_key = twitterApp.client_id
    consumer_secret = twitterApp.secret
    access_token = twitterToken.token
    access_token_secret = twitterToken.token_secret
    api_items = []

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api1 = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    api2 = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, parser=tweepy.parsers.JSONParser())
    api_items.append(api1)
    api_items.append(api2)

    try:
        for api in api_items:
            api.verify_credentials()
            print("Authentication OK")
    except:
        print("Error during authentication")

    return api_items

"""
# gets Most Recent Tweet
"""


def getMostRecentTweet(uid):
    '''RETURNS the most recent tweet based on a user id'''

    userAccount = SocialAccount.objects.get(
        provider="twitter", user_id=uid)

    API = twitter_auth(uid)
    resp1 = API[1].user_timeline(user=userAccount.uid)

    return resp1

"""
# gets the since_id of the Most Recent Tweet
"""

def get_params(uid):
    '''Build API params'''

    params = {
        "since_id": None
    }
    try:  # try to get last mention we pulled from twitter in our database
        since_id = Integrations_Twitter_Mentions.objects.filter(
            user_iden=uid).order_by('-timestamp')[0].mention_id
        if since_id is None:
            since_id = str(getMostRecentTweet(uid=uid)[0]["id_str"])


    except:  # if none exist use the latest tweet by the user as 'starting point'
        since_id = str(getMostRecentTweet(uid=uid)[0]["id_str"])

    params["since_id"] = since_id
    return params

"""
# gets the Latest Mention linked to 'since_id'
"""

def getLatestMentions(uid):
    '''RETURNS list of database tuple objects containing mentions since last mention/user tweet'''

    api_params = get_params(uid=uid)
    since_id = api_params['since_id']

    API = twitter_auth(uid)
    response = API[1].mentions_timeline(since_id)

    return response


def getOldestMentions(uid):
    api_params = get_params(uid=uid)
    max_id = api_params['since_id']

    API = twitter_auth(uid)
    response = API[1].mentions_timeline(max_id=max_id)

    return response