import cherrypy
import json

import io
import jsonpickle
import urllib.parse
from algorithms.algorithm_v2 import Algorithm_v2
from algorithms.selectors.black_list_selector import BlackListSelector
from algorithms.selectors.simple_selector import SimpleSelector

WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_PORT = 9876
WEBHOOK_LISTEN = '127.0.0.1'

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/"


class WebhookServer(object):
    def __init__(self):
        self.markup_list = list()
        self.algorithm = None

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, **kwargs):
        action = kwargs['action']
        if action == "reset":
            self.markup_list = list()
            print("Reset")
            return 'Markup list is empty'
        if action == "add":
            text = str(kwargs['markup']).replace("\'", "\"")
            markup = jsonpickle.decode(text)
            markup.file = str(len(self.markup_list)) + ".html"
            markup.type = "HTMLTree"
            with open(str(len(self.markup_list)) + ".html", "w") as file:
                file.write(kwargs['raw_page'])
            self.markup_list.append(markup)
            print("Add markup")
            print(str(markup))
            return "Markup added"
        if action == "learn":
            selector = SimpleSelector()
            self.algorithm = Algorithm_v2("", selector=selector)
            self.algorithm.learn(self.markup_list)
            print("Learn is done")
            return "Learn is done"
        if action == "parse":
            parser_result = self.algorithm.parse(kwargs['raw_page'])
            print(str(parser_result))
            return json.loads(str(parser_result))


cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.SO_REUSEADDR': 1,
    'server.ssl_module': 'builtin'
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
