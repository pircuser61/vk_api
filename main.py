import os

import tornado.web as web
import tornado.ioloop as ioloop
import tornado.escape as escape

import vk_oauth
import vk

path = os.path.dirname(__file__)
html = {'main': os.path.join(path, 'html', 'main.html'),
        'result': os.path.join(path, 'html', 'result.html'),
        'error': os.path.join(path, 'html', 'error.html'),
        }


class StartPage(web.RequestHandler):

    def get(self):
        self.render(html['main'])


class OAuthVk(vk_oauth.OAuthVk):

    _APP_ID_ = '5799473'
    _CLIENT_SECRET_ = 'ePxhl0tDNmV1t5EuveeJ'
    _REDIRECT_URL_ = 'http://localhost:8888/oauth_vk'

    def on_success(self, response):
        """вызывается при удачной авторизации"""
        # raise NotImplementedError("on_success")
        try:
            keys = escape.json_decode(response.body)
        except Exception as e:
            self.render(html['error'], error=e)
        else:
            self.set_secure_cookie('token', keys['access_token'])
            self.set_cookie('user_id', str(keys['user_id']))
            self.render(html['result'], data=keys)

    def on_error(self):
        """при ошибке"""
        # raise NotImplementedError("on_error")
        self.render(html['error'])

class SomeCmd(web.RequestHandler):
    async def get(self):
        cmd = self.get_argument('cmd', default=None)
        if cmd == 'friends':
            token = self.get_secure_cookie('token')
            api = vk.Api(token.decode('utf-8'))
            response = await api.friends.get()
            self.render(html['result'], data=response.body)

# main loop
if __name__ == '__main__':
    app = web.Application(
        [('/', StartPage),
         ('/oauth_vk', OAuthVk),
         ('/api',SomeCmd),
         ],
        debug=True,
        cookie_secret='54309673028670355275932573'
    )
    app.listen(8888)
    ioloop.IOLoop.current().start()
