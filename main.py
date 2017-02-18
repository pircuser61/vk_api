import os

import tornado.web as web
import tornado.ioloop as ioloop
import tornado.httpclient as httpclient
import tornado.escape as escape

import tornado.auth

path = os.path.dirname(__file__)
html = {'main': os.path.join(path, 'html', 'main.html'),
        'result': os.path.join(path, 'html', 'result.html'),
        'error': os.path.join(path, 'html', 'error.html'),
        }


class StartPage(web.RequestHandler):

    def get(self):
        if self.get_secure_cookie('code'):
            vk_auth = False  # True
        else:
            vk_auth = False
        self.render(html['main'], vk_auth=vk_auth)

    def post(self):
        pass


class OAuthVk(web.RequestHandler):

    _ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
    _AUTHORIZE_URL = 'https://oauth.vk.com/authorize'

    def __init__(self, *args):
        super().__init__(*args)

        params = {'client_id': '5799473',
                  'redirect_uri': 'http://localhost:8888/oauth_vk',
                  # 'scope': str(2),
                  }
        token_params = {'client_id': '5799473',
                        'client_secret': 'ePxhl0tDNmV1t5EuveeJ',
                        'redirect_uri': 'http://localhost:8888/oauth_vk',
                        # 'code': '',
                        }
        self.token_url = self._ACCESS_TOKEN_URL + '?' + '&'.join([k + '=' + v for k, v in token_params.items()])
        self.code_url = self._AUTHORIZE_URL + '?' + '&'.join([k + '=' + v for k, v in params.items()])

    async def get(self):
        if self.get_argument('code', default=None):
            vk_code = self.get_argument('code', default=None)

            if vk_code:
                a_http = httpclient.AsyncHTTPClient()
                print(self.token_url)
                print('================================================')
                response = await a_http.fetch(self.token_url+'&code='+vk_code)
                # self.render(response.body)
                print(escape.json_decode(response.body))
                # self.set_secure_cookie('code', vk_code)

            else:
                self.redirect(html['error'])
        else:
            self.redirect(self.code_url)

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


# main loop
if __name__ == '__main__':
    app = web.Application(
        [('/', StartPage),
         ('/oauth_vk', OAuthVk),
         ],
        debug=True,
        cookie_secret='54309673028670355275932573'
    )
    app.listen(8888)
    ioloop.IOLoop.current().start()
