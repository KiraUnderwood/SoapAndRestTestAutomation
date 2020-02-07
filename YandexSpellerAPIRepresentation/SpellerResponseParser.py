import requests


class SpellerResponse:
    class Error:
        def __init__(self, body, num):
            if isinstance(body, list):
                if isinstance(body[num], dict):
                    self.code = body[num]["code"]
                    self.pos = body[num]["pos"]
                    self.row = body[num]["row"]
                    self.col = body[num]["len"]
                    self.len = body[num]["word"]
                    self.s = body[num]["s"]

    def __init__(self, response):
        if isinstance(response, requests.Response):
            self.stat_code = response.status_code
            self.number_of_errors = len(response.json())
            self.body = response.json()
            self.error = None

    def parse_response_element(self, number):
        return self.Error(self.body, number)
