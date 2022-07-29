from . import twitterHandler
from allauth.socialaccount.models import SocialAccount
from dashboards.models import Integrations_Twitter_Mentions
from django.db import transaction
import logging


logger = logging.getLogger(__name__)


class MentionsHandler(twitterHandler.TwitterHandler):

    def __init__(self, data, integration_name, user_iden):

        self.mentions = []
        super(MentionsHandler, self).__init__(data, integration_name, user_iden, 'twitter', 'mentions')

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_mentions()

    def _Handler__save_dependent_objects(self):
        pass

    """     
    args - response.JSON
    """
    def _Handler__parse_data(self):

        for item in self.data:
            print("_Handler__parse_data item: {}".format(item))
            # uid = item.get('')
            # create a database tuple object for every mention pulled from api
            mention = Integrations_Twitter_Mentions(
                integration=SocialAccount.objects.get(provider='twitter', user_id=self.user_iden),
                integration_name="twitter",
                user_iden=self.user_iden,
                mention_id=item.get("id_str", None),
                text=item.get("text", None),
                other_user_id=item.get("user", {}).get("id_str", None),
                other_user_name=item.get("user", {}).get("name", None),
                other_user_screen_name=item.get("user", {}).get("screen_name", None),
                timestamp=self.getTimeStamp(item.get("created_at", None)))
            self.mentions.append(mention)

    def save_mentions(self):
        for mention in self.mentions:
            self.update_or_save_instance(Integrations_Twitter_Mentions, mention, "mention_id")
