from __future__ import division
import  RPi.GPIO as GPIO
import Adafruit_PCA9685
import pygame
import math
import time
import sys

#初始化
pygame.init()
pygame.joystick.init()


PIN_NO=23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_NO,GPIO.OUT)

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

#设置舵机的最大、最小、中间位置对应数值
servo_min = 150  
servo_max = 600  
servo_mid = 375

# 舵机
pwm.set_pwm(1, 0, 375)
time.sleep(1)

# 获取小米手柄
joystick_count = pygame.joystick.get_count()
if joystick_count == 0 :
    sys.exit()


ss = servo_mid
sudu = 10 #速度

def IsJd(a):
    if a>600:a=600
    if a<150:a=150

    return math.ceil(a)

#单发射
def shoot():
    GPIO.output(PIN_NO, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(PIN_NO, GPIO.LOW)
    time.sleep(1)





while True:
    joystick = pygame.joystick.Joystick(0)
    joystick.init() 
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")


    axisX = joystick.get_axis(0) #摇杆水平方向
    axisY = joystick.get_axis(1) #摇杆垂直方向
    buttonA = joystick.get_button(0) # A按钮 自动控制
    buttonX = joystick.get_button(3) # X按钮 回正
    buttonL1 = joystick.get_button(6) # L1按钮 单发
    buttonR1 = joystick.get_button(7) # R1按钮 单发
    buttonL2 = joystick.get_button(8) # L2按钮 连发快射
    buttonR2 = joystick.get_button(9) # R2按钮 连发快射
    #print(axisX,axisY,buttonA,buttonX,buttonL1,buttonL2,buttonR2)

    

    if buttonX == 1 :
        pwm.set_pwm(1, 0, 375)
        ss = servo_mid
        print("舵机回正")

        time.sleep(1)

    if buttonA == 1 :
        print("自动模式启动")
        time.sleep(1)

    if axisX != 0 :
        ss +=sudu*axisX
        ss = IsJd(ss)
        print("水平转动：",ss)        
        pwm.set_pwm(1, 0, ss)
        time.sleep(0.05)

    if axisY != 0 :         
        ss +=sudu*axisY
        ss =IsJd(ss)
        print("垂直转动",ss)
        pwm.set_pwm(0, 0, ss)
        time.sleep(0.05)

    if buttonL1 ==1 or  buttonR1 ==1:
        print("启动单射模式")
        shoot()

    if buttonL2 ==1 or  buttonR2 ==1:
        print("启动速射连发模式")
        if GPIO.input(PIN_NO) == 0: GPIO.output(PIN_NO, GPIO.HIGH)
    elif buttonL2 ==0 or  buttonR2 ==0:        
        if GPIO.input(PIN_NO) == 1: 
            GPIO.output(PIN_NO, GPIO.LOW) 
            print("停止速射连发模式")      




# 别忘记释放资源和独占
pygame.quit ()



       



