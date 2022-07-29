from . import instagramHandler
from dashboards.models import Integrations_Instagram_Media_Objects

from django.db import transaction
from django.utils import timezone


class InstagramInsightHandler(instagramHandler.InstagramHandler):

    def __init__(self, data, integration_id, user_iden, name,account_name, insight_model):

        self.insights = {}
        self.insight_model = insight_model
        super(InstagramInsightHandler, self).__init__(data, integration_id,user_iden, name, account_name)


    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_insights(self.insight_model)

    def _Handler__save_dependent_objects(self):
        return

    def _Handler__parse_data(self):
        for obj in self.data:
            self.grab_insight(obj, self.insight_model)

    def save_insights(self, insight_model):
        for media_id,insights in self.insights.items():
            if media_id:
                objects = self.get_instances_if_exists( Integrations_Instagram_Media_Objects,
                                              Integrations_Instagram_Media_Objects(media_id=media_id),
                                             unique_attr="media_id")
                for insight in insights:
                    insight.media_object_ref=objects[0]

                    self.update_or_save_instance(
                    insight_model,
                    insight,
                    ["user_iden","record_id"]
                    )
            else:
                for insight in insights:
                    self.update_or_save_instance(
                    insight_model,
                    insight,
                    ["user_iden","record_id"]
                    )

    def grab_insight(self, obj, insight_model):

        base_record_id = obj.get("id",None)
        description = obj.get("description",None)
        name=obj.get("name",None),
        title=obj.get("title",None),
        period=obj.get("period",None)

        values = obj.get("values",None)

        media_id = obj.get("media_id",None)


        if base_record_id and values:
            base_record_id += self.integration_name

        for json in values:

            end_time = json.get("end_time",None)
            value = json.get("value",None)
            if end_time:
                record_id = base_record_id + end_time
            else:
                record_id = base_record_id

            if type(value) == dict:
                val_struct = value
            else:
                val_struct = {'':value}

            for k, v in val_struct.items():
                record_id += k

                insight = insight_model(
                    integration_id=self.integration_id,
                    integration_name=self.integration_name,
                    user_iden=self.user_iden,
                    last_sync_time=timezone.now(),
                    record_id=record_id,
                    description=description,
                    name=name,
                    title=title,
                    period=period,
                    value=v,
                    end_time=end_time,
                    account_name=self.account_name
                )


                if media_id in self.insights:
                    self.insights[media_id].append(insight)
                else:
                    self.insights[media_id] = [insight]
