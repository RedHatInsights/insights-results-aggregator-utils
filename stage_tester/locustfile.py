from gevent import monkey
from locust import HttpUser, task, between, run_single_user, events
from functools import cached_property
import os
import requests
import configparser
import random
import logging

monkey.patch_socket()

conf_file = os.getenv("CONFIG_FILE_PATH", "../dev.conf")
env_var_prefix = os.getenv("ENV_VAR_PREFIX", "LOAD_TEST_DEV_")


class APIUser(HttpUser):

    wait_time = between(0.1, 1)
    # for debug only, will be overwritten by configuration
    host = "https://console.redhat.com"

    def on_start(self):

        self.configure()
        self.login()

    def configure(self):
        cfg = configparser.ConfigParser()
        cfg.read(conf_file)

        self.offline_token = cfg["load_test"]["offline_token"]
        self.client_id = cfg["load_test"]["client_id"]
        self.api_url = cfg["load_test"]["api_url"]
        self.login_url = cfg["load_test"]["login_url"]
        self.organization = cfg["load_test"]["organization"]

    def login(self):

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = "grant_type=refresh_token&client_id={}&refresh_token={}".format(
            self.client_id, self.offline_token
        )
        response = requests.post(self.login_url, headers=headers, data=payload)
        self.access_token = response.json()["access_token"]

    @cached_property
    def clusters(self):
        path = f'/api/insights-results-aggregator/v1/organizations/{self.organization}/clusters'
        response = self.get_api_call(path)
        payload = response.json()
        return payload["clusters"]

    @task
    def retrieve_org_overview(self):

        self.get_api_call("/api/insights-results-aggregator/v1/org_overview")

    @task
    def retrieve_cluster_list(self):

        path = f"/api/insights-results-aggregator/v1/organizations/{self.organization}/clusters"
        self.get_api_call(path)

    @task
    def retrieve_additional_info(self):
        self.get_api_call("/api/insights-results-aggregator/v1/info")

    @task
    def retrieve_results_for_cluster(self):

        uuid = random.choice(self.clusters)
        self.get_api_call(
            f"/api/insights-results-aggregator/v1/clusters/{uuid}/report"
        )

    def get_api_call(self, path):

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        response = self.client.get(path, headers=headers)

        # elementary check for response content
        assert response is not None, "Proper response expected"

        return response


@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.1:
        logging.error("Test failed due to failure ratio > 10%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 500:
        logging.error("Test failed due to average response time ratio > 500 ms")
        environment.process_exit_code = 1
    elif environment.stats.total.get_response_time_percentile(0.95) > 1000:
        logging.error("Test failed due to 95th percentile response time > 1 s")
        environment.process_exit_code = 1
    else:
        environment.process_exit_code = 0


if __name__ == "__main__":

    print("load testing debug")

    run_single_user(APIUser)
