import path_find
import wifi
from dataclasses import dataclass
import threading
import serial
import serial_module

end_node = 0

threads = []

fire_state = [False, False, False, False, False,
                False, False, False, False, False,
                False, False, False, False, False,
                False, False, False, False, False,
                False, False, False, False, False]

# Display 인스턴스를 생성
display_objects = [
    # wifi.Display("192.168.222.48", 10000, 9, {10: "Gs", 4: "Tr"}, 2),
    # wifi.Display("192.168.0.86", 8080, 21, {3 : "Tr"}, 2),
    # wifi.Display("192.168.0.86", 8080, 22, {3: "Tl", 13 : "Tr"}, 2),
    # wifi.Display("192.168.0.86", 8080, 10, {4: "Tl", 9: "Gs", 6: "Bw"}, 2), #10 - 1
    # wifi.Display("192.168.0.86", 8080, 10, {4: "Bw", 9: "Bw", 6: "Gs"}, 2), #10 - 2
    # wifi.Display("192.168.222.48", 10000, 4, {9: "Tl", 10: "Tr", 14: "Bw"}, 2),
    # wifi.Display("192.168.222.48", 10000, 3, {13: "Bw", 14: "Tl", 11: "Tr"}, 2),
    # wifi.Display("192.168.0.86", 8080, 23, {4: "Tr"}, 2),
    wifi.Display("192.168.153.134", 8080, 11, {3: "Tl", 12: "Gs"}, 2),
    # wifi.Display("192.168.0.86", 8080, 12, {3: "Tr", 8: "Bw", 11: "Gs"}, 2), #12 - 1
    # wifi.Display("192.168.0.86", 8080, 12, {3: "Bw", 8: "Gs", 11: "Bw"}, 2),#12 - 2
    # wifi.Display("192.168.0.86", 8080, 24, {4: "Tl", 14: "Tr"}, 2),
    # wifi.Display("192.168.0.86", 8080, 15, {2: "Gs", 5: "Tr", 6:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 16, {1: "Tr", 0:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 17, {13: "Tr", 1:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 19, {14: "Tr", 2:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 18, {2: "Tr"}, 2),
    # wifi.Display("192.168.0.86", 8080, 6, {5: "Gs", 15: "Tr", 2:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 7, {8: "Gs", 0: "Tr", 1:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 8, {7: "Gs", 1: "Tr", 0:"Tl"}, 2),
    # wifi.Display("192.168.0.86", 8080, 20, {4: "Gs", 9: "Tr", 10:"Tl"}, 2)
]

Display_1 = wifi.Display("192.168.0.86", 8080, 1, {7: "Gs", 1: "Tr", 0:"Tl"}, 2)
Display_2 = wifi.Display("192.168.0.86", 8080, 2, {7: "Gs", 1: "Tr", 0:"Tl"}, 2)
Display_3 = wifi.Display("192.168.0.86", 8080, 5, {6: "Gs", 2: "Tr", 15:"Tl"}, 2)



No_graph = path_find.DynamicGraph.array_to_adjacency_list(path_find.array_graph)
Di_graph = path_find.DynamicGraph.array_to_adjacency_list(path_find.array_graph)
Di_graph.remove_node(14)



def data_process():
    global No_graph
    global Di_graph
    for display in display_objects:
        No_shortest_distance, No_path = No_graph.dijkstra(display.NODE, end_node)
        Di_shortest_distance, Di_path = Di_graph.dijkstra(display.NODE, end_node)

        #print(Di_path)
        #print(Di_path[display20.No])
        #print(No_path[display20.No])
        # wifi.send_data(display,"Di" + display.arrow[Di_path[display.No]], "No" + display.arrow[No_path[display.No]])
        print(Di_path[display.No])
        thread = threading.Thread(
                target=wifi.send_data_async,
                args=(display,
                    "Di" + display.arrow[Di_path[display.No]],
                    "No" + display.arrow[No_path[display.No]])
            )
        threads.append(thread)
        thread.start()

    No_shortest_distance, No_path = No_graph.dijkstra(Display_1.NODE, end_node)
    Di_shortest_distance, Di_path = Di_graph.dijkstra(Display_1.NODE, end_node)
    Disp_1_No = ""
    Disp_1_Di = ""
    if No_path[2] == 0:
        if(No_path[1] == 5):
            Disp_1_No = "Bw"
        elif(No_path[1] == 2):
            Disp_1_No = "Gs"
    elif No_path[2] == 13:
        Disp_1_No = "Bw"
    elif No_path[2] == 8:
        Disp_1_No = "Tl"
    elif No_path[2] == 7:
        Disp_1_No = "Tr"
        
    if Di_path[2] == 0:
        if(Di_path[1] == 5):
            Disp_1_Di = "Bw"
        elif(Di_path[1] == 2):
            Disp_1_Di = "Gs"
    elif Di_path[2] == 13:
        Disp_1_Di = "Bw"
    elif Di_path[2] == 8:
        Disp_1_Di = "Tl"
    elif Di_path[2] == 7:
        Disp_1_Di = "Tr"

    thread = threading.Thread(
            target=wifi.send_data_async,
            args=(Display_1,
                "Di" + Disp_1_Di,
                "No" + Disp_1_No)
    )
    # threads.append(thread)
    # thread.start()


    No_shortest_distance, No_path = No_graph.dijkstra(Display_1.NODE, end_node)
    Di_shortest_distance, Di_path = Di_graph.dijkstra(Display_1.NODE, end_node)
    Disp_2_No = ""
    Disp_2_Di = ""
    if Di_path[1] == 0:
        Disp_2_Di = "Bw"
    elif Di_path[2] == 0:
        Disp_2_Di = "Tl"
    elif Di_path[2] == 6:
        Disp_2_Di = "Tr"

    if No_path[1] == 0:
        Disp_2_No = "Bw"
    elif No_path[2] == 0:
        Disp_2_No = "Tl"
    elif No_path[2] == 6:
        Disp_2_No = "Tr"

    thread = threading.Thread(
            target=wifi.send_data_async,
            args=(Display_2,
                "Di" + Disp_2_Di,
                "No" + Disp_2_No)
    )
    # threads.append(thread)
    # thread.start()

    No_shortest_distance, No_path = No_graph.dijkstra(Display_3.NODE, end_node)
    Di_shortest_distance, Di_path = Di_graph.dijkstra(Display_3.NODE, end_node)
    Disp_3_No = ""
    Disp_3_Di = ""
    if Di_path[1] == 0:
        Disp_3_Di = "Gs"
    elif Di_path[1] == 1:
        Disp_3_Di = "Bw"

    if No_path[1] == 0:
        Disp_3_No = "Gs"
    elif No_path[1] == 1:
        Disp_3_No = "Bw"

    thread = threading.Thread(
            target=wifi.send_data_async,
            args=(Display_3,
                "Di" + Disp_3_Di,
                "No" + Disp_3_No)
    )
    # threads.append(thread)
    # thread.start()

    for thread in threads:
        thread.join()

# 특정 함수를 실행할 사용자 정의 함수
def handle_received_data(data):
    global No_graph
    global Di_graph
    print(f"Interrupt triggered! Received data: {data}")

    if(data[0] == 'S'):
        fire_state[int(data[1:])] = True
    elif(data[0] == 'R'):
        fire_state[int(data[1:])] = False
    
    if any(fire_state):
        No_graph = path_find.DynamicGraph.array_to_adjacency_list(path_find.array_graph)
        Di_graph = path_find.DynamicGraph.array_to_adjacency_list(path_find.array_graph)
        Di_graph.remove_node(14)

        for i, j in enumerate(fire_state):  # 인덱스와 값을 함께 가져옴
            if j == True:  # j가 True일 경우
                Di_graph.remove_node(i)  # 인덱스를 노드로 제거
                No_graph.remove_node(i)

        data_process()
    
    else:
        for display in display_objects:
            thread = threading.Thread(
                    target=wifi.send_data_async,
                    args=(display,
                        "Of",
                        "Of")
                )
            threads.append(thread)
            thread.start()





def main():
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
    interrupt_thread = threading.Thread(target=serial_module.serial_interrupt, args=(ser,))
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
    main()
