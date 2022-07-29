import requests
import time


class FB_API(object):

    BASE_URL = "https://graph.facebook.com/v8.0/"
    PAGE_TOKEN = ''
    PAGE_ID = ''

    def get_fb_page_details(page_id, api_access_token):
        page_url = "{}{}?fields=access_token&access_token={}".format(
            FB_API.BASE_URL, page_id, api_access_token)
        json_response = requests.get(page_url).json()
        if 'access_token' not in json_response:
            err_msg = str(json_response)
            raise IOError(err_msg)
        else:
            return json_response

    def __init__(self, page_id, api_access_token):
        page_details = FB_API.get_fb_page_details(page_id, api_access_token)
        FB_API.PAGE_TOKEN = page_details['access_token']
        FB_API.PAGE_ID = page_id

    def get_fb_insights(fb_post_id=None, period='day', metrics="", since=None, until=None, is_post_level=False):

        scope_mapping = {
            True: fb_post_id,
            False: FB_API.PAGE_ID
        }

        object_id = scope_mapping[is_post_level]

        if not object_id:
            err_msg = '''Need to pass in correspoding value for insight API scope level
                        \nis_post_level: {}\fb_page_id: {}\fb_post_id: {}'''.format(is_post_level, FB_API.PAGE_ID, fb_post_id)

            raise ValueError(err_msg)

        else:
            insight_api_url = '''{}{}/insights?'''.format(
                FB_API.BASE_URL, object_id)

            if metrics != None:
                insight_api_url += "metric={}&".format(metrics)

            if period:
                insight_api_url += "period={}&".format(period)
            if since:
                insight_api_url += "since={}&".format(since)
            if until:
                insight_api_url += "until={}&".format(until)

            insight_api_url += "access_token={}".format(FB_API.PAGE_TOKEN)

            print(insight_api_url)
            tries = 3

            while tries != 0:

                json_response = requests.get(insight_api_url).json()
                if 'error' in json_response:
                    time.sleep(1)
                    tries -= 1
                else:
                    return json_response

            err_msg = str(json_response)
            raise IOError(err_msg)

    def get_fb_page_views(period='day', since=None, until=None):

        metrics = '''page_views_total,page_views_logout,page_views_logged_in_total,page_views_logged_in_unique,
        page_views_external_referrals,page_views_by_profile_tab_total,page_views_by_age_gender_logged_in_unique'''

        return FB_API.get_fb_insights(fb_post_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_fb_page_impressions(period='day', since=None, until=None):

        metrics = '''page_impressions,page_impressions_unique,page_impressions_paid,
        page_impressions_paid_unique,page_impressions_organic,
        page_impressions_organic_unique,page_impressions_viral,
        page_impressions_viral_unique,
        page_impressions_nonviral,page_impressions_by_story_type,
        page_impressions_by_story_type_unique,page_impressions_by_city_unique,
        page_impressions_by_country_unique,page_impressions_by_locale_unique,
        page_impressions_by_age_gender_unique,page_impressions_frequency_distribution,
        page_impressions_viral_frequency_distribution'''

        return FB_API.get_fb_insights(fb_post_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_fb_page_engagements(period='day', since=None, until=None):

        metrics = '''page_engaged_users,page_consumptions,
                    page_consumptions_unique,page_consumptions_by_consumption_type,
                    page_consumptions_by_consumption_type_unique,page_places_checkin_total,
                    page_places_checkin_total_unique,page_places_checkin_mobile,
                    page_places_checkin_mobile_unique,page_places_checkins_by_age_gender,
                    page_fans_online,page_fans_online_per_day,page_fan_adds_by_paid_non_paid_unique,
                    page_negative_feedback,page_negative_feedback_unique,
                    page_negative_feedback_by_type,page_negative_feedback_by_type_unique,page_positive_feedback_by_type,
                    page_positive_feedback_by_type_unique,page_fans_online,page_fans_online_per_day,
                    page_fan_adds_by_paid_non_paid_unique
                    '''

        return FB_API.get_fb_insights(fb_post_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_fb_page_reactions(period='day', since=None, until=None):

        metrics = '''page_actions_post_reactions_like_total,page_actions_post_reactions_like_total,
        page_actions_post_reactions_love_total,page_actions_post_reactions_wow_total,
        page_actions_post_reactions_haha_total,page_actions_post_reactions_sorry_total,
        page_actions_post_reactions_anger_total,page_actions_post_reactions_total'''

        return FB_API.get_fb_insights(fb_post_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_fb_page_demographics(period='day', since=None, until=None):

        metrics = '''page_fans,page_fans_locale,page_fans_city,page_fans_country,
                    page_fans_gender_age,page_fan_adds,page_fan_adds_unique,
                    page_fans_by_like_source,page_fans_by_like_source_unique,page_fan_removes,
                    page_fan_removes_unique,page_fans_by_unlike_source_unique'''

        return FB_API.get_fb_insights(fb_post_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_fb_page_posts(period='day', since=None, until=None):

        metrics = '''page_posts_impressions,page_posts_impressions_unique,
                    page_posts_impressions_paid,page_posts_impressions_paid_unique,
                    page_posts_impressions_organic,page_posts_impressions_organic_unique'''

        return FB_API.get_fb_insights(fb_post_id=None,
                                      period=period,
                                      metrics=metrics,
                                      since=since,
                                      until=until,
                                      is_post_level=False
                                      )

    def get_fb_page_published_posts(period='day', since=None, until=None):

        fields = '''id%2Cadmin_creator%2Ccreated_time%2Cfrom%2Cfull_picture%2Cicon%2Cis_expired%2Cis_instagram_eligible%2Cis_popular%2C\
                   is_published%2Cmessage%2Cparent_id%2Cpermalink_url%2Cpromotion_status%2Cscheduled_publish_time%2C\
                   shares%2Cstatus_type%2Ctimeline_visibility%2Cupdated_time'''

        post_url = f'''https://graph.facebook.com/v9.0/{FB_API.PAGE_ID}/published_posts?fields={fields}'''
        if since:
            post_url += "since={}&".format(since)
        if until:
            post_url += "until={}&".format(until)

        post_url += "{}&access_token={}".format(fields, FB_API.PAGE_TOKEN)

        print(post_url)
        json_response = requests.get(post_url).json()
        if 'data' not in json_response:
            err_msg = json_response
            raise IOError(err_msg)
        else:
            return json_response

    def get_fb_page_published_post_enagagements(post_id):

        return FB_API.get_fb_insights(
            fb_post_id=post_id,
            period=None,
            metrics="post_engaged_users,post_negative_feedback,post_negative_feedback_unique,\
                     post_engaged_fan,post_clicks,post_clicks_unique",
            is_post_level=True
        )

    def get_fb_page_published_post_impressions(post_id):

        return FB_API.get_fb_insights(
            fb_post_id=post_id,
            period=None,
            metrics="post_impressions,post_impressions_unique,post_impressions_paid,post_impressions_paid_unique,\
            post_impressions_fan,post_impressions_fan_unique,post_impressions_fan_paid,post_impressions_fan_paid_unique,\
            post_impressions_organic,post_impressions_organic_unique,post_impressions_viral,post_impressions_viral_unique,\
            post_impressions_nonviral,post_impressions_nonviral_unique",
            is_post_level=True
        )

    def get_fb_page_published_post_reactions(post_id):

        return FB_API.get_fb_insights(
            fb_post_id=post_id,
            period=None,
            metrics="post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total,post_reactions_haha_total,\
                     post_reactions_sorry_total,post_reactions_anger_total",
            is_post_level=True
        )
