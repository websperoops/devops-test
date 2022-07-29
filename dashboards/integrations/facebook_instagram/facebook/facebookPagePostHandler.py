import datetime

from dashboards.integrations.facebook_instagram.facebook import fb_api, facebookInsightHandler
from dashboards.models import Integrations_Facebook_Page_Posts, Integrations_Facebook_Page_Post_Impressions, \
    Integrations_Facebook_Page_Post_Engagements, Integrations_Facebook_Page_Post_Reactions

from django.db import transaction
from . import facebookHandler


class FacebookPagePostHandler(facebookHandler.FacebookHandler):

    def __init__(self, data, integration_id, user_iden, name, account_name, model):
        self.posts = []
        self.impressions = []
        self.engagements = []
        self.reactions = []
        super(FacebookPagePostHandler, self).__init__(
            data, integration_id, user_iden, name, account_name)

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_fb_posts()

    def _Handler__save_dependent_objects(self):
        impressionsHandler = facebookInsightHandler.FacebookInsightHandler(
            self.impressions, self.integration_id, self.user_iden, self.name, self.account_name, Integrations_Facebook_Page_Post_Impressions)
        impressionsHandler.save_all_objects()
        engagementsHandler = facebookInsightHandler.FacebookInsightHandler(
            self.engagements, self.integration_id, self.user_iden, self.name, self.account_name, Integrations_Facebook_Page_Post_Engagements)
        engagementsHandler.save_all_objects()
        reactionsHandler = facebookInsightHandler.FacebookInsightHandler(
            self.reactions, self.integration_id, self.user_iden, self.name, self.account_name, Integrations_Facebook_Page_Post_Reactions)
        reactionsHandler.save_all_objects()

    def _Handler__parse_data(self):
        for obj in self.data:
            scheduled_publish_time = obj.get("scheduled_publish_time", None)
            if scheduled_publish_time:
                scheduled_publish_time = datetime.datetime.fromtimestamp(
                    scheduled_publish_time).strftime('%G-%m-%d %H:%M:%S')

            post = Integrations_Facebook_Page_Posts(
                integration_id=self.integration_id,
                integration_name=self.integration_name,
                user_iden=self.user_iden,
                post_id=obj.get("id", None),
                admin_creator=obj.get("admin_creator", None),
                created_time=obj.get("created_time", None),
                _from=obj.get("from", None),
                full_picture=obj.get("full_picture", None),
                icon=obj.get("icon", None),
                is_expired=obj.get("is_expired", None),
                is_instagram_eligible=obj.get("is_instagram_eligible", None),
                is_popular=obj.get("is_popular", None),
                is_published=obj.get("is_published", None),
                message=obj.get("message", None),
                parent_id=obj.get("parent_id", None),
                permalink=obj.get("permalink_url", None),
                promotion_status=obj.get("promotion_status", None),
                scheduled_publish_time=scheduled_publish_time,
                shares=obj.get("shares", None),
                status_type=obj.get("status_type", None),
                timeline_visibility=obj.get("timeline_visibility", None),
                updated_time=obj.get("updated_time", None),
            )
            self.posts.append(post)
            self.grab_insights(obj.get("id", None))

    def save_fb_posts(self):
        for post in self.posts:
            self.update_or_save_instance(Integrations_Facebook_Page_Posts,
                                         post,
                                         "post_id")

    def grab_insights(self, post_id):
        enagagements = fb_api.FB_API.get_fb_page_published_post_enagagements(post_id)[
            "data"]
        for insight in enagagements:
            insight["post_id"] = post_id
            self.engagements.append(insight)
        impressions = fb_api.FB_API.get_fb_page_published_post_impressions(post_id)[
            "data"]
        for insight in impressions:
            insight["post_id"] = post_id
            self.impressions.append(insight)
        reactions = fb_api.FB_API.get_fb_page_published_post_reactions(post_id)[
            "data"]
        for insight in reactions:
            insight["post_id"] = post_id
            self.reactions.append(insight)
