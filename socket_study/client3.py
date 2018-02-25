import socket
import time

def client(id):
    sk = socket.socket()
    sk.connect(("127.0.0.1", 8888))  # 主动初始化与服务器端的连接
    while True:
        sk.sendall(bytes(str(id), encoding="utf8"))
        send_data = input("输入发送内容:")
        sk.sendall(bytes(send_data, encoding="utf8"))
        if send_data == "byebye":
            break
        accept_data = str(sk.recv(1024), encoding="utf8")
        print("".join(("接收内容：", accept_data)))
    sk.close()

client(1)
