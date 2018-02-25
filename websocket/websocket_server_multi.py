import hashlib
import base64
import socket
import struct
import socketserver
import json



class MyServer(socketserver.BaseRequestHandler):
    client_count = 0

    def handle(self):
        self.client_count += 1

        print("new connection, count: " + str(self.client_count))
        print(self.client_address)
        self.client_socket = self.request
        self.web_socket_handshake()

        while 1:
            print("send to client:" + str(self.client_socket.recv(2048)))

        client_socket.close()

    def web_socket_handshake(self):
        recv_data = self.client_socket.recv(2048).decode()
        print(recv_data)
        entities = recv_data.split("\r\n")
        sec_websocket_key = ""
        for item in entities:
            if item.startswith("Sec-WebSocket-Key"):
                sec_websocket_key = item.split(":")[1].strip()
                break

        if sec_websocket_key == "":
            return False

        sec_websocket_key = sec_websocket_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

        response_key = base64.b64encode(hashlib.sha1(bytes(sec_websocket_key, encoding="utf8")).digest())
        response_key_str = response_key.decode()
        print(response_key_str)
        response_key_entity = "Sec-WebSocket-Accept: " + response_key_str + "\r\n"
        self.client_socket.send(bytes("HTTP/1.1 101 Web Socket Protocol Handshake\r\n", encoding="utf8"))
        self.client_socket.send(bytes("Upgrade: websocket\r\n", encoding="utf8"))
        self.client_socket.send(bytes(response_key_entity, encoding="utf8"))
        self.client_socket.send(bytes("Connection: Upgrade\r\n\r\n", encoding="utf8"))
        print("send the hand shake data")


if __name__ == '__main__':
    # 传入 端口地址 和 我们新建的继承自socketserver模块下的BaseRequestHandler类  实例化对象
    sever = socketserver.ThreadingTCPServer(("127.0.0.1", 8124), MyServer)
    sever.serve_forever()  # 通过调用对象的serve_forever()方法来激活服务端
