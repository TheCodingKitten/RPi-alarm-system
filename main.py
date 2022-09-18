#imports
from gpiozero import LED, Button
from time import sleep
from datetime import datetime

#globals
global systemRunning
global fireAlarm
global fireInput
global alarmSilenced
global troubleState

#changable variables
systemRunning = False
fireAlarm = False
fireInput = False
alarmSilenced = False
troubleState = False

#static variables
logEntryBase = "[{}] - {} " #Set basis of entry format
logType = "System Error" #Set initial log type and define var

#Inputs
systemUnlock = Button(27)
alarmSilence = Button(20)
alarmReset = Button(16,hold_time=1, hold_repeat=False)
#Zone Inputs
zone1_CallPoint = Button(18) #Change to active_state=False if using push to open button

#Outputs
systemLED = LED(21)
fireLED = LED(4)
troubleLED = LED(17)
silenceLED = LED(22)

#Main fn
def mainStart():
    global fireInput
    while systemRunning == True:
        systemLED.on()
        if zone1_CallPoint.is_pressed == True:
            fireAlarm("[ZONE 1 CALL POINT]")
    systemLED.off()

#fire fn
def fireAlarm(zone):
    global fireInput
    global alarmSilenced
    logType = "FIRE ALARM ACTIVATED"
    logFile.write(logEntryBase.format(datetime.now(), logType) + zone + "\n")
    print((logEntryBase.format(datetime.now(), logType) + zone)) #TESTING PURPOSES
    resetLogType()
    fireInput = True
    alarmSilenced = False
    silenceLED.off()
    while fireInput == True:
        fireLED.toggle()
        sleep(0.25)
        if fireInput == True and alarmSilence.is_pressed == True and systemUnlock.is_pressed == True:
            silenceAlarm()
        if fireInput == True and alarmReset.is_held == True and systemUnlock.is_pressed == True:
            resetAlarm()
    fireLED.off()

#trouble fn
def trouble(type):
    logType = "TROUBLE"
    logFile.write(logEntryBase.format(datetime.now(), logType) + type + "\n")
    print((logEntryBase.format(datetime.now(), logType) + type))
    resetLogType()
    while troubleState == True:
        troubleLED.toggle()
        sleep(0.7)

#silenced fn
def silenceAlarm():
    global alarmSilenced
    global fireInput
    logType = "ALARM SILENCED"
    logFile.write(logEntryBase.format(datetime.now(), logType) + "\n")
    print((logEntryBase.format(datetime.now(), logType)))
    resetLogType()
    alarmSilenced = True
    fireInput = False
    fireLED.off()
    while alarmSilenced == True:
        silenceLED.toggle()
        sleep(0.3)
        if alarmSilenced == True and alarmReset.is_held == True and systemUnlock.is_pressed == True:
            resetAlarm()
        if zone1_CallPoint.is_pressed == True:
            fireAlarm("[ZONE 1 CALL POINT]")

#reset alarm fn
def resetAlarm():
    logType = "ALARM RESET"
    logFile.write(logEntryBase.format(datetime.now(), logType) + "\n")
    print((logEntryBase.format(datetime.now(), logType)))
    resetLogType()
    global fireInput
    fireInput = False
    global alarmSilenced
    alarmSilenced = False
    silenceLED.on()
    fireLED.on()
    sleep(0.75)
    silenceLED.off()
    fireLED.off()

#logType reset fn
def resetLogType():
    global logType
    logType = "SYSTEM ERROR"

systemRunning = True #Allow system to start

logFile = open("ControlPanel.log", "a") #open or create log file

#start system
if systemRunning == True:
    #add entry to log file stating the script has started fully
    logType = "SYSTEM STARTED"
    logFile.write(logEntryBase.format(datetime.now(), logType) + "\n")
    print((logEntryBase.format(datetime.now(), logType)))
    resetLogType()
    mainStart() #Start main script

troubleState = True
trouble("- END OF SCRIPT REACHED")
