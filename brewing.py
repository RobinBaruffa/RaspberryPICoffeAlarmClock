import RPi.GPIO as GPIO
import pigpio
import time

class Brewing:
    def __init__(self):
        self.servo = pigpio.pi()
        self.servo.set_mode(12, pigpio.OUTPUT)
        self.servo.set_mode(19, pigpio.OUTPUT)


        self.push_button_open_position =   190000
        self.push_button_closed_position = 450000

        self.switch_on_position =  300000
        self.switch_off_position = 190000

        self.servo.hardware_PWM(12, 200, self.switch_off_position) #ON/OFF switch
        self.servo.hardware_PWM(19, 200, self.push_button_open_position) #Release button

    def start_brewing(self):
        self.servo.hardware_PWM(19, 200, self.switch_on_position) #Turn coffee machine On
        time.sleep(45) #delay in sec until coffe machine warmed up
        self.servo.hardware_PWM(12, 200, self.push_button_closed_position) #push button
        time.sleep(0.5)
        self.servo.hardware_PWM(12, 200, self.push_button_open_position) #release button
        time.sleep(20) #delay in sec before overfilling

        self.servo.hardware_PWM(19, 200, self.switch_off_position)

    def __del__(self):
        print("Exiting...")
        self.servo.hardware_PWM(12, 200, self.push_button_open_position)
        time.sleep(0.1)
        self.servo.hardware_PWM(19, 200, self.switch_off_position)
        time.sleep(0.2)
        self.servo.stop()
        time.sleep(0.2)
        GPIO.cleanup()

# servo = pigpio.pi()
# servo.set_mode(12, pigpio.OUTPUT)
# servo.set_mode(19, pigpio.OUTPUT)
# servo.hardware_PWM(12, 200, 500000)
# servo.hardware_PWM(19, 200, 500000)