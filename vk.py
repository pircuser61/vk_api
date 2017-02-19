import os

import tornado.web as web
import tornado.ioloop as ioloop
import tornado.httpclient as httpclient
import tornado.escape as escape



_METHOD_URL_ = 'https://api.vk.com/method/'
_V = '5.62'  #не добавлено

class Api():
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


    def __init__(self, token):
        if not token:
            raise ValueError("Empty token")
        self.token = token#str(token)[2:-1]
        self._friends = None

    @property
    def friends(self):
        if not self._friends:
            self._friends = Friends(self.token)
        return self._friends


class Friends:
    def __init__(self, token):
        self.url = _METHOD_URL_ + 'friends.'
        self.token = token

    async def get(self, user_id=None, order='random', count=10, fields=('nickname', 'sex', 'domain',)):

        if user_id:
            url = '{}get?user_id={}&order={}&count={}&fields={}&access_token={}'.\
                format(self.url, user_id, order, count, ';'.join(fields),self.token)
        else:
            url = '{}get?order={}&count={}&fields={}&access_token={}'. \
                format(self.url, order, count, ';'.join(fields), self.token)
        print('================\r\n\r\n{}\r\n'.format(url))
        http = httpclient.AsyncHTTPClient()
        return await http.fetch(url)




