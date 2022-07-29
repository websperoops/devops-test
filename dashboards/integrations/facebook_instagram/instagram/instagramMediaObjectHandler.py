from . import instagramHandler

from dashboards.integrations.facebook_instagram.instagram import ig_api, instagramInsightHandler
from dashboards.models import Integrations_Instagram_Media_Objects, Integrations_Instagram_Media_Insights_Impressions, \
Integrations_Instagram_Media_Insights_Engagements,Integrations_Instagram_Media_Insights_Reach, Integrations_Instagram_Media_Insights_Saved, \
Integrations_Instagram_Media_Insights_Video_Views, Integrations_Instagram_Media_Insights_Story_Replies, \
Integrations_Instagram_Media_Insights_Story_Taps_Fwd, Integrations_Instagram_Media_Insights_Story_Taps_Back, \
Integrations_Instagram_Media_Insights_Story_Exits

from django.utils import timezone
from django.db import transaction


class InstagramMediaObjectHandler(instagramHandler.InstagramHandler):

    def __init__(self, data, integration_id, user_iden, name,account_name,is_story):
        self.is_story = is_story
        self.media_objects = []
        self.engagements = []
        self.impressions = []
        self.reach = []
        self.saved = []
        self.video_views = []
        self.story_exits = []
        self.story_replies = []
        self.story_taps_forward = []
        self.story_taps_back = []


        super(InstagramMediaObjectHandler, self).__init__(data, integration_id,user_iden, name, account_name)


    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_media_objects()

    def _Handler__save_dependent_objects(self):

        if not self.is_story:
            engagementHandler = instagramInsightHandler.InstagramInsightHandler(self.engagements,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Engagements)
            engagementHandler.save_all_objects()
            impressionHandler = instagramInsightHandler.InstagramInsightHandler(self.impressions,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Impressions)
            impressionHandler.save_all_objects()
            reachHandler = instagramInsightHandler.InstagramInsightHandler(self.reach,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Reach)
            reachHandler.save_all_objects()
            savedHandler = instagramInsightHandler.InstagramInsightHandler(self.saved,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Saved)
            savedHandler.save_all_objects()
            videoViewsHandler = instagramInsightHandler.InstagramInsightHandler(self.video_views,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Video_Views)
            videoViewsHandler.save_all_objects()
        else:
            exitHandler = instagramInsightHandler.InstagramInsightHandler(self.story_exits,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Story_Exits)
            exitHandler.save_all_objects()
            repliesHandler = instagramInsightHandler.InstagramInsightHandler(self.story_replies,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Story_Replies)
            repliesHandler.save_all_objects()
            tapsForwardHandler = instagramInsightHandler.InstagramInsightHandler(self.story_taps_forward,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Story_Taps_Fwd)
            tapsForwardHandler.save_all_objects()
            tapsBackHandler = instagramInsightHandler.InstagramInsightHandler(self.story_taps_back,self.integration_id,self.user_iden,self.name,self.account_name,Integrations_Instagram_Media_Insights_Story_Taps_Back)
            tapsBackHandler.save_all_objects()

    def _Handler__parse_data(self):
        for obj_id in self.data:
            obj = ig_api.IG_API.get_ig_media(obj_id["id"])

            media_object = Integrations_Instagram_Media_Objects(
                integration_id=self.integration_id,
                integration_name=self.integration_name,
                user_iden=self.user_iden,
                media_id = obj.get("id",None),
                media_type=obj.get("media_type",None),
                media_url=obj.get("media_url",None),
                owner_id = obj.get("owner",{}).get("id",None),
                username=obj.get("username",None),
                caption=obj.get("caption",None),
                comments_count=obj.get("comments_count",None),
                permalink=obj.get("permalink",None),
                timestamp = obj.get("timestamp",timezone.now()),
                is_story=self.is_story
            )
            self.media_objects.append(media_object)
            self.grab_media_insights(
                                     obj.get("id",None),
                                     obj.get("media_type",None)
                                     )

    def grab_media_insights(self,media_id,media_type):

        mapping = {
            "engagement":self.engagements,
            "impressions":self.impressions,
            "reach":self.reach,
            "saved":self.saved,
            "video_views":self.video_views,
            "carousel_album_engagement":self.engagements,
            "carousel_album_impressions":self.impressions,
            "carousel_album_reach":self.reach,
            "carousel_album_saved":self.saved
            }

        if self.is_story == True:
            response = ig_api.IG_API.get_ig_story_insights(media_id)
            mapping = {
                "exits":self.story_exits,
                "impressions":self.impressions,
                "reach":self.reach,
                "replies":self.story_replies,
                "taps_forward":self.story_taps_forward,
                "taps_back":self.story_taps_back
            }

        elif media_type == 'IMAGE' :
            response = ig_api.IG_API.get_ig_image_insights(media_id)

        elif media_type == 'VIDEO':
            response = ig_api.IG_API.get_ig_video_insights(media_id)

        elif media_id == 'CAROUSEL_ALBUM':
            response = ig_api.IG_API.get_ig_media_carousel_insights(media_id)

        else:
            response = {"data":[]}

        for object_insight in response["data"]:
            struct = mapping[object_insight["name"]]
            object_insight["media_id"] = media_id
            struct.append(object_insight)




    def save_media_objects(self):
        for obj in self.media_objects:
            self.update_or_save_instance(Integrations_Instagram_Media_Objects,
                                         obj,
                                         ["media_id",
                                          "user_iden"]
                                         )
