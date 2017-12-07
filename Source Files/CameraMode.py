##########################################
#Camosun College - Electronics           #
#Project Group:   BikrAmanZac            #
#Project:         Motion Synthesizer     #
#                                        #
#Group Members:   Amandeep Singh         #
#                 Bikramjit Singh        #
#                 Zachary Legg           #
##########################################

##Motion Synthesizer - CameraMode.py                  
##
##This is the CameraMode file which controls everything to do with the camera. In the CameraMode, there are two modes that
##the user can choose between. The first is the Ball Tracking mode and the second is the Dance Mode. The user can toggle through
##these two modes using the "CameraModeChanger" button. This mode has a very simple Tkinter GUI. When the camera is loading,
##The GUI tells the user to wait. When the user is in the camera mode, they will see the video stream pop up on top of the GUI.
##For all the camera mode computer vision techniques, we are using OpenCV.

import numpy as np
import argparse
import cv2
import time          #Used for the delays when getting ultrasonic sensor readings (Distance).
from psonic import * #Important library that enables Python interface for Sonic Pi.
from tkinter import *
import subprocess
import RPi.GPIO as GPIO


win = Tk() 							#Initialize the GUI window.
win.geometry('638x167+340+450')		#This GUI is to indicate the camera is loading.
win.title("Camera Mode Loading")
LoadingCameraImage= PhotoImage(file='LoadingCameraMessage.ppm')
can = Canvas(win, height=167, width=638)	#Dimensions are set to fit the text inside so and so that it is easy for the user to see.
can.create_image(0,0,image=LoadingCameraImage, anchor='nw')
can.pack() 									#Display the "Camera Loading" message to let the user know the camera is loading.
win.update()

##We initialize the screens resolution to set all windows and GUI items so that they centered properly. 
displayWidth = 1280
displayHeight = 1024
HalfDisplayWidth = int(displayWidth/2)	#Determine these values for less math later on in the Main Loop.
HalfDisplayHeight = int(displayHeight/2)
frameWidth = 700						#Initialize the video streams frame size for use in placing the frames for diaplays on the screen.
frameHeight = 580
HalfFrameWidth = int(frameWidth/2)		#Again determining these values for less math in the Main Loop.
HalfFrameHeight = int(frameHeight/2)
track1 = 2								#Tracks are for the songs that will play in the dance mode. THere are 4 different songs.
track2 = 0								#Any song can be used, but the code must be modified for the different file names.
track3 = 0
track4 = 0

#In the Dance mode, we base wether the music plays or stops on how much movement a user is making. We are using frame difference to
#detect how much motion the user makes. This system runs at a very fast frame rate and we need to average the difference detected
#through all the frames to get a smoother representation of how much the user is actually moving.
avgArray = [0,0,0,0,0]
    
def windowAverage(Array, totalAvg):		#This is the function that does the window average to smooth the frame difference readings for the dance mode.
    Array[0] = Array[1]
    Array[1] = Array[2]
    Array[2] = Array[3]
    Array[3] = Array[4]
    Array[4] = totalAvg
    windowedAvg = int((Array[0] + Array[1] + Array[2] + Array[3]+ Array[4])/5)
    return windowedAvg


LowerThreshold = (56,201,150)    # values changed for accurate tracking of specific object
UpperThreshold = (56, 201, 150)

noteRate = 2			#Variable that determines the speed that the notes will play.
noteRateCount = 0		#Count value to compare against the NoteRate value to determine when it is appropriate to play the note. 

init_x = 0    # initial x reference point 
init_y = 0    # initial y ref. point


camera = cv2.VideoCapture(0) 		#Get the Camera loaded and try until it is.
while (camera.isOpened()==False):
    camera= cv2.VideoCapture(0)
  
win.destroy() 						#After the camera is loaded, destroy the "Camera Loading" window.

GPIO.setmode(GPIO.BCM) 				#Setup all the GPIO buttons. All inputs and no Outputs.
CameraModeChanger = 8
CameraModeSynthChange = 7
CalibrationButton = 6			#When in the ball tracking mode, the user can press the Calibration button to calibrate the system for any color object they desire.
GPIO.setup(CameraModeChanger,GPIO.IN)
GPIO.setup(CameraModeSynthChange,GPIO.IN)
GPIO.setup(CalibrationButton,GPIO.IN)
initialCal = True	 			#Initially in the ball tracking mode, the user will need to calibrate the system to detect an object of their choosing.


##The Main LOOP
while True: 
##Before the user presses the cameraModeChange button, they will see the introductory screen for Camera mode.
##It just lets them know that they are in camera mode and that they need to press the CameraModeChange button to toggle through the Camera Modes.
    grabbed, frame = camera.read()
    frame = cv2.resize(frame, (frameWidth, frameHeight))
    cv2.rectangle(frame, (0,0), (750,150), (49, 189, 30), -1)
    cv2.rectangle(frame, (0, 0), (150, 590), (148, 24, 4), -1)
    cv2.rectangle(frame, (550, 0), (750, 590), (143, 148, 4), -1)
    cv2.rectangle(frame, (0,430), (750, 590), (136, 4, 148), -1)
    cv2.putText(frame, ("Camera Mode"),(190,100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 3, cv2.LINE_AA)
    cv2.putText(frame, ("Start"),(285,485), cv2.FONT_HERSHEY_SIMPLEX, 1.9, (255,255,0), 5, cv2.LINE_AA)
    cv2.putText(frame, ("Press Camera Change Button"),(60,550), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,0), 3, cv2.LINE_AA)
    cv2.imshow("Camera Mode", frame)
    cv2.moveWindow('Camera Mode', (HalfDisplayWidth-HalfFrameWidth),(HalfDisplayHeight-int(HalfFrameHeight/2)))
    key = cv2.waitKey(1) & 0xFF
    # if the 'esc' key is pressed, stop the loop
    if key == 27:
            break
        
    if GPIO.input(CameraModeChanger)== 0:		#Once the user presses the CameraModeChange button, they will initially enter the Ball tracking mode.
        time.sleep(0.3)
        while GPIO.input(CameraModeChanger)== 0:#We debounce every switch and also wait for the user to release the button before they continue.
            pass
        time.sleep(0.3)
        cv2.destroyAllWindows()		#Get rid of all the windows and give way for the next window.
        synthCounter = 0			#This is a value that determines which synthesizer sound effect will be used in ball tracking mode.
        
        while True:                                
            ##Calibration for Ball tracking mode.
            #In ball tracking mode, the user chooses an object and calibrates the system to recognize only that object based on its HSV color values.
            #It's important to note that ball traking mode tracks any object NOT JUST BALLS, we just used balls when we were designing it and named the mode accordingly.
            
			if GPIO.input(CalibrationButton)== 0 or initialCal is True:	#On the first time in ball tracking mode, we calibrate the software for an object that the user chooses.
            
			##If the user wants to calibrate and use another objects they can press the CalibrationButton to run this calibration code again to set different threshold values for a different object.    
                cv2.destroyAllWindows()	#Make sure there are no other windows open before beginning the initial calibration.
                calcount = 0			#CalCount is used to count down how much time the user has until the device calibrates with the object they choose.

##To calibrate the HSV thresholds used to detect the objects, the user will place the object so that it is in the center of the
##specified circle fields displayed in the window. We then save a picture and extract what color that object is. We use those values
##to determine the Lower and Upper Threshold values used in the detection process.
                while calcount<100:
                    grabbed, frame = camera.read()
                    frame = cv2.resize(frame, (frameWidth, frameHeight))
                    frame = cv2.flip(frame,1)
                    #Count down that gives the user enough time to read the instructions on the screen to calibrate the system. 
                    if calcount<20:
                        cv2.putText(frame, ("5"),(300,175), cv2.FONT_HERSHEY_SIMPLEX, 5, (157,0,255), 7, cv2.LINE_AA)
                    if 20<calcount<40:
                        cv2.putText(frame, ("4"),(300,175), cv2.FONT_HERSHEY_SIMPLEX, 5, (157,0,255), 7, cv2.LINE_AA)
                    if 40<calcount<60:
                        cv2.putText(frame, ("3"),(300,175), cv2.FONT_HERSHEY_SIMPLEX, 5, (157,0,255), 7, cv2.LINE_AA)
                    if 60<calcount<80:
                        cv2.putText(frame, ("2"),(300,175), cv2.FONT_HERSHEY_SIMPLEX, 5, (157,0,255), 7, cv2.LINE_AA)
                    if 80<calcount<100:
                        cv2.putText(frame, ("1"),(300,175), cv2.FONT_HERSHEY_SIMPLEX, 5, (157,0,255), 7, cv2.LINE_AA)
                    ##Below we are defining the circle that the user must put the object in to calibrate it. Also putting text which gives instructions.  
                    cv2.circle(frame,(350,290), 20, (0, 237, 0), 5)
                    cv2.circle(frame,(350,290), 30, (217, 0, 237), 7)
                    cv2.putText(frame, ("Fill the circle with your ball"),(150,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3, cv2.LINE_AA)
                    cv2.imshow('Calibration', frame)
                    cv2.moveWindow('Calibration',(HalfDisplayWidth-HalfFrameWidth),(HalfDisplayHeight-int(HalfFrameHeight/2)))
                    calcount+=1                   
                    key = cv2.waitKey(1) & 0xFF
                    
                cv2.imwrite('/home/pi/Pictures/FOX.jpg',frame)#After the countdown, the image of the object is saved.
                cv2.destroyAllWindows()#Destroy the calibration window.
                image = cv2.imread('/home/pi/Pictures/FOX.jpg')#We then use the saved image of the object to extract the objects unique HSV color components.
                imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                HSV = imageHSV[290, 350]#We extract the HSV color components of the center pixel of the object.
                LowerThreshold = (int(HSV[0]-20),int(HSV[1]-20),int(HSV[2]-20))#Use the HSV color data to set threshold values for the object detecting process.
                UpperThreshold = (int(HSV[0]+20),int(HSV[1]+20),int(HSV[2]+20))
                if initialCal is True:
                    initialCal = not initialCal#Once the initial calibration has terminated, we dont need to run a calibration unless the user needs to,
                                               #and in that case, they will just press the CalibrationButton.
            
            ##Calibration Done.
            
            
            
            if GPIO.input(CameraModeSynthChange)== 0:#If the user presses the CameraModeSynthChange button, they can go through the list of sound effects.
                synthCounter += 1
                if synthCounter>9:
                   synthCounter=0
                while GPIO.input(CameraModeSynthChange)== 0:
                    pass 
            
            
            #10 sound effects to choose from.
            if synthCounter == 0:
                Synthesizer = CHIPLEAD
            if synthCounter == 1:
                Synthesizer = DTRI
            if synthCounter == 2:
                Synthesizer = DSAW
            if synthCounter == 3:
                Synthesizer = FM
            if synthCounter == 4:
                Synthesizer = CHIPBASS
            if synthCounter == 5:
                Synthesizer = BLADE
            if synthCounter == 6:
                Synthesizer = SINE
            if synthCounter == 7:
                 Synthesizer = SUBPULSE
            if synthCounter == 8:
                Synthesizer = TB303
            if synthCounter == 9:
                 Synthesizer = ZAWA
            
            
            
            #Object Detection Start
            grabbed, frame = camera.read()						#Get current frame.
            frame = cv2.resize(frame, (frameWidth, frameHeight))#Resize it.
            frame = cv2.flip(frame,1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)		#Change it to HSV color Space
            mask = cv2.inRange(hsv, LowerThreshold, UpperThreshold)#Use the threshold values to from calibration to mask the HSV frame.
            mask = cv2.dilate(mask, None, iterations=10)		#Dilate the image.
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]#Find all the contours.
            center = None										#Initialize centre for an object if it exists.
            
            
                
            
            
            if len(cnts) > 0:					  #Check to see if the there are any contours detected.
                c = max(cnts, key=cv2.contourArea)#find biggest countour in the frame based off of the mask.
                ((x, y), radius) = cv2.minEnclosingCircle(c)    # x,y is the center 
                M = cv2.moments(c)                              # moments collection is used to calculate the center 
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # find center of the contour/object 
                        
                if radius > 1: #If the object has a radius greater the specified amount, we can play music with that information.
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)#Display a red circle in the center of the object.
                    init_x = center[0]#Get the x coordinate of the object's center.
                    musicx = int((init_x*30/frameWidth)+50)#Scale the value to a range of MIDI notes that work.
                    init_y= center [1]#Get the y coordinate of the object's center.
                    musicy = init_y
					
                    ##To play music using the position values of the object, we are basing the pitch of the note played by the
                    ##x coordinate of the object on the frame and we are basing the note rate on the y position of the object
                    ##on the frame. As the iobjects gets further away from the centre of the frame in the y direction (either up or down)
                    ##the note rate slows down. As the x coordinate value gets bigger, the pitch gets higher.
                    ##If no object is detected or the object is to small or far away, no music is played. 
					
                    if musicy > 348:
                        if musicy > 464:
                            noteRate = 3
                        else:
                            noteRate = 2
                    elif musicy < 232:
                        if musicy < 116:
                            noteRate = 3
                        else:
                            noteRate = 2
                    elif 232 < musicy < 348:
                        noteRate = 1
                    noteRateCount += 1
                        
                    if noteRateCount > noteRate:
                        noteRateCount = 0
                        if 81 > (musicx) > 49:
                            use_synth(Synthesizer)          
                            play(musicx)
							
            #In the ball tracking mode, we show the current frame with a red dot indicating the center of the object.
            #the display is in the middle of the screen 3/4 of the way down from the top of the screen.
			
            cv2.imshow("Ball Mode", frame)
            cv2.moveWindow('Ball Mode', (HalfDisplayWidth-HalfFrameWidth),(HalfDisplayHeight-int(HalfFrameHeight/2)))
            
            #Because we are in Camera Mode, we need to check the test.txt file to determine wether the master process wants to shut down this process.
            #If the value in the file is '1', we need to break out of all the while loops and release the camera.
			
            file = open("test.txt", "r")
            val = file.read(1)
            file.close()
            if val == "1":
                break
            #If the user presses the CameraModeChanger button, the Ball tracking mode is closed and the Danceing mode is started.
            if GPIO.input(CameraModeChanger)== 0:
                cv2.destroyAllWindows()	#Destroy the Ball tracking window.
                break
            key = cv2.waitKey(1) & 0xFF
			
            # if the 'esc' key is pressed, stop the loop
            if key == 27:
                cv2.destroyAllWindows()
                break
    ##Ball Traking mode end.
    
    ##Dance Mode Begin.
    if GPIO.input(CameraModeChanger)== 0:
        time.sleep(0.3)
        while GPIO.input(CameraModeChanger)== 0:
            pass
        time.sleep(0.3)
        cv2.destroyAllWindows()					#Make sure no other windows are on the screen.
        grabbed, current_frame = camera.read()	#Get Current frame
        current_frame = cv2.resize(current_frame, (frameWidth, frameHeight))#Resive frame
        previous_frame = current_frame			#Initialize the previous frame for the first loop.
		
##In Dancing mode, we compare the current frame with the previous frame to determine how much the user is moving.
##We set the difference threshold so that music stops playing when the user stops dancing and vice versa.
##If the user is dancing enough, one of the 4 tracks will play (Track is just any MP3 file you want). When they stop dancing,
##the music stops, and when they start dancing again, the next track will start playing and so on and so forth. The 4 tracks
##loop one after the other.

        while True:
            current_frame = cv2.resize(current_frame, (frameWidth, frameHeight))#Resize the frame
            frame_diff = cv2.absdiff(current_frame,previous_frame)#get difference between the current and previous frame.
            sum_diff = cv2.sumElems(frame_diff)		#get the sum of the difference of all the pixels.
            totalAverage = int(sum_diff[0]/100000)	#Get a representative averange.
            winAvg = windowAverage(avgArray, totalAverage)#Put the raw average throught the window averaging function. Smooths out the background noise.
            cv2.imshow('DANCE',frame_diff)
            cv2.moveWindow('DANCE', (HalfDisplayWidth-HalfFrameWidth),(HalfDisplayHeight-int(HalfFrameHeight/2)))
            print(winAvg)		#Print the windowed average (For Debugging!).
            
            if winAvg>30:		#Set the threshold for how much motion the user must use to get the songs to play.
                if track1 == 2:	#Using subprocesses to play the different tracks using "mpg321"
                    p = subprocess.Popen(['mpg321', 'Smooth.mp3'])
                    track1 = 0
                    track2 = 1
                if track2 == 2:
                    p = subprocess.Popen(['mpg321', 'Mario.mp3'])
                    track2 = 0
                    track3 = 1
                if track3 == 2:
                    p = subprocess.Popen(['mpg321', 'Super.mp3'])
                    track3 = 0
                    track4 = 1
                if track4 == 2:
                    p = subprocess.Popen(['mpg321', 'Crank.mp3'])
                    track1 = 1
                    track4 = 0
            else:				#If the user isn't moving enough terminate the song and set the next track up.
                try:
                    p.terminate()     
                except:
                    pass
                if track1==1:
                    track1+=1
                if track2==1:
                    track2+=1
                if track3==1:
                    track3+=1
                if track4==1:
                    track4+=1
            
            if GPIO.input(CameraModeChanger)== 0: #When the user wants to switch back to ball tracking mode, they can press the CameraModeChanger button again.
                cv2.destroyAllWindows()
                break
            #Check the test.txt file to see if the master process file wants to shut the whole camera operation down.
            file = open("test.txt", "r")
            val = file.read(1)
            file.close()
            if val == "1":
                break
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                cv2.destroyAllWindows()
                break
            
            previous_frame = current_frame.copy()#Set the previous frame to the current frame before grabing the next frame.
            ret, current_frame = camera.read()#Grab the next frame.
    try:#Stop any music playing befor going back to Ball tracking mode or before terminating the whole camera mode.
        p.terminate()     
    except:
        pass
    #Check the file again.
    file = open("test.txt", "r")
    val = file.read(1)
    file.close()
    if val == "1":
        break
    
try:
    p.terminate()     
except:
    pass

cv2.destroyAllWindows()		#Destroy all remaining windows before terminating this code.
camera.release()			#release the camera.
GPIO.cleanup() 				#Necessary when using the GPIO pins.
        
        
        
        
        
        
        
        
        
        
        
        
        