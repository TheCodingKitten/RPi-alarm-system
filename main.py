#imports
from gpiozero import LED, Button
from time import sleep
from datetime import datetime
import atexit

#globals
global systemRunning
global fireAlarm
global fireInput
global alarmSilenced

#changable variables
systemRunning = False
fireAlarm = False
fireInput = False
alarmSilenced = False

#static variables
logEntryBase = "[{}] - {} "
logType = "System Error"

#Inputs
systemUnlock = Button(27)
zone1_alarmIn = Button(18)
alarmSilence = Button(20)
alarmReset = Button(16)

#Outputs
systemLED = LED(21)
fireLED = LED(4)
troubleLED = LED(17)

#Main fn
def mainStart():
    global fireInput
    while systemRunning == True:
        systemLED.on()
        if zone1_alarmIn.is_pressed == True:
            fireInput = True
            fireAlarm("[ZONE 1]")

#fire fn
def fireAlarm(zone):
    global fireInput
    global alarmSilenced
    logType = "FIRE ALARM ACTIVATED "
    logFile.write(logEntryBase.format(datetime.now(), logType) + zone + "\n")
    resetLogType()
    while fireInput == True:
        fireLED.toggle()
        sleep(0.5)
        if fireInput == True and alarmSilence.is_pressed == True and systemUnlock.is_pressed == True:
            fireInput = False
            alarmSilenced = True
            silenced()
        if fireInput == True and alarmReset.is_pressed == True and systemUnlock.is_pressed == True:
            fireInput = False
            alarmSilenced = False
    fireLED.off()

#trouble fn
def trouble(type):
    logType = "TROUBLE"
    logFile.write(logEntryBase.format(datetime.now(), logType) + type + "\n")
    resetLogType()
    while trouble == True:
        troubleLED.toggle()
        sleep(0.5)

#silenced fn
def silenced():
    global alarmSilenced
    global fireInput
    logType = "FIRE ALARM SILENCED"
    logFile.write(logEntryBase.format(datetime.now(), logType) + "\n")
    resetLogType()
    while alarmSilenced == True:
        fireLED.toggle()
        sleep(1)
        if alarmSilenced == True and alarmReset.is_pressed == True and systemUnlock.is_pressed == True:
            fireLED.on()
            alarmSilenced = False
            sleep(0.25)
            fireLED.off()
        if zone1_alarmIn.is_pressed == True:
            fireInput = True
            alarmSilenced = False
            fireAlarm("[ZONE 1]")
    fireLED.off()

#logType reset fn
def resetLogType():
    global logType
    logType = "SYSTEM ERROR"

systemRunning = True #Enable power LED

logFile = open("ControlPanel.log", "a") #open or create log file

#start system
if systemRunning == True:
    #add entry to log file stating the script has started fully
    logType = "SYSTEM STARTED"
    logFile.write(logEntryBase.format(datetime.now(), logType) + "\n")
    resetLogType()
    mainStart()

trouble("- END OF SCRIPT REACHED")
