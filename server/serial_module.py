import serial
import threading
import main



# 데이터 수신 인터럽트 스레드
def serial_interrupt(ser):
    while True:
        if ser.in_waiting > 0:  # 버퍼에 데이터가 있을 경우
            try:
                received_data = ser.readline().decode().strip()
                if received_data:  # 데이터가 비어 있지 않다면
                    main.handle_received_data(received_data)
            except Exception as e:
                print(f"Error in serial interrupt: {e}")
                break

def main_private():
    # 시리얼 포트와 속도 설정
    ser = serial.Serial(
        port='/dev/ttyAMA0',  # Raspberry Pi의 기본 시리얼 포트
        baudrate=9600,        # 통신 속도 (보드레이트)
        timeout=0             # 타임아웃 없음 (지속 수신 대기)
    )

    # 시리얼 포트가 열려 있는지 확인
    if ser.isOpen():
        print("Serial port is open and listening...")

    # 인터럽트처럼 동작하는 스레드 시작
    interrupt_thread = threading.Thread(target=serial_interrupt, args=(ser,))
    interrupt_thread.daemon = True  # 메인 종료 시 스레드도 종료
    interrupt_thread.start()

    try:
        # 메인 루프는 아무것도 하지 않고 대기만 함
        while True:
            pass
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        ser.close()
        print("Serial port closed")

if __name__ == "__main__":
    main_private()