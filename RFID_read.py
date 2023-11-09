"""
sudo pip3 install spidev
sudo pip3 install mfrc522

"""
import telepot
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
data_id = ['관리자 코드'] #데이터 초기화
reader = SimpleMFRC522() #RFID 객체 생성

def telbot_get_chatid():
    # 봇 토큰을 사용하여 봇을 초기화
    bot_token = '6873483008:AAEh14eISGJdMR_zRP861w_FMrkrYUcd1t8'
    bot = telepot.Bot(bot_token)

    # 대기 시간 동안 메시지를 체크
    start_time = time.time()
    wait_time = 30
    while time.time() - start_time < wait_time:
        try:
            # 메시지 수신
            response = bot.getUpdates()
            if response:
                # 가장 최근 메시지의 채팅 ID 반환
                chat_id = response[-1]['message']['chat']['id']
                return chat_id
        except telepot.exception.TelegramError as e:
            print("An error occurred:", e)

        # 1초 대기
        time.sleep(1)

    # 대기 시간 동안 아무 메시지도 수신되지 않은 경우 None 반환
    return None


def register(id):
    # 새로운 id를 기존 데이터 추가
    data_id.append(id)

    chat_id = telbot_get_chatid()
    # 새로운 데이터 쓰기
    print("다시 한번 등록할 카드 태그")
    reader.write(chat_id)
    print("카드 등록 완료")


#!/usr/bin/env python



try:
    while True:
        id, text = reader.read()
        if(id == "관리자 코드"):
            id, text = reader.read()
            print('등록할 카드 태그')
            if(id == "관리자 코드"):
                print("등록취소")
                continue
            register(id)
            continue
        
        for i in data_id:
            if(id == data_id):
                #통과
                
                continue

        print("Access denied")
        

        #led 추가
except KeyboardInterrupt:
    GPIO.cleanup()



#시간 구하기
from datetime import datetime

now = datetime.now()
print(now)

# 출력결과
# 2021-11-11 13:30:05.551179