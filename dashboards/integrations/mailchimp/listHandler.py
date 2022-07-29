from . import integration as mailchimp_integration
from . import mailchimpHandler

from dashboards.models import Integrations_MailChimp_Lists, Integrations_MailChimp_ListStats, Integrations_MailChimp_ListMembers

from django.contrib.auth.models import User as DjangoUser
from django.db import transaction

from ...enums.CoreEnums import Master_Blocklight_User


class ListHandler(mailchimpHandler.MailChimpHandler):

    def __init__(self, data, pk, user_iden, integration_name, name, ):
        self.lists = []
        self.stats = {}
        self.members = {}

        super(ListHandler, self).__init__(data, pk, user_iden, integration_name, name)
    def _Handler__save_independent_objects(self):

        with transaction.atomic():
            self.save_lists()
    
    def _Handler__save_dependent_objects(self):

        with transaction.atomic():
            self.save_stats()
            self.save_members()
    
    def _Handler__parse_data(self):
        for obj in self.data:
            list_id = obj.get("id", None)
            if list_id:
                chimp_list = Integrations_MailChimp_Lists(
                    list_id=list_id,
                    user_iden=self.user_iden,
                    web_id=obj.get("web_id", None),
                    name=obj.get("name", None),
                    contact=obj.get("contact", None),
                    date_created=obj.get("date_created", None),
                    list_rating=obj.get("list_rating", None),
                    stats=obj.get("stats", None),
                    integration_id=self.integration_id
                )
                self.lists.append(chimp_list)
                
                self.grab_stats(obj.get("stats", {}), obj.get("name", None), obj.get("date_created", None), list_id)
                try:
                    self.grab_members(list_id, self.user_iden)
                except Exception as e:
                    raise e

    def save_lists(self):
        for chimp_list in self.lists:
            self.update_or_save_instance(Integrations_MailChimp_Lists, chimp_list, "list_id")
    
    def save_stats(self):
        for l_id, l_stats in self.stats.items():
            mailchimp_list = self.get_instances_if_exists(
                Integrations_MailChimp_Lists,
                Integrations_MailChimp_Lists(list_id=l_id),
                "list_id"
            )
            if mailchimp_list:
                for stat in l_stats:
                    stat.stats_ref = mailchimp_list[0]
                    self.update_or_save_instance(Integrations_MailChimp_ListStats, stat, unique_attr='stats_id')
    
    def save_members(self):
        for l_id, l_members in self.members.items():
            mailchimp_list = self.get_instances_if_exists(
                Integrations_MailChimp_Lists,
                Integrations_MailChimp_Lists(list_id=l_id),
                "list_id"
            )
            if mailchimp_list:
                for member in l_members:
                    member.member_ref = mailchimp_list[0]
                    self.update_or_save_instance(Integrations_MailChimp_ListMembers, member, unique_attr="member_id")
                    
    def grab_stats(self, stats, name, date_created, list_id):
        if stats:
            mailchimp_list = Integrations_MailChimp_ListStats(
                user_iden = self.user_iden,
                list_name = name,
                date_created = date_created,
                stats_id = list_id,
                avg_sub_rate=stats.get("avg_sub_rate", None),
                open_rate=stats.get("open_rate", None),
                member_count=stats.get("member_count", None),
                click_rate=stats.get("click_rate", None),
                cleaned_count_since_send=stats.get("cleaned_count_since_send", None),
                member_count_since_send=stats.get("member_count_since_send", None),
                target_sub_rate=stats.get("target_sub_rate", None),
                last_sub_date=stats.get("last_sub_date", None),
                merge_field_count=stats.get("merge_field_count", None),
                avg_unsub_rate=stats.get("avg_unsub_rate", None),
                unsubscribe_count=stats.get("unsubscribe_count", None),
                cleaned_count=stats.get("cleaned_count", None),
                campaign_last_sent=stats.get("campaign_last_sent", None),
                unsubscribe_count_since_send=stats.get("unsubscribe_count_since_send", None),
                campaign_count=stats.get("campaign_count", None),
                last_unsub_date=stats.get("last_unsub_date", None),
                integration_id=self.integration_id
            )

            if list_id not in self.stats:
                self.stats[list_id] = [mailchimp_list]
            else:
                self.stats[list_id].append(mailchimp_list)
    
    def grab_members(self, list_id, user_id):
        integration = mailchimp_integration.MailchimpIntegration()
        user = DjangoUser.objects.get(id=user_id)
        #integration, user = mailchimp_integration.MailchimpIntegration(), DjangoUser.objects.get(id=Master_Blocklight_User.User_Id)
        auth_params = integration.build_auth_params('mailchimp', user)
        if auth_params != 'done':
            apis = integration.get_params(auth_params)
            for api in apis:
                if api['name'] == 'lists':
                    MailChimpAPI = api['data']['API']
                    records_synced = 0
                    REQ_LIMIT = 250
                    total_items = 1
                    while total_items >= 0:
                        data = MailChimpAPI.members.all(list_id, count=REQ_LIMIT, offset=records_synced)
                        total_items = data.get('total_items', 0)
                        members=data['members']
                        for member in members:
                            member_id = member.get("id", None)
                            if member_id:
                                l_member = Integrations_MailChimp_ListMembers(
                                    user_iden=self.user_iden,
                                    member_id=member_id,
                                    email_address=member.get("email_address", None),
                                    unique_email_id=member.get("unique_email_id", None),
                                    email_type=member.get("email_type", None),
                                    status=member.get("status", None),
                                    stats=member.get("stats", None),
                                    ip_signup=member.get("ip_signup", None),
                                    timestamp_signup=member.get("timestamp_signup", None),
                                    member_rating=member.get("member_rating", None),
                                    vip=member.get("vip", None),
                                    email_client=member.get("email_client", None),
                                    location=member.get("location", None),
                                    list_id=list_id,
                                    integration_id=self.integration_id
                                )

                                if list_id not in self.members:
                                    self.members[list_id] = [l_member]
                                else:
                                    self.members[list_id].append(l_member)

                        total_items -= records_synced
                        records_synced += REQ_LIMIT
