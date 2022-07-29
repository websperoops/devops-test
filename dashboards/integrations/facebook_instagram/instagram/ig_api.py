import requests


class IG_API(object):

    BASE_URL = "https://graph.facebook.com/v8.0/"
    PAGE_TOKEN = ''
    IG_USER_ID = ''

    def get_ig_page_details(page_id, api_access_token):
        page_url = "{}{}?fields=instagram_business_account,access_token&access_token={}".format(
            IG_API.BASE_URL, page_id, api_access_token)
        json_response = requests.get(page_url).json()
        if 'access_token' not in json_response:
            err_msg = str(json_response)
            raise IOError(err_msg)
        else:
            return json_response

    def __init__(self, page_id, api_access_token):
        page_details = IG_API.get_ig_page_details(page_id, api_access_token)
        IG_API.PAGE_TOKEN = page_details['access_token']
        IG_API.IG_USER_ID = page_details['instagram_business_account']['id']

    def get_ig_insights(ig_media_id=None, period='day', metrics="", since=None, until=None, is_post_level=False):

        scope_mapping = {
            True: ig_media_id,
            False: IG_API.IG_USER_ID
        }

        object_id = scope_mapping[is_post_level]

        if not object_id:
            err_msg = '''Need to pass in correspoding value for insight API scope level
                        \nis_post_level: {}\nig_user_id: {}\nig_media_id: {}'''.format(is_post_level, ig_user_id, ig_media_id)

            raise ValueError(err_msg)

        else:
            insight_api_url = '''{}{}/insights?metric={}'''.format(
                IG_API.BASE_URL, object_id, metrics)

            if period:
                insight_api_url += "&period={}".format(period)
            if since:
                insight_api_url += "&since={}".format(since)
            if until:
                insight_api_url += "&until={}".format(until)

            insight_api_url += "&access_token={}".format(IG_API.PAGE_TOKEN)

            json_response = requests.get(insight_api_url).json()
            if 'error' in json_response and json_response['error'].get("error_user_title", None) == 'Media Posted Before Business Account Conversion':
                return {"data": []}

            elif 'data' not in json_response:
                err_msg = str(json_response)
                limit_flag = 'last 2 years'
                if limit_flag in err_msg:
                    return {"data": []}
                else:
                    raise IOError(err_msg)

            else:
                return json_response

    def get_ig_account_impressions(period='day', since=None, until=None):

        return IG_API.get_ig_insights(ig_media_id=None,
                                      period=period,
                                      metrics="impressions",
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_ig_account_reach(period='day', since=None, until=None):

        return IG_API.get_ig_insights(ig_media_id=None,
                                      period=period,
                                      metrics="reach",
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_ig_account_followers(period='day', since=None, until=None):

        metrics = '''email_contacts,get_directions_clicks,
                     profile_views,text_message_clicks,
                     website_clicks,phone_call_clicks'''

        return IG_API.get_ig_insights(ig_media_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )
    
    def get_ig_account_follower_count(period='day', since=None, until=None):
        metrics = '''follower_count'''

        return IG_API.get_ig_insights(ig_media_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_ig_account_object_ids(object_type, period='day', since=None, until=None):

        media_id_api_url = "{}{}/{}?".format(IG_API.BASE_URL,
                                             IG_API.IG_USER_ID, object_type)
        if since:
            media_id_api_url += "&since={}".format(since)

        if until:
            media_id_api_url += "&until={}".format(until)

        media_id_api_url += "&access_token={}".format(IG_API.PAGE_TOKEN)
        json_response = requests.get(media_id_api_url).json()
        if 'data' not in json_response:
            err_msg = str(json_response)
            raise IOError(err_msg)

        else:
            return json_response

    def get_ig_account_media_ids(period='day', since=None, until=None):

        return IG_API.get_ig_account_object_ids("media",
                                                period=period,
                                                since=since,
                                                until=until
                                                )

    def get_ig_account_story_ids(period='day', since=None, until=None):

        return IG_API.get_ig_account_object_ids("stories",
                                                period=period,
                                                since=since,
                                                until=until
                                                )

    def get_ig_media(ig_media_id=None):
        media_fields = "id,media_type,media_url,owner,username,caption,comments_count,permalink,timestamp"

        if not ig_media_id:
            err_msg = '''Need to pass in media_id to get media_object
                        \nig_media_id: {}'''.format(ig_media_id)

            raise ValueError(err_msg)

        else:
            media_url = "{}{}?fields={}&access_token={}".format(
                IG_API.BASE_URL, ig_media_id, media_fields, IG_API.PAGE_TOKEN)
            json_response = requests.get(media_url).json()

            return json_response

    def get_ig_image_insights(ig_media_id):
        metrics = "engagement,impressions,reach,saved"
        return IG_API.get_ig_insights(ig_media_id, period=None, metrics=metrics, is_post_level=True)

    def get_ig_video_insights(ig_media_id):
        metrics = "engagement,impressions,reach,saved,video_views"
        return IG_API.get_ig_insights(ig_media_id, period=None, metrics=metrics, is_post_level=True)

    def get_ig_media_carousel_insights(ig_media_id):
        metrics = "carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved"
        return IG_API.get_ig_insights(ig_media_id, period=None, metrics=metrics, is_post_level=True)

    def get_ig_story_insights(ig_media_id):
        metrics = "exits,impressions,reach,replies,taps_forward,taps_back"
        return IG_API.get_ig_insights(ig_media_id, period=None, metrics=metrics, is_post_level=True)
