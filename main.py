import os

import tornado.web as web
import tornado.ioloop as ioloop
import tornado.httpclient as httpclient
import tornado.escape as escape

import vk_oauth

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
        self.render(html['result'],data=escape.json_decode(response.body))

    def on_error(self):
        """при ошибке"""
        # raise NotImplementedError("on_error")
        self.render(html['error'])



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
