import socket
import base64
import time


def send_encoded_data(server, port, data):
    syn = b'YOINK'
    data = base64.b64encode(base64.b64encode(base64.b64encode(data)))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, port))
        s.sendall(syn)
        time.sleep(.1)
        s.sendall(data)


if __name__ == '__main__':
    send_encoded_data('localhost', 8080, b'This is a test message')