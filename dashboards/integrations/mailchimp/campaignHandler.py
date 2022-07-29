from . import mailchimpHandler
from datetime import date
from dashboards.models import Integrations_MailChimp_Campaigns, Integrations_MailChimp_CampaignReports, Integrations_MailChimp_Campaigns_Bl_Insights

from django.db import transaction
from django.utils import timezone


class CampaignHandler(mailchimpHandler.MailChimpHandler):

    def __init__(self, data, pk, user_iden, integration_name, name):

        self.campaigns = []
        self.campaigninsights = []
        self.reports = {}

        super(CampaignHandler, self).__init__(data, pk, user_iden, integration_name, name)
    def _Handler__save_independent_objects(self):

        with transaction.atomic():
            self.save_campaigns()
            self.save_insights()

    def _Handler__save_dependent_objects(self):

        with transaction.atomic():
            self.save_reports()
            
    def _Handler__parse_data(self):

        for obj in self.data:
            campaign_id = obj.get('id', None)
            if campaign_id:
                settings_parse_container = obj.get('settings', None)
                report_summary = obj.get("report_summary", {})
                send_time = obj.get("send_time",None)
                campaign = Integrations_MailChimp_Campaigns(
                    campaign_id=campaign_id,
                    user_iden=self.user_iden,
                    integration_id=self.integration_id,
                    type=obj.get("type",None),
                    date_created=obj.get("create_time",None),
                    archive_url=obj.get("archive_url",None),
                    long_archive_url=obj.get("long_archive_url",None),
                    status=obj.get("status",None),
                    emails_sent=obj.get("emails_sent",None),
                    send_time=send_time,
                    content_type=obj.get("content_type",None),
                    recipients=obj.get("recipients",None),
                    settings=obj.get("settings",None),
                    title=settings_parse_container.get('title', None),
                    preview_text=settings_parse_container.get('preview_text', None),
                    tracking=obj.get("tracking",None),
                    report_summary=obj.get("report_summary", {}),
                    delivery_status=obj.get("delivery_status",None),
                    subject_line=settings_parse_container.get("subject_line", None),
                    from_name=settings_parse_container.get("from_name",None)
                )
                total_revenue = report_summary.get('ecommerce', {}).get("total_revenue", 0)
                total_orders = report_summary.get('ecommerce', {}).get("total_orders", 0)
                send_time=obj.get("send_time", str(timezone.now()))
                create_time=obj.get("create_time", str(timezone.now()))
                if send_time and create_time:
                    send_time = date(int(send_time[0:4]), int(send_time[5:7]), int(send_time[8:10]))
                    create_time = date(int(create_time[0:4]), int(create_time[5:7]), int(create_time[8:10]))
                    time_diff = send_time - create_time
                if type(total_revenue) == tuple:
                    total_revenue = total_revenue[0]
                    total_orders = total_orders[0]
                if total_orders == 0:
                    campaign_aov = 0
                else:
                    campaign_aov = total_revenue/total_orders
                insight = Integrations_MailChimp_Campaigns_Bl_Insights(
                    user_iden=self.user_iden,
                    integration_id=self.integration_id,
                    archive_url=obj.get("archive_url",None),
                    emails_sent=obj.get("emails_sent",None),
                    send_time=obj.get("send_time",None),
                    campaign_id=campaign_id,
                    subject_line=settings_parse_container.get("subject_line", None),
                    from_name=settings_parse_container.get("from_name",None),
                    open_rate = report_summary.get("open_rate", None),
                    click_rate = report_summary.get("click_rate", None),
                    subscriber_clicks = report_summary.get("subscriber_clicks", None),
                    total_spent = report_summary.get('ecommerce', {}).get("total_spent", 0),
                    total_revenue = total_revenue,
                    total_orders = total_orders,
                    clicks = report_summary.get("clicks", None),
                    opens = report_summary.get("opens", None),
                    unique_opens = report_summary.get("unique_opens", None),
                    type=obj.get("type",None),
                    date_created=obj.get(create_time),
                    long_archive_url=obj.get("long_archive_url",None),
                    status=obj.get("status",None),
                    title=settings_parse_container.get('title', None),
                    preview_text=settings_parse_container.get('preview_text', None),
                    campaign_aov=campaign_aov,
                    campaign_creation_time=time_diff.days
                )
                self.campaigns.append(campaign)
                self.campaigninsights.append(insight)
                self.grab_reports(report_summary, campaign_id, send_time)
        
    def save_campaigns(self):
        for campaign in self.campaigns:
            self.update_or_save_instance(Integrations_MailChimp_Campaigns, campaign, "campaign_id")
    
    def save_insights(self):
        for insight in self.campaigninsights:
            self.update_or_save_instance(Integrations_MailChimp_Campaigns_Bl_Insights, insight, "campaign_id")
        
    def save_reports(self):
        for c_id, reports in self.reports.items():
            report = self.get_instances_if_exists(
                Integrations_MailChimp_Campaigns,
                Integrations_MailChimp_Campaigns(campaign_id=c_id),
                "campaign_id"
            )
            if report:
                for rep in reports:
                    rep.campaign_ref = report[0]
                    self.update_or_save_instance(Integrations_MailChimp_CampaignReports, rep, unique_attr='campaign_id')

    def grab_reports(self, report_summary, campaign_id, send_time):
        if report_summary:
            report = Integrations_MailChimp_CampaignReports(
                integration_id = self.integration_id,
                campaign_id=campaign_id,
                user_iden = self.user_iden,
                create_time = send_time,
                open_rate = report_summary.get("open_rate", None),
                click_rate = report_summary.get("click_rate", None),
                subscriber_clicks = report_summary.get("subscriber_clicks", None),
                total_spent = report_summary.get('ecommerce', {}).get("total_spent", 0),
                total_revenue = report_summary.get('ecommerce', {}).get("total_revenue", 0),
                total_orders = report_summary.get('ecommerce', {}).get("total_orders", 0),
                clicks = report_summary.get("clicks", None),
                opens = report_summary.get("opens", None),
                unique_opens = report_summary.get("unique_opens", None),
            )

            if campaign_id not in self.reports:
                self.reports[campaign_id] = [report]

            else:
                self.reports[campaign_id].append(report) 
