import socket
import threading

# 서버 설정
SERVER_IP = "0.0.0.0"  # 모든 네트워크 인터페이스에서 수신
SERVER_PORT = 8080
BUFFER_SIZE = 1024  # 수신 버퍼 크기

def handle_client(client_socket, client_address):
    """
    클라이언트의 연결을 처리하는 함수
    """
    print(f"Connected by {client_address}")
    try:
        while True:
            # 클라이언트로부터 데이터 수신
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break  # 클라이언트가 연결을 종료함

            message = data.decode('utf-8')
            print(f"Received from {client_address}: {message}")

            # 클라이언트에게 응답 (필요하면 아래 코드를 수정)
            response = f"Server received: {message}"
            client_socket.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        print(f"Connection closed by {client_address}")
        client_socket.close()

def start_server():
    """
    TCP 서버를 시작하는 함수
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)  # 최대 5개의 연결 대기
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            # 클라이언트 연결 수락
            client_socket, client_address = server_socket.accept()
            # 새로운 스레드에서 클라이언트 처리
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
