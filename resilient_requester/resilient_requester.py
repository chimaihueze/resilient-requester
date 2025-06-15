import logging
import time
import random

import requests
from resilient_requester.helpers.helper_functions import check_params


class Requester:

    @staticmethod
    def get_request(url, proxy=None, headers=None, timeout=0, retries=0):

        proxy, headers, timeout, retries = check_params(proxy, headers, timeout, retries)

        attempts = 0

        while attempts <= retries:

            try:
                logging.info(f"Requesting page: {url}")
                response = requests.get(url=url, proxies=proxy, headers=headers, timeout=timeout)
                response.raise_for_status()
                logging.info(f"Request successful: {response.status_code}, returning response now.")
                return response
            except Exception as e:
                logging.error(f"Request failed: {e}")
                if attempts < retries:
                    attempts += 1
                    waiting_time = random.randint(1, 5)
                    logging.info(f"Retrying in {waiting_time} seconds...")
                    time.sleep(waiting_time)
                else:
                    logging.error(f"Maximum number of retries {retries} reached. Exiting...")
                    return None
        return None
