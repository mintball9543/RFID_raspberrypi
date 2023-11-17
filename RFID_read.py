"""
sudo pip3 install spidev
sudo pip3 install mfrc522

"""
import telepot
import time
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# 전역변수
data_id = ['관리자 코드'] #데이터 초기화
reader = SimpleMFRC522() #RFID 객체 생성

# 봇 토큰을 사용하여 봇을 초기화
bot_token = '6873483008:AAEh14eISGJdMR_zRP861w_FMrkrYUcd1t8'
bot = telepot.Bot(bot_token)

# GPIO 세팅
GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.OUT) # 21번 핀
GPIO.setup(24,GPIO.OUT) # 24번 핀
GPIO.output(21, False) # red
GPIO.output(24, False) # green


def telbot_get_chatid():
    """
    텔레그램 봇에서 받은 chat_id 얻는 함수
    """

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
    """
    새로운 RFID 태그 id 등록
    """

    # 새로운 id를 기존 데이터 추가
    data_id.append(id)

    chat_id = telbot_get_chatid()
    # 새로운 데이터 쓰기
    print("다시 한번 등록할 카드 태그")
    reader.write(chat_id)
    print("카드 등록 완료")

def send_telegram_massage(id, t):
    """
    텔레그램 메시지 전송 함수
    id: chat id
    t: time
    """

    message = f"{id}님 카드 태그 성공 메시지입니다.\n시간: {t}"
    bot.sendMessage(id, t)

#!/usr/bin/env python


# 메인부분
try:
    while True:
        id, text = reader.read()
        print(f"현재 Tag한 id: {id}")
        
        if(id == "관리자 코드"):
            id, text = reader.read()
            print('등록할 카드 태그')
            if(id == "관리자 코드"):
                print("등록취소")
                continue
            register(id)
            continue
        
        if id in data_id:
            # 서보 모터로 문 오픈
            

            # 텔레그램 봇으로 메시지 전송
            send_telegram_massage(text, datetime.now())
            
            # green_led
            GPIO.output(24, True)
            sleep(5)
            GPIO.output(24, False)
        else:
            print("Access denied")
            
            # red_led
            GPIO.output(21, True)
            sleep(2)
            GPIO.output(21, False)

except KeyboardInterrupt:
    GPIO.cleanup()




"""
#시간 구하기
now = datetime.now()
print(now)

# 출력결과
# 2021-11-11 13:30:05.551179
"""