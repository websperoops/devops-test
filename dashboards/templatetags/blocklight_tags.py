from dashboards.models import Dashboard
from django import template


register = template.Library()


@register.inclusion_tag('layout/navtag_authenticated.html')
def get_social_navbar(user):
    """
    {% get_social_navbar user %}
    Returns:
    <LI>
        <a href="/dashboards/{{ account }}/{{account.0.id}}/" class="waves-effect waves-primary">
        <i class="mdi mdi-{{account}} m-r-5" ></i>
        {{ account.provider }}</a>
    </LI>
    <LI>
    ... next account
        </li> ad infinitum
    """
    dashboards = Dashboard.objects.filter(user=user)
    accounts = user.socialaccount_set.all()
    return {'accounts': accounts, 'dashboards': dashboards}
