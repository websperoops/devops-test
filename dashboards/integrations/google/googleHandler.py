from dashboards.integrations.utils import Handler
import logging


class GoogleHandler(Handler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, name):

        '''
        This class is meant to be inherited to sync shopify objects/resources from the
        python shopify API wrapper library.


        Args:
            data (dict): API response data from the shopify wrapper library.
            integration_id (int): the id for the integraion
            user_iden (int): the user's id
            shop_id (int): the associated shops id
            name (str): hardcoded name specifying the core object/resource
        '''

        super(GoogleHandler, self).__init__(data, integration_id, user_iden, "google", name)
        Handler.log_behavior(f"successfully read in {self.name}, API response data into handler of length {self.batch_size}")

    def _Handler__save_independent_objects(self):
        pass

    def _Handler__save_dependent_objects(self):
        pass

    def _Handler__parse_data(self):
        pass
