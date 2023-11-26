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
manage_id = 659122598553
data_id = [659122598553] #데이터 초기화
reader = SimpleMFRC522() #RFID 객체 생성
red_led = 18
green_led = 40
servo_pin = 12
id_name = dict()

# 봇 토큰을 사용하여 봇을 초기화
bot_token = '6873483008:AAEh14eISGJdMR_zRP861w_FMrkrYUcd1t8'
bot = telepot.Bot(bot_token)

# GPIO 세팅
GPIO.setmode(GPIO.BOARD) # BOARD: Pin 번호 사용
GPIO.setup(servo_pin, GPIO.OUT) # 서보모터
GPIO.setup(red_led,GPIO.OUT)
GPIO.setup(green_led,GPIO.OUT)
GPIO.output(red_led, False) # red
GPIO.output(green_led, False) # green


def telbot_get_chatid():
    """
    텔레그램 봇에서 받은 chat_id 얻는 함수
    """
    temp = False

    # 대기 시간 동안 메시지를 체크
    start_time = time.time()
    wait_time = 60

    print("제공되었던 봇으로 이름을 보내세요 : 60seconds wait...")

    while time.time() - start_time < wait_time:
        if (time.time() - start_time) % 10 == 0:
            print(time.time() - start_time)
        
        # 메시지 수신
        response = bot.getUpdates()
        if response:
            if response[-1]['message']['date'] - start_time > 0:
                # 가장 최근 메시지의 채팅 ID 반환
                chat_id = response[-1]['message']['chat']['id']
                name = response[-1]['message']['text']
                return chat_id, name

    # 대기 시간 동안 아무 메시지도 수신되지 않은 경우 None 반환
    return None, None
    while time.time() - start_time < wait_time:
        if (time.time() - start_time % 10) == 0:
            print(time.time() - start_time)
        
        # 메시지 수신
        response = bot.getUpdates()
        if response:
            if response[-1]['message']['date'] - start_time > 0:
                # 가장 최근 메시지의 채팅 ID 반환
                chat_id = response[-1]['message']['chat']['id']
                name = response[-1]['text']
                return chat_id, name
    
    # 대기 시간 동안 아무 메시지도 수신되지 않은 경우 None 반환
    return None, None


def register(id):
    """
    새로운 RFID 태그 id 등록
    """

    # 새로운 id를 기존 데이터 추가
    data_id.append(id)

    chat_id, name = telbot_get_chatid()

    if chat_id == None:
        data_id.remove(id)
        print("텔레그램 봇에 메시지를 보내지 않아 등록이 취소되었습니다.")
        return
    
    # 새로운 데이터 쓰기
    GPIO.output(green_led, True)
    print("다시 한번 등록할 카드 태그")
    reader.write(str(chat_id))
    id_name[id] = name
    GPIO.output(green_led, False)
    print("카드 등록 완료")

def send_telegram_message(id, t):
    """
    텔레그램 메시지 전송 함수
    id: chat id
    t: time
    """

    message = f"{id_name[id]}님 카드 태그 성공 메시지입니다.\n시간: {t}"
    bot.sendMessage(id, message)

def open_door():
    """
    서보모터로 문을 열어주는 함수
    """
    # 서보 모터에 50Hz 주기로 PWM 생성
    servo = GPIO.PWM(servo_pin, 50)
    # pwm 신호를 2.5%로 시작
    servo.start(2.5)
    # duty cycle을 12.5%로 변경
    servo.ChangeDutyCycle(12.5)
    sleep(2)

def close_door():
    """
    서보모터로 문을 닫아주는 함수
    """
    # 서보 모터에 50Hz 주기로 PWM 생성
    servo = GPIO.PWM(servo_pin, 50)
    # pwm 신호를 2.5%로 시작
    servo.start(2.5)
    # duty cycle을 5%로 변경
    servo.ChangeDutyCycle(5)
    sleep(2)

# 메인부분
try:
    while True:
        id, text = reader.read()
        print(f"현재 Tag한 id: {id}")
        try:
            text = int(text)
        except:
            print("text 변수가 chat_id가 아님")

        if(id == manage_id):
            id, text = reader.read()
            print('등록할 카드 태그')
            sleep(2)
            id, text = reader.read()
            if(id == manage_id):
                print("등록취소")
                sleep(2)
                continue
            register(id)
            continue
        
        if id in data_id:
            # 텔레그램 봇으로 메시지 전송
            send_telegram_message(text, datetime.now())
            
            # 서보 모터로 문 오픈
            # green_led
            open_door()
            GPIO.output(green_led, True)
            
            sleep(5) # 5초 대기
            
            # 서보 모터로 문 닫기
            close_door()
            GPIO.output(green_led, False)
        else:
            print("Access denied")
            
            # red_led
            GPIO.output(red_led, True)
            sleep(2)
            GPIO.output(red_led, False)

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()



"""
#시간 구하기
now = datetime.now()
print(now)

# 출력결과
# 2021-11-11 13:30:05.551179
"""
