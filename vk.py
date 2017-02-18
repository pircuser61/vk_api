import os

import tornado.web as web
import tornado.ioloop as ioloop
import tornado.httpclient as httpclient
import tornado.escape as escape






class VK_api():
    """https: // api.vk.com / method / METHOD_NAME?PARAMETERS & access_token = ACCESS_TOKEN & v = V

    METHOD_NAME (обязательно) — название метода API, к которому Вы хотите
        обратиться. Полный список методов доступен на этой странице.
    PARAMETERS (опционально) — входные параметры соответствующего метода API,
        последовательность пар name=value, разделенных амперсандом. Список параметров указан
        на странице с описанием метода.
    ACCESS_TOKEN (опционально) — ключ доступа. Подробнее о получении токена
        Вы можете узнать в этом руководстве.
    V (опционально) — используемая версия API. Использование этого параметра применяет
        некоторые изменения в формате ответа различных методов.
        На текущий момент актуальная версия API — 5.62. Этот параметр следует
        передавать со всеми запросами.
        Для сохранения совместимости в существующих приложениях по умолчанию используется версия 3.0.
    """

    _BASE_URL_ = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.token = 'access_token=' + token
        self._friends = None

    def friends(self, user_id):
        if not self._friends:
            self._friens=Friends(token)
        return self._friends

class Friends:
    def __init__(self, token):
        self.url = VK_api._BASE_URL_ + 'friends.'

    def get(self, user_id, order = 'random', count=10, fields=('nickname','sex','domain',)):
        url = self._BASE_URL_
        http = httpclient.HTTPClient()
        response = http.fetch()
    def get



