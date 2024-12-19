
#include <WiFi.h>
#include "DFRobotDFPlayerMini.h"


TaskHandle_t Task1Handle = NULL;



#define PLAY_VALUE 110
#define FALSE 0
#define TRUE 1
DFRobotDFPlayerMini player;

int play1 = 0;
int play2 = 0;
int play_st = false;

void Task1(void* pvParameters) {
  while (true) {
    if (play_st == true) {
      static int play_tr = 0;
      if (play_tr == false) {
        player.play(play2);
        play_tr = true;
      } else if (play_tr == true) {
        player.play(play1);
        play_tr = false;
      }
    }
    vTaskDelay(2500 / portTICK_PERIOD_MS);  // FreeRTOS의 딜레이 함수 사용
  }
}



// Wi-Fi 네트워크 정보
const char* ssid = "11111112";
const char* password = "00000001";

WiFiServer server(8080);


void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600);
  delay(5000);
  Serial.println("booting UP");


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi Connected!");


  server.begin();

  Serial.println("Wifi Ok");

  Serial1.begin(9600, SERIAL_8N1, 16, 17); // TX = GPIO16, RX = GPIO17 for display


  xTaskCreate(
    Task1,        // 태스크 함수
    "Task1",      // 태스크 이름
    4096,         // 스택 크기 (바이트 단위)
    NULL,         // 태스크 함수에 전달할 매개변수
    1,            // 우선순위
    &Task1Handle  // 태스크 핸들러
  );


  Serial2.begin(9600, SERIAL_8N1, 32, 33);

  if (player.begin(Serial2)) {
    Serial.println("Audio OK");
  } else {
    Serial.println("Connecting to DFPlayer Mini failed!");
  }
  player.volume(2);
  player.stop();
}

void loop() {
  // put your main code here, to run repeatedly:

  String received;
  WiFiClient client = server.available();
  while (client.connected()) {
    if (client.available()) {
      received = client.readStringUntil('\n');
      client.stop();
      Serial.println(received);
    }

    if (received[0] == 'N') {
      if (received[3] == 'l') {  //비장애인 좌회전
        play1 = 2;
        play_st = true;
        Serial1.println("NoTl");
        
      } else if (received[3] == 'r') {  //비장애인 우회전
        play1 = 3;
        play_st = true;
        Serial1.println("NoTr");

      } else if (received[3] == 's') {  //비장애인 직진
        play1 = 1;
        play_st = true;
        Serial1.println("NoGs");

      } else if (received[3] == 'w') {  //비장애인 후진
        play1 = 4;
        play_st = true;
        Serial1.println("NoBw");
        
      }
    } else if (received[0] == 'D') {
      if (received[3] == 'l') {  //지체장애인 좌회전
        play2 = 6;
        play_st = true;
        Serial1.println("DiTl");
        
      } else if (received[3] == 'r') {  //지체장애인 우회전
        play2 = 7;
        play_st = true;
        Serial1.println("DiTr");

      } else if (received[3] == 's') {  //지체장애인 직진
        play2 = 5;
        play_st = true;
        Serial1.println("DiGs");
        
      } else if (received[3] == 'w') {  //지체장애인 후진
        play2 = 8;
        play_st = true;
        Serial1.println("DiBw");

      }
    } else if (received[0] == 'O') {
      play_st = false;
      Serial1.println("Of");
      player.stop();

    }
  }
}

//비장 직진 1
//비장 좌회전 2
//비장 우회전 3
//비장 뒤로 4
//지체 직진 5
//지체 좌회전 6
//지체 우회전 7
//지체 뒤로 8
