#include "HUB75nano.h"
#include <SoftwareSerial.h>

// a bit broken rn, after the first letters leave the screen it goes haywire
String inputString = "";      // 시리얼 입력 문자열
bool stringComplete = false;  // 문자열 입력 완료 여부

// create an instance of the panel
Panel panel = {};

SoftwareSerial mySerial(A4, A5); // RX, TX

// 명령 파싱 함수
void parseCommand(String command) {
  command.trim();  // 앞뒤 공백 제거

  if (command == "NoTl") {
    panel.drawRect(0, 0, 31, 31, Colors::BLACK, true);
    panel.drawTriangle(0, 16, 15, 0, 15, 31, Colors::GREEN, true);
    panel.drawLine(0, 15, 15, 0, Colors::GREEN);
    panel.drawRect(16, 7, 31, 24, Colors::GREEN, true);

  } else if (command == "NoTr") {
    panel.drawRect(0, 0, 31, 31, Colors::BLACK, true);
    panel.drawTriangle(31, 16, 16, 0, 16, 31, Colors::GREEN, true);
    panel.drawLine(31, 15, 16, 0, Colors::GREEN);
    panel.drawRect(0, 7, 15, 24, Colors::GREEN, true);
  } else if (command == "NoGs") {
    panel.drawRect(0, 0, 31, 31, Colors::BLACK, true);
    panel.drawTriangle(15, 0, 0, 15, 31, 15, Colors::GREEN, true);
    panel.drawRect(7, 16, 24, 31, Colors::GREEN, true);
  } else if (command == "NoBw") {
    panel.drawRect(0, 0, 31, 31, Colors::BLACK, true);
    panel.drawRect(4, 4, 25, 25, Colors::GREEN, true);
    panel.drawRect(9, 9, 20, 20, Colors::BLACK, true);
    panel.drawRect(0, 16, 20, 31, Colors::BLACK, true);
    panel.drawTriangle(0, 15, 12, 15, 6, 25, Colors::GREEN, true);
  } else if (command == "DiTl") {
    panel.drawRect(32, 0, 63, 31, Colors::BLACK, true);
    panel.drawTriangle(0 + 32, 16, 15 + 32, 0, 15 + 32, 31, Colors::GREEN, true);
    panel.drawLine(0 + 32, 15, 15 + 32, 0, Colors::GREEN);
    panel.drawRect(16 + 32, 7, 31 + 32, 24, Colors::GREEN, true);
  } else if (command == "DiTr") {
    panel.drawRect(32, 0, 63, 31, Colors::BLACK, true);
    panel.drawTriangle(31 + 32, 16, 16 + 32, 0, 16 + 32, 31, Colors::GREEN, true);
    panel.drawLine(31 + 32, 15, 16 + 32, 0, Colors::GREEN);
    panel.drawRect(0 + 32, 7, 15 + 32, 24, Colors::GREEN, true);
  } else if (command == "DiGs") {
    panel.drawRect(32, 0, 63, 31, Colors::BLACK, true);
    panel.drawTriangle(15 + 32, 0, 0 + 32, 15, 31 + 31, 15, Colors::GREEN, true);
    panel.drawRect(7 + 32, 16, 24 + 32, 31, Colors::GREEN, true);
  } else if (command == "DiBw") {
    panel.drawRect(32, 0, 63, 31, Colors::BLACK, true);
    panel.drawRect(4 + 32, 4, 25 + 32, 25, Colors::GREEN, true);
    panel.drawRect(9 + 32, 9, 20 + 32, 20, Colors::BLACK, true);
    panel.drawRect(0 + 32, 16, 20 + 32, 31, Colors::BLACK, true);
    panel.drawTriangle(0 + 32, 15, 12 + 32, 15, 6 + 32, 25, Colors::GREEN, true);
  } else if (command == "Of") {
    panel.fillBuffer(Colors::BLACK);
  }
}

void setup() {
  mySerial.begin(9600);
  panel.fillBuffer(Colors::BLACK);  // background COLOR
}

void loop() {
  while (mySerial.available()) {
    char inChar = (char)mySerial.read();  // 문자 읽기
    if (inChar == '\n') {               // 줄바꿈 문자로 명령 종료 확인
      inputString.trim();               // 입력 문자열의 공백 제거
      parseCommand(inputString);        // 명령 파싱 함수 호출
      inputString = "";                 // 입력 문자열 초기화
    } else {
      inputString += inChar;  // 입력된 문자 추가
    }
  }
  panel.displayBuffer();  // makes the buffer visible and the leds all blinky blinky
}