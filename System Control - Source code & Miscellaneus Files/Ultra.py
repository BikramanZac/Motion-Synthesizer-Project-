##########################################
#Camosun College - Electronics           #
#Project Group:   BikrAmanZac            #
#Project:         Motion Synthesizer     #
#                                        #
#Group Members:   Amandeep Singh         #
#                 Bikramjit Singh        #
#                 Zachary Legg           #
##########################################

##Motion Synthesizer - Ultra.py                  

##This is the script which controls everything related to the ultrasonic sensors. 
##There are two sensors used, and this file controls what each sensor does and what sounds they play.
##This file gets runs as child process from the main ssytemcontrol.py script 

from tkinter import *
import time 			#Imported module for delays in the script.
from psonic import * 	#Important moduile that enables Python interface for Sonic Pi.
import RPi.GPIO as GPIO #Import module to interface with IO pins.


SynthesizerNumber = 0 		#Value to determine which synthesizer should be used with the first ultrasonic sensor. 
SynthesizerNumber2 = 0 		#Value to determine which synthesizer should be used with the second ultrasonic sensor. 
NoteRateDeterminer = 0.2 	#Float that determines the delay between each note. We call it the note rate.
arpeggioB00l = 0 			#Boolean that sets the arpeggio mode on or off. 

#GPIO.setwarnings(False)

#This is so that the Python script will loop continuously...
while True:
       
        #This is a setting that means when I define a pin I use the number after the GPIO (EX: TRIG=27 is for GPIO27).
        GPIO.setmode(GPIO.BCM)
        #Setup the pins for the ultrasonic sensors and the push buttons.
        TRIG = 23 
        ECHO = 24
        TRIG2 = 17 
        ECHO2 = 27
        SynthChanger = 6 		#Input that changes the synthesizer of the first ultrasonic sensor.
        SynthChanger2 = 26 		#Input that changes the synthesizer sound effect of the second ultrasonic sensor. 
        SoundRateIncreaser = 13 #Input for the user to change the speed at which the notes are played.
        arpeggioModeButton = 19 #Input that changes the notes played to arpeggios.            
            
        #Setting the GPIOs of the Raspberry Pi 3.
        GPIO.setup(TRIG,GPIO.OUT) 
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.setup(TRIG2,GPIO.OUT) 
        GPIO.setup(ECHO2,GPIO.IN)
        GPIO.setup(SynthChanger,GPIO.IN)
        GPIO.setup(SynthChanger2,GPIO.IN)
        GPIO.setup(SoundRateIncreaser,GPIO.IN)     
        GPIO.setup(arpeggioModeButton,GPIO.IN)
                        
        #Check if the 'arpeggioModeButton' was presses by a user to toggle the arpeggio mode on or off.   
        if GPIO.input(arpeggioModeButton)== 0:
            time.sleep(0.3)			#debounce
            arpeggioB00l += 1		#arpeggio mode toggled on and off using 'arpeggioB00l'.
            if arpeggioB00l > 1:
                arpeggioB00l = 0
            while GPIO.input(arpeggioModeButton)== 0:
                True
                
        
        #Check if the 'SoundRateIncreaser' button is pressed, and cycle through the 3 speed settings when it is pressed.        
        if GPIO.input(SoundRateIncreaser)== 0:
            time.sleep(0.3) 				#debounce
            NoteRateDeterminer -= 0.1 		#the maximum delay between each note should be 0.3 seconds.
            if NoteRateDeterminer < 0.09:	#the minimum delay between each note should be 0.1 seconds.
                NoteRateDeterminer = 0.3                                              
            while GPIO.input(SoundRateIncreaser)== 0:
                True
            
                      
        #Check if the 'SynthChanger' button was pressed to cycle through the first ultrasonic sensor synthesizer's sound effects.     
        if GPIO.input(SynthChanger)== 0:
            time.sleep(0.3) #Debounce the switch
            SynthesizerNumber += 1
            if SynthesizerNumber > 10:
                SynthesizerNumber = 0
            while GPIO.input(SynthChanger)== 0:
                True
        #There are only 10 different synthesizer sound effects to choose from for each ultrasonic sensor.            
        if SynthesizerNumber == 0:
            Synthesizer = CHIPBASS
        if SynthesizerNumber == 1:
            Synthesizer = MOD_SAW
        if SynthesizerNumber == 2:
            Synthesizer = PRETTY_BELL
        if SynthesizerNumber == 3:
            Synthesizer = PROPHET
        if SynthesizerNumber == 4:
            Synthesizer = CHIPLEAD
        if SynthesizerNumber == 5:
            Synthesizer = GROWL
        if SynthesizerNumber == 6:
            Synthesizer = MOD_SINE
        if SynthesizerNumber == 7:
             Synthesizer = PULSE
        if SynthesizerNumber == 8:
            Synthesizer = HOOVER
        if SynthesizerNumber == 9:
             Synthesizer = MOD_TRI     
        #Check if the 'SynthChanger' button was pressed to cycle through the first ultrasonic sensor synthesizer's sound effects.  
        if GPIO.input(SynthChanger2)== 0:
            time.sleep(0.3) #debounce
            SynthesizerNumber2 += 1
            if SynthesizerNumber2 > 10:
                SynthesizerNumber2 = 0
            while GPIO.input(SynthChanger2)== 0:
                True
        #There are only 10 different synthesizer sound effects to choose from for each ultrasonic sensor.             
        if SynthesizerNumber2 == 0:
            Synthesizer2 = BEEP
        if SynthesizerNumber2 == 1:
            Synthesizer2 = DTRI
        if SynthesizerNumber2 == 2:
            Synthesizer2 = DSAW
        if SynthesizerNumber2 == 3:
            Synthesizer2 = FM
        if SynthesizerNumber2 == 4:
            Synthesizer2 = PIANO
        if SynthesizerNumber2 == 5:
            Synthesizer2 = PLUCK
        if SynthesizerNumber2 == 6:
            Synthesizer2 = SINE
        if SynthesizerNumber2 == 7:
             Synthesizer2 = SUBPULSE
        if SynthesizerNumber2 == 8:
            Synthesizer2 = TB303
        if SynthesizerNumber2 == 9:
             Synthesizer2 = ZAWA


        #The next lines of code will get distance measurements from the rwo ultrasonic sensors.
        #This is for the first ultrasonic sensor's distance measurement.
        GPIO.output(TRIG, False)
        time.sleep(0.005)			#make sure that the trigger pin of the ultrasonic sensor is low before sending out a pulse.
        GPIO.output(TRIG, True)
        time.sleep(0.00001)			# send an ultrasonic pulse.
        GPIO.output(TRIG, False)   
        watchdogTimer = time.time() #this watch dog variable is there to make sure that the program doesn't get
        #stuck in an infinite loop when waiting for the pulse to return. This could happen if the pulse was deflected away from the sensor.
        while GPIO.input(ECHO)==0: 	#Wait for the ultrasonic sensor to indicate the pulse has been detected.
            pulsestart = time.time()
            watchdogMonitor = pulsestart - watchdogTimer #make sure that the code doesn't stay in this loop too long.
            if watchdogMonitor > 0.01:
                break
        while GPIO.input(ECHO)==1:				#Get the time it takes for the ECHO Pin on the ultrasonic sensor to go LOW.
            pulseend = time.time()
        pulse_duration = pulseend - pulsestart 	#Find out how long it toolk the pulse to hit the target and come back.
        distance = pulse_duration * 17150		#Use the speed of sound to determine the distance in centimeters. 
        distance = int(distance) 				#convert the distance from a float to an integer so it can be easily printed and used by Sonic Pi.
        #Below is for the second ultrasonic sensor's distance measurements.
        #The code is similar to to the first ultrasonic sensor's distance measurements.
        GPIO.output(TRIG2, False)
        time.sleep(0.005)     
        GPIO.output(TRIG2, True)
        time.sleep(0.00001)
        GPIO.output(TRIG2, False)
        watchdogTimer = time.time()
        while GPIO.input(ECHO2)==0:
            pulsestart = time.time()
            watchdogMonitor = pulsestart - watchdogTimer
            if watchdogMonitor > 0.01:
                break
        while GPIO.input(ECHO2)==1:
            pulseend = time.time()
        pulse_duration = pulseend - pulsestart
        distance2 = pulse_duration * 17150
        distance2 = int(distance2)
        
        
        #Below we are using the distance measurements to play different notes via Sonic Pi. 
        if arpeggioB00l == 0: #If arpeggio mode was toggled off then only play single notes.
        #the first and second ultrasonic sensor play intermittently.
            if distance > 0:			#check if the distance is greater than zero so that we don't have any errors sending notes to Sonic Pi.
                print (distance,"cm") 	#print distance.
                note = distance + 60 	#Add 60 to the distance value to put the notes in a reasonable range for midi in Sonic Pi. 
                if 100> note > 50: 		#Only play notes for measurements made up to 50 cm.  
                    use_synth(Synthesizer) #Use the first ultrasonic sensors, selected synthesizer.
                    play([note, note -12])
            time.sleep(NoteRateDeterminer/2) #delay between the first and the second ultrasonic sensor synthesizer notes.
            #The rest of the code up to the next delay is the same code used to produce a note with Sonic Pi, using the sensors distance measurements.
            #This part is for the second ultrasonic sensor's synthesizer sound.
            if distance2 > 0: 
                print (distance2,"cm")
                note = distance2 + 60
                if 100> note > 50:
                    use_synth(Synthesizer2) #Use the second ultrasonic sensors, selected synthesizer.
                    play([note, note - 17])                               
            time.sleep(NoteRateDeterminer/2)                  
        if arpeggioB00l == 1:#If arpeggio mode was toggled on then play indicated notes with the specified arpeggio mood.           
            if distance > 0:
                print (distance,"cm")
                note = distance + 40
                if 80> note > 30:
                    use_synth(Synthesizer)
                    #play([note, note -12, note + 12, note - 36, note - 24], decay=0.1, sustain_level=0.6, sustain=0.2, release=noteReleaseDeterminer)
                    play_pattern_timed( chord(note, MAJOR7), NoteRateDeterminer) #The first ultrasonic sensor's synthesizor will create MAJOR sounding arpeggios.    
            if distance2 > 0: 
                print (distance2,"cm")
                note = distance2 + 40
                if 80> note > 30:
                    use_synth(Synthesizer2)
                    #play([note, note - 17, note + 4, note - 29, note - 25], decay=0.1, sustain_level=0.6, sustain=0.2, release=noteReleaseDeterminer)
                    play_pattern_timed( chord(note, MINOR7), NoteRateDeterminer)#The Sencond ultrasonic sensor's synthesizor will create MINOR sounding arpeggios.
        
        file = open("test.txt", "r")
        val = file.read(1)
        file.close()
        if val == "2":
            break    
        
        
        GPIO.cleanup() #Necessary when using the GPIO pins.
