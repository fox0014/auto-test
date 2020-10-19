import random
from locust import HttpUser, task, between, TaskSet
import json

class GamestartUser(TaskSet):

    def login(self):
        self.header = {'Accept': '*/*', 'clientType': 'json', 'appVersion': '10000', 'language': 'en_US',
                       'Content-Type': 'application/json',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        loginAccountForm = {
            "appType": "xxx",
            "password": "xxxx",
            "platform": "app",
            "uid": "xxxx"
        }
        # login to the application
        with self.client.post('/user/api/v1/login', data=json.dumps(loginAccountForm),
                         headers=self.header, catch_response=True) as response:
            if response.json()['code'] != 1 and response.json()['code'] != 1002:
                response.failure("Got wrong response")
                return
            accessToken = response.json()['data']['accessToken']
            userId = response.json()['data']['userId']
            phead = {'Access-Token': accessToken, 'userId': str(userId)}
            self.header = dict(self.header, **phead)


    # 用户执行task前调用
    def on_start(self):
        self.login()

    # 用户执行完task后调用
    def on_stop(self):
        pass

    @task(10)
    def game_page(self):
        with self.client.get("/game/api/v2/games",
                            headers=self.header, catch_response=True) as response:
            # 判断body里面的code是否正确
            if response.json()['code'] != 1:
                response.failure("Got wrong response")

    @task(1)
    def index_page(self):
        self.client.get("/")



class LoggedInUser(HttpUser):
    wait_time = between(5, 9)
    tasks = {GamestartUser: 1}

    @task
    def index_page(self):
        pass