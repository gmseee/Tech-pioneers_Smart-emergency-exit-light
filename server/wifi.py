import socket
import time
from dataclasses import dataclass
import threading

@dataclass
class Display:
    IP: str
    PORT: int
    NODE: int
    arrow: dict
    No: int

def send_data_async(display: Display, message1: str, message2: str):
    """
    비동기 데이터 전송을 위해 스레드에서 실행될 함수
    """
    def send_message(ip, port, message):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            client_socket.connect((ip, port))
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent: {message} to {ip}:{port}")
            client_socket.close()
        except Exception as e:
            print(f"Error sending message: {e}")

    # 스레드 생성 및 시작
    thread1 = threading.Thread(target=send_message, args=(display.IP, display.PORT, message1))
    thread2 = threading.Thread(target=send_message, args=(display.IP, display.PORT, message2))

    thread1.start()
    thread2.start()

    # 스레드가 종료될 때까지 대기
    thread1.join()
    thread2.join()

def send_data(ESP32: Display, message1: str, message2: str):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client_socket.connect((ESP32.IP, ESP32.PORT))
    client_socket.sendall(message1.encode('utf-8'))
    client_socket.close()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client_socket.connect((ESP32.IP, ESP32.PORT))
    client_socket.sendall(message2.encode('utf-8'))
    client_socket.close()

def main():
    # 소켓 생성

    while True:
        message = input()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client_socket.connect(("192.168.0.86", 8080))
        # print(f"Connected to ESP32 server at {ESP32_IP}:{ESP32_PORT}")
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")
        client_socket.close()
           

if __name__ == "__main__":
    main()