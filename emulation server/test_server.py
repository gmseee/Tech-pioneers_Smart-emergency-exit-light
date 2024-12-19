import tkinter as tk
from PIL import Image, ImageTk
import socket
import threading

# 서버 설정
SERVER_IP = "0.0.0.0"
SERVER_PORT = 10000
BUFFER_SIZE = 1024

def handle_client(client_socket, client_address, app):
    """클라이언트 요청을 처리하는 함수"""
    print(f"Connected by {client_address}")
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break

            message = data.decode('utf-8')
            app.handle_message(message)

            print(f"Received from {client_address}: {message}")

    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        print(f"Connection closed by {client_address}")
        client_socket.close()

def start_server(app):
    """서버를 별도의 스레드에서 실행"""
    def server_thread():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((SERVER_IP, SERVER_PORT))
        server_socket.listen(5)
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(
                    target=handle_client, 
                    args=(client_socket, client_address, app)
                )
                client_thread.daemon = True
                client_thread.start()
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()

    server_thread = threading.Thread(target=server_thread, daemon=True)
    server_thread.start()

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Image Update")

        # 이미지 파일 경로
        self.image_paths = [
            "nonDisable.png",
            "Disable.png",
            "arrow.png",
            "uturn.png",
            "Off.png"
        ]

        # 이미지 객체 리스트
        self.images = [None] * len(self.image_paths)

        # Label은 4개로 고정
        self.target_size = (100, 100)
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        self.labels = [tk.Label(self.frame) for _ in range(4)]

        for label in self.labels:
            label.pack(side=tk.LEFT, padx=5)

        self.load_images()

    def load_images(self):
        """이미지 파일을 로드하고 초기 Label에 설정"""
        for i, path in enumerate(self.image_paths):
            try:
                img = Image.open(path)
                img = img.resize(self.target_size, Image.LANCZOS)
                self.images[i] = img

                # Label 초기화는 최대 4개까지만
                if i < len(self.labels):
                    tk_img = ImageTk.PhotoImage(img)
                    self.labels[i].config(image=tk_img)
                    self.labels[i].image = tk_img
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                self.images[i] = None

    def change_images(self, row, imageNo, rotation_angle=0):
        """Label의 이미지를 변경"""
        if not (0 <= row < len(self.labels)) or not (0 <= imageNo < len(self.images)):
            print(f"Invalid row ({row}) or imageNo ({imageNo})")
            return

        if self.images[imageNo] is None:
            print(f"Image {imageNo} is not loaded. Cannot rotate or update.")
            return

        rotated_img = self.images[imageNo].rotate(rotation_angle, expand=True)
        tk_img = ImageTk.PhotoImage(rotated_img)
        self.labels[row].config(image=tk_img)
        self.labels[row].image = tk_img  # 참조 유지

    def handle_message(self, message):
        """수신된 메시지를 처리하여 이미지를 업데이트"""


        print(message)
        if message[0] == 'N':
            target_row = 1
        elif message[0] == 'D':
            target_row = 3
        elif message[0] == 'O':
            app.change_images(1, 4)
            app.change_images(3, 4)
            print("O")
            return
        else:
            target_row = -1        


        if target_row == -1:
            print("Invalid message type")
            return



        action = message[3]
        if action == 'l':
            self.change_images(target_row, 2, 180)
        elif action == 'r':
            self.change_images(target_row, 2, 0)
        elif action == 's':
            self.change_images(target_row, 2, 90)
        elif action == 'w':
            self.change_images(target_row, 3, 0)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)

    # 초기 이미지 설정
    app.change_images(0, 0)
    app.change_images(1, 4)
    app.change_images(2, 1)
    app.change_images(3, 4)

    start_server(app)  # 서버를 스레드로 실행
    root.mainloop()