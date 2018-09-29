# WebFrame.py

# coding=utf-8

from socket import *
from setting import *
import time
from urls import *
from views import *


class Application(object):
    def __init__(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(frame_addr)

    def start(self):
        self.sockfd.listen(5)
        while True:
            connfd, addr = self.sockfd.accept()

            # 接收请求方法
            method = connfd.recv(128).decode()
            # 接收请求内容
            path_info = connfd.recv(128).decode()
            print(method, path_info)

            if method == 'GET':
                if path_info == '/' or path_info[-5:] == '.html':
                    status, response_body = self.get_html(path_info)
                else:
                    status, response_body = self.get_data(path_info)

                # 将结果给HttpServer
                connfd.send(status.encode())
                time.sleep(0.1)
                connfd.send(response_body.encode())

            elif method == 'POST':
                pass

    def get_html(self, path_info):
        if path_info == '/':
            get_file = STATIC_DIR + '/index.html'
        else:
            get_file = STATIC_DIR + path_info

        try:
            f = open(get_file)
        except IOError:
            response = ('404', '===Sorry, not found the page===')
        else:
            response = ('200', f.read())
        finally:
            return response

    def get_data(self, path_info):
        for url, handler in urls:
            if path_info == url:
                response_body = handler()
                return '200', response_body
        return '404', "Sorry, not found the data"


if __name__ == "__main__":
    app = Application()
    app.start()  # 启动框架，等待request










