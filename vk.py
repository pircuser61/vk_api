import tornado.httpclient as httpclient

_METHOD_URL_ = 'https://api.vk.com/method/'
_V = '5.62'  # не добавлено


class Api:
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
        self.token = token
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

    async def get(self, user_id=None, order=None, count=None, fields=('nickname', 'sex', 'domain',)):
        params_list = []
        if user_id:
            params_list.append('user_id=' + user_id)
        if order:
            params_list.append('order=' + order)
        if count:
            params_list.append('count=' + str(count))
        if fields:
            params_list.append('fields=' + ';'.join(fields))
        params = '&'.join(params_list)
        print(params)
        print('\r\n')
        url = '{}get?{}&access_token={}&v={}'\
            .format(self.url, params, self.token, _V)
        print(url)
        http = httpclient.AsyncHTTPClient()
        return await http.fetch(url)


class Photos:
    def __init__(self, token):
        self.url = _METHOD_URL_ + 'photos.'
        self.token = token

    async def get_all(self):  # параметры лень
        pass
