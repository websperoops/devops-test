from dashboards.integrations.utils import Handler
import logging


class MailChimpHandler(Handler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, pk, user_iden, integration_name, name, model=None):

        super(MailChimpHandler, self).__init__(data, pk, user_iden, integration_name, name)
    
    def __save_independent_objects(self):
        return


    def __save_dependent_objects(self):
        return

    def __parse_data(self):
        return