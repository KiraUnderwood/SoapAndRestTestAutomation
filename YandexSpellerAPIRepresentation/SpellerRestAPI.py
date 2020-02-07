from enum import Enum

import pytest
import requests


class Options(Enum):
    IGNORE_DIGITS = 2
    IGNORE_URLS = 4
    FIND_REPEAT_WORDS = 8
    IGNORE_CAPITALIZATION = 512


class Lang(Enum):
    ru = "ru"
    uk = "uk"
    en = "en"


class Format(Enum):
    plain = 'plain'
    html = 'html'


class Errors(Enum):
    ERROR_UNKNOWN_WORD = 1
    ERROR_REPEAT_WORD = 2
    ERROR_CAPITALIZATION = 3
    ERROR_TOO_MANY_ERRORS = 4


class SpellerRest:
    checkText = 'https://speller.yandex.net/services/spellservice.json/checkText'
    checkTexts = 'https://speller.yandex.net/services/spellservice.json/checkTexts'
    text = None
    lang = str(Lang.ru.value) + ',' + str(Lang.en.value)
    options = None
    format = str(Format.plain)

    def __init__(self):
        self.checkText = 'https://speller.yandex.net/services/spellservice.json/checkText'
        self.checkTexts = 'https://speller.yandex.net/services/spellservice.json/checkTexts'
        self.text = None
        self.lang = str(Lang.ru.value) + ',' + str(Lang.en.value)
        self.options = None
        self.format = str(Format.plain)

    def setparams(self, text=None, language=[], option=[], formatting=None):
        text = '' if text is None else str(text)

        if not language:
            lang = self.lang
        else:
            lang = ''
            for lan in language:
                lang += lan + ','

        if not option:
            opt = self.options
        else:
            opt = 0
            for op in option:
                opt += int(op)

        if formatting is None:
            formatting == self.format
        else:
            formatting = str(formatting)

        return {'text': text, 'lang': lang, 'options': opt, 'format': formatting}

    def checktext_post(self, params):
        return requests.post(self.checkText, data=params)

    def checktest_get(self, params):
        return requests.get(self.checkText, params=params)

    def checktexts_post(self, params):
        return requests.post(self.checkTexts, data=params)

    def checktests_get(self, params):
        return requests.get(self.checkTexts, params=params)
