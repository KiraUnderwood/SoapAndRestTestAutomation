import pytest

from .SpellerRestAPI import SpellerRest, Options, Lang, Format, Errors
from .SpellerResponseParser import SpellerResponse


@pytest.fixture(scope="function")
def api():
    return SpellerRest()


'''
This test is to show the usage of Speller Rest and Response representation.
'''


def test_random_something(api):
    params1 = api.setparams(text='новгарод клей клEй ошипка', language=[Lang.ru.value, Lang.en.value],
                            option=[Options.IGNORE_CAPITALIZATION.value, Options.FIND_REPEAT_WORDS.value])
    response1 = api.checktext_post(params1)
    parsed_resp = SpellerResponse(response1)
    print(parsed_resp.body)
    assert parsed_resp.number_of_errors == 2
