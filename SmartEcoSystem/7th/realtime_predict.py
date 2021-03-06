import learn
import RPi.GPIO as GPIO
import datetime
import time
import spidev
import adafruit_dht
import board

dhtDevice = adafruit_dht.DHT11(board.D4)

# 시간에 대한 리스트
timelist = []
# 습도에 대한 리스트
humilist = []
# 온도에 대한 리스트
templist = []

# panpump 함수를 정의합니다.
def panpump(hum, temp):
    #############################################
    #       예측한 습도와 온도에 따라서          #
    #    팬과 펌프를 제어하는 함수를 정의합니다.  #
    #############################################

# error 함수를 정의합니다.
def error(expected, measurement):
    ############################################
    #       수업자료에 있는 오차율 공식에 따라   #      
    #        오차율 구하는 함수를 정의합니다.    #  
    ############################################ 


#dataMag=10
dataMag = int(input("학습할 데이터의 갯수를 정하세요: "))
step = int(input("학습할 횟수를 정하세요: "))

i = 0
# i가 step값 보다 작은 범위 한에서 아래 과정을  무한반복합니다. 
try:
     while True:
        # 센서값을 읽어서 저장합니다.
        t = float(dhtDevice.temperature)
        h = float(dhtDevice.humidity)
    
        # 현재 시각에 대한 값을 저장합니다.  
        now = datetime.datetime.now()

        # 시각을 시,분,초로 나타냅니다. 
        nowTime = now.strftime('%H:%M:%S')
        
        # 시,분,초로 나타낸 현재 시각을 출력합니다.
        print(nowTime)
        
        # 습도를  형식에 맞게 값을 출력합니다..
        print('Temp={1:0.01f}*C Humidity={1:0.01f}%'.format(t, h))
    
        # i를 시간의 리스트 값으로 추가합니다.
        timelist.append(i)
        
        # 측정된 습도값을 리스트값에 추가합니다.
        humilist.append(h)
        
        # 측정된 온도값을 리스트값에 추가합니다.
        templist.append(t)
        
        # 실제 시간간격을 1초로 설정합니다.
        time.sleep(1)
         
        if i == dataMag - 1 and i != 0:
             
            W_h, b_h = learn.LinearRegression(step , 0.001, humilist, timelist, dataMag)
            W_t, b_t = learn.LinearRegression(step , 0.001, templist, timelist, dataMag)     
            
            timeNext = dataMag

            next_hum = W_h * timeNext + b_h
            real_hum = float(dhtDevice.humidity)
            
            next_temp = W_t * timeNext + b_t 
            real_temp = float(dhtDevice.temperature)
        
            # 오차율을 구하는 함수를 호출하세요.
            error(next_hum, real_hum)
            error(next_temp, real_temp)

            ###################################################
            #       지금까지 알아낸 정보들을 출력해보세요       #
            ###################################################
            
            i = 0

            timelist.clear()
            humilist.clear()
            templist.clear()

            panpump(next_hum, next_temp)

        else:
            i = i + 1

          

except KeyboardInterrupt:
    print("finish")