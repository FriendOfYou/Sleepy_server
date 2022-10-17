from app import app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

if __name__ == '__main__':
    # @app.route('/wqee/<int:id>')
    # def list_new(id):
    #     return "jieshoudao%s"%id
    # app.run(debug=True)
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    print('Server is running...')
    IOLoop.current().start()
