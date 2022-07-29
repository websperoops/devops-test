from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render

from dashboards.integrations.twitter.integration import TwitterIntegration
from dashboards.models import Integrations_Twitter_Mentions

import json


@login_required
def index(request):
    return render(request, "dashboards/social.html")

@login_required
def mentions(request):

    user = request.user
    uid = user.id
    max_mentions = 20
    response = {}
    all_mentions = Integrations_Twitter_Mentions.objects.filter(user_iden=uid).order_by('-timestamp')
    # print(all_mentions)
    # if len(all_mentions) > max_mentions:
    #     all_mentions = all_mentions[0:max_mentions-1]

    # for mention in all_mentions:
    #     mention_json = {
    #         "screen_name":mention.other_user_screen_name,
    #         "text":mention.text,
    #         "mention_id":mention.mention_id,
    #         "platform":mention.integration,
    #         "timestamp":mention.timestamp,
    #     }
    #     response[mention.mention_id] = mention_json
    all_mentions = serializers.serialize('json',all_mentions)
    return HttpResponse(all_mentions, content_type="application/json")


@login_required
def messages(request):
    user = request.user
    uid = user.id
    messages  = TwitterIntegration.recentMessages(user,uid)
    return HttpResponse(json.dumps(messages), content_type="application/json")
@login_required
def updateStatus(request):
    if request.method == 'POST':
        user = request.user
        uid = user.id
        new_post = json.loads(request.body)['new_post']
        print(new_post)
        if len(new_post) != 0:
            TwitterIntegration.updateStatus(user,uid,new_post)
            return JsonResponse({"post":new_post}, safe=False)

@login_required
def reply(request):
    if request.method == "POST":
        user = request.user
        uid = user.id
        # TWEET_URL = r"https://api.twitter.com/1.1/statuses/update.json"
        tweet_to_respond_to = request.POST["mention_id"]
        other_user_handle = '@'+ request.POST["screen_name"]
        text = request.POST["text"]

        if other_user_handle not in text:
            text = other_user_handle + " " + text

        # TWEET_URL += "?status={}?in_reply_to_status_id={}".format(text, tweet_to_respond_to)

        if len(text) < 241:
            print(uid)
            response = TwitterIntegration.updateStatus(user, uid, text, reply_id=tweet_to_respond_to)
            # oauth = TwitterIntegration.genOAuthSession(uid)
            # resp = oauth.post(TWEET_URL)
            # response = resp.json()
            print(response, 'dddddd')
        else:
            response = {
                "":"Bad Request"
            }

        return JsonResponse(response, safe=False)



    pass
