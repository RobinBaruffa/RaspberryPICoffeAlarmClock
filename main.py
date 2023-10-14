#!/usr/local/bin/python3
import sys

# This gets the Qt stuff
from PyQt5.QtWidgets import *
import datetime
import time
import threading
from signal import signal, SIGINT
# This is our window from QtCreator
import mainwindow_auto
from brewing import Brewing

# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self) # gets defined in the UI file
        self.showFullScreen()
        ### Hooks to for buttons
        self.HoursPlus.clicked.connect(lambda: self.AddHour())
        self.HoursMinus.clicked.connect(lambda: self.RemoveHour())
        self.MinutesPlus.clicked.connect(lambda: self.AddMinute())
        self.MinutesMinus.clicked.connect(lambda: self.RemoveMinute())
        self.SetAlarm.clicked.connect(lambda: self.StartCountdown())
        self.StopAlarm.clicked.connect(lambda: self.StopCountdown())
        self.Quit.clicked.connect(self.close)

        self.CoffeeNow.clicked.connect(lambda: self.StartCoffee())

        self.waking_time = datetime.datetime.now()
        self.countdown = False
        self.b = Brewing()

        timeCheckThread = threading.Thread(target=self.timeCheckThreadCallback, daemon=True)
        timeCheckThread.start()



    def AddHour(self):
        self.waking_time = self.waking_time + datetime.timedelta(hours=1)
        self.UpdateWakeUpTime()
    def RemoveHour(self):
        self.waking_time = self.waking_time - datetime.timedelta(hours=1)
        self.UpdateWakeUpTime()
    def AddMinute(self):
        self.waking_time = self.waking_time + datetime.timedelta(minutes=1)
        self.UpdateWakeUpTime()
    def RemoveMinute(self):
        self.waking_time = self.waking_time - datetime.timedelta(minutes=1)
        self.UpdateWakeUpTime()
    def StartCountdown(self):
        self.SetAlarm.setStyleSheet("color: rgb(138, 226, 52);")
        self.countdown = True
    def StopCountdown(self):
        self.SetAlarm.setStyleSheet("color: rgb(0, 0, 0);")
        self.countdown = False
    def UpdateWakeUpTime(self):
        self.CorrectWakeUpTime()
        self.WakeUpTime.setText(self.waking_time.strftime("%H:%M"))
    def StartCoffee(self):
        print("Starting coffee")
        self.StopCountdown()
        self.b.start_brewing()
        

    def CorrectWakeUpTime(self):
        if self.waking_time - datetime.datetime.now() < datetime.timedelta(days=0):
            self.waking_time = self.waking_time + datetime.timedelta(days=1)
        elif self.waking_time - datetime.datetime.now() > datetime.timedelta(days=0):
            self.waking_time = self.waking_time - datetime.timedelta(days=1)


    def timeCheckThreadCallback(self):
        while True:
            time.sleep(0.9)
            timeRemaining = self.waking_time - datetime.datetime.now()
            timeRemaining_string = f"{int(timeRemaining.seconds / (60*60)):02d}:{int((timeRemaining.seconds / 60)%60)}"
            self.RemainingTime.setText(timeRemaining_string)

            if self.waking_time == datetime.datetime.now() and self.countdown:
                self.StartCoffee()

    def closeEvent(self, event):
        del self.b

def main():
    
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    # without this, the script exits immediately.
    sys.exit(app.exec_())

# python bit to figure how who started This
if __name__ == "__main__":
   main()

