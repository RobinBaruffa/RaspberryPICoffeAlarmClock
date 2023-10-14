import RPi.GPIO as GPIO
import pigpio
import time

class Brewing:
    def __init__(self):
        self.servo = pigpio.pi()
        self.servo.set_mode(12, pigpio.OUTPUT)
        self.servo.set_mode(19, pigpio.OUTPUT)
        self.servo.hardware_PWM(12, 200, 200000) #
        self.servo.hardware_PWM(19, 200, 190000)

    def start_brewing(self):
        self.servo.hardware_PWM(19, 200, 300000) #Turn coffee machine On
        time.sleep(44) #TODO: delay in sec until coffe machine warmed up
        
        self.servo.hardware_PWM(12, 200, 265000) #push button
        time.sleep(0.5)
        self.servo.hardware_PWM(12, 200, 190000) #release button
        time.sleep(15) #delay in sec before overfilling

        self.servo.hardware_PWM(19, 200, 190000)

    def __del__(self):
        print("Exiting...")
        self.servo.hardware_PWM(12, 200, 200000)
        time.sleep(0.1)
        self.servo.hardware_PWM(19, 200, 190000)
        time.sleep(0.1)
        GPIO.cleanup()

# servo = pigpio.pi()
# servo.set_mode(12, pigpio.OUTPUT)
# servo.set_mode(19, pigpio.OUTPUT)
# servo.hardware_PWM(12, 200, 500000)
# servo.hardware_PWM(19, 200, 500000)