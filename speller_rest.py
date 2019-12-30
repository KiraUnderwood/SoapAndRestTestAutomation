import sys
from http import HTTPStatus

import pytest
import requests

'''
This module is basic tests for API by Yandex Speller
https://yandex.ru/dev/speller/doc/dg/concepts/api-overview-docpage/
No modularity or OOP are involved.
'''

very_long_row_in_cyrillics = 'сегодня ' * 1249 + 'сигодня'  # 10000 sym / 8 symb = 1250 + the last word with typo.
# With post is expected


# to be checked, with get the request is supposed to return 414 since over 10 KB

# resource 1: api to check one test paragraph, resourse2: api to check collection of test paragraphs
@pytest.fixture(scope="function")  # standard of pytest to do setup/teardown and preparing test data within the fixtures
def check_one_paragraph():
    return 'https://speller.yandex.net/services/spellservice.json/checkText'


@pytest.fixture(scope="function")
def check_multiple_paragraphs():
    return 'https://speller.yandex.net/services/spellservice.json/checkTexts'


class TestSpellerCases:

    def test_declared_text_body_limits_get_1(self, check_one_paragraph):
        params = {
            'text': very_long_row_in_cyrillics,
            'lang': 'ru',
        }
        string_size = sys.getsizeof(very_long_row_in_cyrillics)
        response_code = requests.get(check_one_paragraph, params=params).status_code
        assert string_size > 10240 and response_code == HTTPStatus.REQUEST_URI_TOO_LONG.value,\
            f"The string size is {string_size} was expected to be over 10240 and response code is {response_code} was expecting {HTTPStatus.REQUEST_URI_TOO_LONG.value} "

    """
    The next tests assert the expected error code reported in the json response as per https://yandex.ru/dev/speller/doc/dg/reference/error-codes-docpage/
    """
    def test_declared_text_body_limits_post_2(self, check_one_paragraph):
        params = {
            'text': very_long_row_in_cyrillics,
            # 'text': stroka.encode('utf-8'),
            'lang': 'ru',
            'options': 8,
        }
        response = requests.post(check_one_paragraph, data=params).json()
        assert response[0]["code"] == 1

    def test_declared_text_body_limits_post_3(self, check_multiple_paragraphs):
        params = {
            'text': very_long_row_in_cyrillics,
            # 'text': stroka.encode('utf-8'),
            'lang': 'ru',
            'options': 8,
        }
        response = requests.post(check_multiple_paragraphs, data=params).json()
        assert response[0]["code"] == 1

    def test_non_latin_symbol_4(self, check_one_paragraph):
        params = {
            'text': 'Spañish',
            'lang': 'en,ru',
            'options': 8
        }
        response = requests.post(check_one_paragraph, data=params).json()
        assert response[0]["code"] == 1

    def test_incorrect_number_of_opt_over_the_top_5(self, check_one_paragraph):
        params = {
            'text': 'новгарод клей клEй ошипка авп17х4534 http://htmlbook.ru/content/formatirovanie-teksta',
            'lang': 'en,ru',
            'options': 600
        }
        response = requests.post(check_one_paragraph, data=params).json()
        # print(response)
        assert response[0]["code"] == 1
        assert len(response) == 2

    def test_incorrect_number_of_opt_over_the_top_6(self, check_one_paragraph):
        params = {
            'text': 'новгарод клий',
            'lang': 'en,ru',
            'options': 600
        }
        response = requests.post(check_one_paragraph, data=params).json()
        assert len(response) == 2

    def test_enable_all_options_7(self, check_one_paragraph):
        params = {
            'text': 'новгарод клей клEй ошипка авп17х4534 http://htmlbook.ru/content/formatirovanie-teksta',
            'lang': 'en,ru,uk',
            'options': 526
        }
        response = requests.post(check_one_paragraph, data=params).json()
        print(response)
        assert len(response) == 3
