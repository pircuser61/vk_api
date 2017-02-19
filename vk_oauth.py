from tornado import web
from tornado import httpclient


class OAuthVk(web.RequestHandler):
    """Авторизация в ВК
       on_success(HTTPResponse response) - если не возникло ошибок,
            response - ответ сервера vk
       on_error(error) - в случае возникновеня ошибок
            error - строка с описанием, или exception
    """

    _ACCESS_TOKEN_URL = 'https://oauth.vk1.com/access_token'
    _AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    _APP_ID_ = ''   # id - приложения (в настройках vk)
    _REDIRECT_URL_ = ''  # www.yousite.com/oauth
    _CLIENT_SECRET_ = ''  # защищенный ключ приложения (в настройках vk)

    def __init__(self, *args):
        super().__init__(*args)

        params = {'client_id': self._APP_ID_,
                  'redirect_uri': self._REDIRECT_URL_,
                  # 'scope': str(2),
                  }
        token_params = {'client_id': self._APP_ID_,
                        'client_secret': self._CLIENT_SECRET_,
                        'redirect_uri': self._REDIRECT_URL_,
                        # 'code': '',
                        }
        self.token_url = self._ACCESS_TOKEN_URL + '?' + '&'.join([k + '=' + v for k, v in token_params.items()])
        self.code_url = self._AUTHORIZE_URL + '?' + '&'.join([k + '=' + v for k, v in params.items()])

    async def get(self):
        if self.get_argument('code', default=None):
            vk_code = self.get_argument('code', default=None)
            if vk_code:
                a_http = httpclient.AsyncHTTPClient()
                try:
                    response = await a_http.fetch(self.token_url+'&code='+vk_code)
                except Exception as e:  # в описаниии не прописаны все exception которые оно может выбросить
                                        # как вариант сервер vk недоступен
                    self.on_error(e)    # возвращаю exception параметром, вместо raise
                else:
                    self.on_success(response)
            else:
                self.on_error("code is None")
        else:
            self.redirect(self.code_url)

    def on_success(self, response):
        """вызывается при удачной авторизации"""
        raise NotImplementedError("on_success")

    def on_error(self, error):
        """при ошибке"""
        raise NotImplementedError("on_error")
