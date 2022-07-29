from . import utils
from dashboards.integrations.utils.dashboard_sync_complete import token_failure
from dashboards.models import Integrations_Twitter_Mentions
import logging
from tweepy import Cursor, TweepError, RateLimitError


logger = logging.getLogger(__name__)


def save_twitter(integration=None, user=None, task_id=None):

    print('save_twitter is loading...')

    logger.debug("SYNC - TWITTER - {}".format(user))
    user_iden = user.id

    integration.set_sync_state(user_iden, 'twitter', task_id)
    auth_params = integration.build_auth_params('twitter', user)
    if auth_params != 'done':

        apis = integration.get_params(auth_params)

        # // BEGIN LOOP THROUGH ENDPOINTS
        for api in apis:
            name = api['name']
            data = api['data']

            # data parser
            model = data['model']
            handler = data['handler']

            status = SyncTwitter(auth_params['initialize'], model, auth_params['pk'], name, handler, auth_params['user_iden'])

    return status

# Twitter Sync
def SyncTwitter(initialize, model, pk, name, handler, user_iden):

    print("SyncTwitter is loading...")

    def Sync(data, pk, model, handler, name, user_iden):

        table_handler = handler(data, pk, user_iden)
        table_handler.save_all_objects()

    try:
        mentionsResponse = utils.getLatestMentions(user_iden)
        Sync(mentionsResponse, pk, user_iden, handler, name, user_iden)
    except:
        token_failure('twitter', user_iden)
        return '0Auth Error'

    ct_internal = len(model.objects.filter(integration_id=pk))
    if initialize == False or ct_internal > 0:
        data = utils.getOldestMentions(user_iden)
        Sync(data, pk, user_iden, handler, name, user_iden)

    """ 
        Historical Crawl
    """

    API = utils.twitter_auth(user_iden)

    max_id = Integrations_Twitter_Mentions.objects.filter(user_iden=user_iden).order_by('timestamp')[0].mention_id
    mentions_json = []
    try:
        for mention in Cursor(API[0].mentions_timeline, max_id=max_id).items():
            mention_json = mention._json
            mentions_json.append(mention_json)
        Sync(mentions_json, pk, user_iden, handler, name, user_iden)
        SLEEPTIME = 0
    except RateLimitError:
        SLEEPTIME = 1 if SLEEPTIME == 0 else SLEEPTIME * 2
        msg = f"Too many frequent requests sleeping for {SLEEPTIME} seconds"
        logger.debug(msg)
        return
    except TweepError as e:
        logger.debug(e)
        raise e

    return 'success'