from . import facebookHandler
from dashboards.models import Integrations_Facebook_Page_Posts
from django.db import transaction
from django.utils import timezone


class FacebookInsightHandler(facebookHandler.FacebookHandler):

    def __init__(self, data, integration_id, user_iden, name,account_name, insight_model):

        self.insight_model = insight_model
        super(FacebookInsightHandler, self).__init__(data, integration_id,user_iden, name, account_name)


    def _Handler__save_independent_objects(self):
        self.save_insights(self.insight_model)


    def _Handler__save_dependent_objects(self):
        return


    def _Handler__parse_data(self):
        for obj in self.data:
            self.grab_insight(obj, self.insight_model)


    def save_insight_chunk(self, insight_model, post_id,insights):
        with transaction.atomic():

            FacebookInsightHandler.logger.info("New Insight TXN")
            if post_id:
                objects = self.get_instances_if_exists(Integrations_Facebook_Page_Posts,
                                              Integrations_Facebook_Page_Posts(post_id=post_id),
                                             unique_attr="post_id")

                for insight in insights:
                    insight.post_ref=objects[0]

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


    def save_insights(self, insight_model):
        CHUNK_SIZE = 250
        for post_id,insights in self.insights.items():
            print(len(insights))
            if len(insights) < CHUNK_SIZE:
                self.save_insight_chunk(insight_model, post_id, insights)

            else:
                for idx in range(0, len(insights), CHUNK_SIZE):
                    try:
                        chunk = insights[idx:idx + CHUNK_SIZE]
                    except IndexError as e:
                        chunk = insights[idx::]

                    self.save_insight_chunk(insight_model, post_id, chunk)


            if post_id:
                objects = self.get_instances_if_exists(Integrations_Facebook_Page_Posts,
                                              Integrations_Facebook_Page_Posts(post_id=post_id),
                                             unique_attr="post_id")

                for insight in insights:
                    insight.post_ref=objects[0]

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

        post_id = obj.get("post_id",None)


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

                insight = insight_model(
                    integration_id=self.integration_id,
                    integration_name=self.integration_name,
                    user_iden=self.user_iden,
                    last_sync_time=timezone.now(),
                    record_id=(record_id + k),
                    description=description,
                    name=name,
                    title=title,
                    period=period,
                    value=v,
                    end_time=end_time,
                    account_name=self.account_name
                )


                if post_id in self.insights:
                    self.insights[post_id].append(insight)
                else:
                    self.insights[post_id] = [insight]
