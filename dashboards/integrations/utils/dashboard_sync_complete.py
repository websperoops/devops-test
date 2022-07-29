from allauth.socialaccount.models import SocialAccount

def dashboard_sync_complete(provider, user_id):
    soc_acc = SocialAccount.objects.filter(provider=provider, user_id = user_id).last()
    if soc_acc:
        soc_acc.extra_data.pop('Syncing', None)
        soc_acc.save()


def token_failure(provider, user_id):
    soc_acc = SocialAccount.objects.filter(
        provider=provider, user_id=user_id).last()
    soc_acc.extra_data['Force_Reauth'] = True
    soc_acc.save()