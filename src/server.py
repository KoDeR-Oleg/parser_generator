import cherrypy
import json
import jsonpickle
import urllib.parse
from algorithms.algorithm_v2 import Algorithm_v2
from algorithms.selectors.black_list_selector import BlackListSelector

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
    def index(self):
        print(str(cherrypy.request.headers))
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':

            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            obj = json.loads(json_string)

            if obj['action'] == "reset":
                self.markup_list = list()
                print("Reset")
            elif obj['action'] == "learn":
                selector = BlackListSelector()
                self.algorithm = Algorithm_v2("../golden/google/", selector=selector)
                self.algorithm.learn(self.markup_list)
                print("Learn is done")
            elif obj['action'] == "add":
                text = str(obj['markup']).replace("\'", "\"")
                markup = jsonpickle.decode(text)
                self.markup_list.append(markup)
                print("Add markup")
            elif obj['action'] == "parse":
                parser_result = self.algorithm.parse(obj['raw_page'])
                print(str(parser_result))

            return ''
        else:
            raise cherrypy.HTTPError(403)


cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.SO_REUSEADDR': 1,
    'server.ssl_module': 'builtin'
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
