from tornado import web
from tornado import httpclient


class OAuthVk(web.RequestHandler):
    """Авторизация в ВК

    """
    _ACCESS_TOKEN_URL = 'https://oauth.vk.com/access_token'
    _AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    _APP_ID_ = ''
    _REDIRECT_URL_ = ''
    _CLIENT_SECRET_ = ''

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
                response = await a_http.fetch(self.token_url+'&code='+vk_code)
                self.on_success(response)

            else:
                self.on_error()
        else:
            self.redirect(self.code_url)

    def on_success(self, response):
        """вызывается при удачной авторизации"""
        raise NotImplementedError("on_success")

    def on_error(self):
        """при ошибке"""
        raise NotImplementedError("on_error")
