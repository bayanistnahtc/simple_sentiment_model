import tornado.ioloop
import tornado.web
import tornado.websocket
import importlib
from os import listdir, chdir
from os.path import isfile, join, dirname
import sys


def python_files_in_directory(working_dir):
    files = [f for f in listdir(working_dir) if isfile(join(working_dir, f)) and f != sys.argv[0].split('/')[-1]]
    python_files = [f for f in files if f.endswith('.py')]
    python_filenames = [f.split('.py')[0] for f in python_files]
    return python_filenames


def load_modules(filenames, working_dir):
    modules = dict()
    for file in filenames:
        try:
            modules[file] = importlib.import_module(file, working_dir)
        except Exception as e:
            print(f"Could not load module {file} with exception: {str(e)}")
    print(f"Loaded modules: {list(modules.keys())}")
    return modules


class ScriptRunnerWebSocket(tornado.websocket.WebSocketHandler):

    modules = load_modules(python_files_in_directory(sys.argv[2]), sys.argv[2])

    def check_origin(self, origin):
        return True

    def data_received(self, chunk):
        pass

    def open(self):
        pass

    def on_message(self, message):
        try:
            self.write_message(ScriptRunnerWebSocket.modules[self.request.path[1:]].predict(message))
        except Exception as e:
            print(str(e))
            self.close(reason=f"an error occurred while executing script {self.request.path[1:]} with message: {str(e)}")

    def on_close(self):
        pass  # print("WebSocket closed")


def make_app(working_dir):
    files = python_files_in_directory(working_dir)
    handlers = [(r'/' + filename, ScriptRunnerWebSocket) for filename in files]

    return tornado.web.Application(handlers, debug=True)

if __name__ == "__main__":
    # dir_name = dirname(sys.argv[2])
    # chdir(dir_name)
    port = 8889#sys.argv[1]
    working_dir = sys.argv[2]
    #
    app = make_app(working_dir)
    print(f"Starting socket server on port {port}")
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port, address='127.0.0.1')
    tornado.ioloop.IOLoop.current().start()

