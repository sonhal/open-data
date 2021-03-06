

from src.data import make_work_ads_data_set
import unittest
import requests


class TestMakeData(unittest.TestCase):

    def test_work_ads_data_set_api_endpoints(self):
        oldest_data_set = 2002
        current_newest_data_set = 2017
        api_base = make_work_ads_data_set.API_URL_BASE

        for year in range(oldest_data_set, current_newest_data_set):
            data_set_api_endpoint = api_base + str(year)
            result = requests.api.get(data_set_api_endpoint)
            self.assertEqual(200, result.status_code, "Endpoint request failed for: " + data_set_api_endpoint)
