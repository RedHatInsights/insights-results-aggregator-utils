from gevent import monkey
from locust import HttpUser, task, between, run_single_user, events
from cached_property import cached_property
from dynaconf import Dynaconf, Validator
import os
import requests
import random
import logging

monkey.patch_socket()

conf_file = os.getenv("CONFIG_FILE_PATH", "../config_dev.toml")
env_var_prefix = os.getenv("ENV_VAR_PREFIX", "LOAD_TEST")

cfg = Dynaconf(
    envvar_prefix=env_var_prefix,
    settings_file=conf_file,
    environments=True,
    default_env="load_test",
    validators=[
        Validator("login_mode", must_exist=True),
        Validator("api_url", must_exist=True),
        Validator("organization", must_exist=True)
    ]
)


class APIUser(HttpUser):

    wait_time = between(0.1, 1)
    # for debug only, will be overwritten by configuration
    host = "https://console.redhat.com"

    def on_start(self):

        if cfg.login_mode == "token":
            self.login()
        elif cfg.login_mode == 'proxy':
            self.auth = (cfg.username, cfg.password)

    def login(self):

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = "grant_type=refresh_token&client_id={}&refresh_token={}".format(
            cfg.client_id, cfg.offline_token
        )
        response = requests.post(cfg.login_url, headers=headers, data=payload)
        self.access_token = response.json()["access_token"]

    @cached_property
    def clusters(self):
        path = f'/api/insights-results-aggregator/v1/organizations/{cfg.organization}/clusters'
        response = self.get_api_call(path)
        payload = response.json()
        return payload["clusters"]

    @task
    def retrieve_org_overview(self):

        self.get_api_call("/api/insights-results-aggregator/v1/org_overview")

    @task
    def retrieve_cluster_list(self):

        path = f"/api/insights-results-aggregator/v1/organizations/{cfg.organization}/clusters"
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

        path = f"{cfg.api_url}{path}"

        if cfg.login_mode == 'token':
            headers = {
                "Accept": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            }
            response = self.client.get(path, headers=headers)

        elif cfg.login_mode == 'proxy':
            response = requests.get(path, cfg.proxy, auth=self.auth)

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
