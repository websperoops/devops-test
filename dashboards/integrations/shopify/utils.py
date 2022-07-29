from dashboards.integrations.utils.dashboard_sync_complete import token_failure
from pyactiveresource.connection import UnauthorizedAccess, ClientError, ServerError
import time


def shopify_api_request(APIfunc, logger, user_id, *args, **kwargs):
    SLEEPTIME = 1
    while True:
        try:
            data = APIfunc(**kwargs)
            SLEEPTIME = 1
            break
        except ClientError as e:
            if e.code == 429:
                msg=f"Too many frequent requests sleeping for {SLEEPTIME} seconds"
                logger.info(msg)
                time.sleep(SLEEPTIME)
                SLEEPTIME *= 2
            elif e.code == 401:
                token_failure('shopify', user_id)
                raise e
            else:
                raise e

        except ServerError as e:
            msg=f"Too many frequent requests sleeping for {SLEEPTIME} seconds"
            logger.info(msg)
            time.sleep(SLEEPTIME)
            SLEEPTIME *= 2
    return data
