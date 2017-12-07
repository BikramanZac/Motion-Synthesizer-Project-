##########################################
#Camosun College - Electronics           #
#Project Group:   BikrAmanZac            #
#Project:         Motion Synthesizer     #
#                                        #
#Group Members:   Amandeep Singh         #
#                 Bikramjit Singh        #
#                 Zachary Legg           #
##########################################

##Motion Synthesizer - SystemControl.py                  
##
##This is the main file that controls all the processes of the motion synthesizer. There
##are 2 other files that are controlled by this file. The first file is the ultrasonic music
##mode and the second is the camera mode. We are using subprocessing to control the two
##different modes. Under no circumstance should either of the modes be running at the same time.
##We are using Opencv computer vision techniques to control music with motion detected by
##the camera. We chose to use the Tkinter Module for our GUI. The base of this project relies on
##the psonic module which enables us to interface with the Sonic Pi coding environment which gives
##us access to a synthesis engine.  

##MODULES:
import time
from tkinter import *
import cv2
from psonic import *
import subprocess
import RPi.GPIO as GPIO

##The screen that you are using with this device must be initialized in the following variable. This 
##is essential because it allows the Motion Synthesizer to resize the GUI for any screen Resolution.
displayWidth = 1280
displayHeight = 1024
HalfDisplayWidth = displayWidth/2#I have divided the values in half so that there are less computations later.
HalfDisplayHeight = displayHeight/2#This makes it easier to place GUI objects in the centre of the screen.

GPIO.setmode(GPIO.BCM)#We are defining the pins in this project using the Broadcom GPIO numbers (BCM).
HelpMenu = 20#Help Menu Button
ModeChangeButton = 21#Middle button which switches between Ultrasonic and Camera mode.
GPIO.setup(ModeChangeButton,GPIO.IN)#Setup the GPIOs as Inputs.
GPIO.setup(HelpMenu,GPIO.IN)

##To kill subprocesses, we have a text fiel that is accesses by both the Ultrasaonic and the Camera mode.
##There is one variable in that file and it only has two states(1 or 2). When we want to run the ultrasonic sensor
##mode, we write a "1" to the file which will then shut down the camera mode properly, by releasing the camera for
##use later. When we want to run the Camera mode, we overwrite the "1", we previously wrote, with a "2". The process
##controlling the Ultrasonic mode will then properly terminate giving the camera mode access to some of the buttons
##that were being used by the Ultrasonic mode.  
file = open("test.txt", "w")#The little "w" argument means we want to "write" to the file.("r" for "read").
file.write("1")#initially we want the UIltrasonic mode to be used.
file.close()#close file when finished the overwrite.

help = False#help is a boolean that we use to determine when the user wants to view the Help Page.

loadgifimagelist = ["LoadGIF/frame_000_delay-0.03s.gif","LoadGIF/frame_001_delay-0.03s.gif","LoadGIF/frame_002_delay-0.03s.gif",
                    "LoadGIF/frame_003_delay-0.03s.gif","LoadGIF/frame_004_delay-0.03s.gif","LoadGIF/frame_005_delay-0.03s.gif",
                    "LoadGIF/frame_006_delay-0.03s.gif","LoadGIF/frame_007_delay-0.03s.gif","LoadGIF/frame_008_delay-0.03s.gif",
                    "LoadGIF/frame_009_delay-0.03s.gif","LoadGIF/frame_010_delay-0.03s.gif","LoadGIF/frame_011_delay-0.03s.gif",
                    "LoadGIF/frame_012_delay-0.03s.gif","LoadGIF/frame_013_delay-0.03s.gif","LoadGIF/frame_014_delay-0.03s.gif",
                    "LoadGIF/frame_015_delay-0.03s.gif","LoadGIF/frame_016_delay-0.03s.gif","LoadGIF/frame_017_delay-0.03s.gif",
                    "LoadGIF/frame_018_delay-0.03s.gif","LoadGIF/frame_019_delay-0.03s.gif","LoadGIF/frame_020_delay-0.03s.gif",
                    "LoadGIF/frame_021_delay-0.03s.gif","LoadGIF/frame_022_delay-0.03s.gif","LoadGIF/frame_023_delay-0.03s.gif",
                    "LoadGIF/frame_024_delay-0.03s.gif","LoadGIF/frame_025_delay-0.03s.gif","LoadGIF/frame_026_delay-0.03s.gif",
                    "LoadGIF/frame_027_delay-0.03s.gif","LoadGIF/frame_028_delay-0.03s.gif","LoadGIF/frame_029_delay-0.03s.gif",
                    "LoadGIF/frame_030_delay-0.03s.gif","LoadGIF/frame_031_delay-0.03s.gif","LoadGIF/frame_032_delay-0.03s.gif",
                    "LoadGIF/frame_033_delay-0.03s.gif","LoadGIF/frame_034_delay-0.03s.gif","LoadGIF/frame_035_delay-0.03s.gif",
                    "LoadGIF/frame_036_delay-0.03s.gif","LoadGIF/frame_037_delay-0.03s.gif","LoadGIF/frame_038_delay-0.03s.gif",
                    "LoadGIF/frame_039_delay-0.03s.gif","LoadGIF/frame_040_delay-0.03s.gif","LoadGIF/frame_041_delay-0.03s.gif",
                    "LoadGIF/frame_042_delay-0.03s.gif","LoadGIF/frame_043_delay-0.03s.gif","LoadGIF/frame_044_delay-0.03s.gif",
                    "LoadGIF/frame_045_delay-0.03s.gif","LoadGIF/frame_046_delay-0.03s.gif","LoadGIF/frame_047_delay-0.03s.gif",
                    "LoadGIF/frame_048_delay-0.03s.gif","LoadGIF/frame_049_delay-0.03s.gif","LoadGIF/frame_050_delay-0.03s.gif",
                    "LoadGIF/frame_051_delay-0.03s.gif","LoadGIF/frame_052_delay-0.03s.gif","LoadGIF/frame_053_delay-0.03s.gif",
                    "LoadGIF/frame_054_delay-0.03s.gif","LoadGIF/frame_055_delay-0.03s.gif","LoadGIF/frame_056_delay-0.03s.gif",
                    "LoadGIF/frame_057_delay-0.03s.gif","LoadGIF/frame_058_delay-0.03s.gif","LoadGIF/frame_059_delay-0.03s.gif",
                    "LoadGIF/frame_060_delay-0.03s.gif","LoadGIF/frame_061_delay-0.03s.gif","LoadGIF/frame_062_delay-0.03s.gif",
                    "LoadGIF/frame_063_delay-0.03s.gif","LoadGIF/frame_064_delay-0.03s.gif","LoadGIF/frame_065_delay-0.03s.gif",
                    "LoadGIF/frame_066_delay-0.03s.gif","LoadGIF/frame_067_delay-0.03s.gif","LoadGIF/frame_068_delay-0.03s.gif",
                    "LoadGIF/frame_069_delay-0.03s.gif","LoadGIF/frame_070_delay-0.03s.gif","LoadGIF/frame_071_delay-0.03s.gif",
                    "LoadGIF/frame_072_delay-0.03s.gif","LoadGIF/frame_073_delay-0.03s.gif","LoadGIF/frame_074_delay-0.03s.gif",
                    "LoadGIF/frame_075_delay-0.03s.gif","LoadGIF/frame_076_delay-0.03s.gif","LoadGIF/frame_077_delay-0.03s.gif",
                    "LoadGIF/frame_078_delay-0.03s.gif","LoadGIF/frame_079_delay-0.03s.gif","LoadGIF/frame_080_delay-0.03s.gif",
                    "LoadGIF/frame_081_delay-0.03s.gif","LoadGIF/frame_082_delay-0.03s.gif","LoadGIF/frame_083_delay-0.03s.gif",
                    "LoadGIF/frame_084_delay-0.03s.gif","LoadGIF/frame_085_delay-0.03s.gif","LoadGIF/frame_086_delay-0.03s.gif",
                    "LoadGIF/frame_087_delay-0.03s.gif","LoadGIF/frame_088_delay-0.03s.gif","LoadGIF/frame_089_delay-0.03s.gif",
                    "LoadGIF/frame_090_delay-0.03s.gif","LoadGIF/frame_091_delay-0.03s.gif","LoadGIF/frame_092_delay-0.03s.gif",
                    "LoadGIF/frame_093_delay-0.03s.gif","LoadGIF/frame_094_delay-0.03s.gif","LoadGIF/frame_095_delay-0.03s.gif",
                    "LoadGIF/frame_096_delay-0.03s.gif","LoadGIF/frame_097_delay-0.03s.gif","LoadGIF/frame_098_delay-0.03s.gif",
                    "LoadGIF/frame_099_delay-0.03s.gif","LoadGIF/frame_100_delay-0.03s.gif","LoadGIF/frame_101_delay-0.03s.gif",
                    "LoadGIF/frame_102_delay-0.03s.gif","LoadGIF/frame_103_delay-0.03s.gif","LoadGIF/frame_104_delay-0.03s.gif",
                    "LoadGIF/frame_105_delay-0.03s.gif","LoadGIF/frame_106_delay-0.03s.gif","LoadGIF/frame_107_delay-0.03s.gif",
                    "LoadGIF/frame_108_delay-0.03s.gif","LoadGIF/frame_109_delay-0.03s.gif","LoadGIF/frame_110_delay-0.03s.gif",
                    "LoadGIF/frame_111_delay-0.03s.gif","LoadGIF/frame_112_delay-0.03s.gif","LoadGIF/frame_113_delay-0.03s.gif",
                    "LoadGIF/frame_114_delay-0.03s.gif","LoadGIF/frame_115_delay-0.03s.gif","LoadGIF/frame_116_delay-0.03s.gif",
                    "LoadGIF/frame_117_delay-0.03s.gif","LoadGIF/frame_118_delay-0.03s.gif","LoadGIF/frame_119_delay-0.03s.gif",
                    "LoadGIF/frame_120_delay-0.03s.gif","LoadGIF/frame_121_delay-0.03s.gif","LoadGIF/frame_122_delay-0.03s.gif",
                    "LoadGIF/frame_123_delay-0.03s.gif","LoadGIF/frame_124_delay-0.03s.gif","LoadGIF/frame_125_delay-0.03s.gif",
                    "LoadGIF/frame_126_delay-0.03s.gif","LoadGIF/frame_127_delay-0.03s.gif","LoadGIF/frame_128_delay-0.03s.gif",
                    "LoadGIF/frame_129_delay-0.03s.gif","LoadGIF/frame_130_delay-0.03s.gif","LoadGIF/frame_131_delay-0.03s.gif",
                    "LoadGIF/frame_132_delay-0.03s.gif","LoadGIF/frame_133_delay-0.03s.gif","LoadGIF/frame_134_delay-0.03s.gif",
                    "LoadGIF/frame_135_delay-0.03s.gif","LoadGIF/frame_136_delay-0.03s.gif","LoadGIF/frame_137_delay-0.03s.gif",
                    "LoadGIF/frame_138_delay-0.03s.gif","LoadGIF/frame_139_delay-0.03s.gif","LoadGIF/frame_140_delay-0.03s.gif",
                    "LoadGIF/frame_141_delay-0.03s.gif","LoadGIF/frame_142_delay-0.03s.gif","LoadGIF/frame_143_delay-0.03s.gif",
                    "LoadGIF/frame_144_delay-0.03s.gif","LoadGIF/frame_145_delay-0.03s.gif","LoadGIF/frame_146_delay-0.03s.gif",
                    "LoadGIF/frame_147_delay-0.03s.gif","LoadGIF/frame_148_delay-0.03s.gif","LoadGIF/frame_149_delay-0.03s.gif",
                    "LoadGIF/frame_150_delay-0.03s.gif","LoadGIF/frame_151_delay-0.03s.gif","LoadGIF/frame_152_delay-0.03s.gif",
                    "LoadGIF/frame_153_delay-0.03s.gif","LoadGIF/frame_154_delay-0.03s.gif","LoadGIF/frame_155_delay-0.03s.gif",
                    "LoadGIF/frame_156_delay-0.03s.gif","LoadGIF/frame_157_delay-0.03s.gif","LoadGIF/frame_158_delay-0.03s.gif",
                    "LoadGIF/frame_159_delay-0.03s.gif","LoadGIF/frame_160_delay-0.03s.gif","LoadGIF/frame_161_delay-0.03s.gif",
                    "LoadGIF/frame_162_delay-0.03s.gif","LoadGIF/frame_163_delay-0.03s.gif","LoadGIF/frame_164_delay-0.03s.gif",
                    "LoadGIF/frame_165_delay-0.03s.gif","LoadGIF/frame_166_delay-0.03s.gif","LoadGIF/frame_167_delay-0.03s.gif",
                    "LoadGIF/frame_168_delay-0.03s.gif","LoadGIF/frame_169_delay-0.03s.gif","LoadGIF/frame_170_delay-0.03s.gif",
                    "LoadGIF/frame_171_delay-0.03s.gif","LoadGIF/frame_172_delay-0.03s.gif","LoadGIF/frame_173_delay-0.03s.gif",
                    "LoadGIF/frame_174_delay-0.03s.gif","LoadGIF/frame_175_delay-0.03s.gif","LoadGIF/frame_176_delay-0.03s.gif",
                    "LoadGIF/frame_177_delay-0.03s.gif","LoadGIF/frame_178_delay-0.03s.gif","LoadGIF/frame_179_delay-0.03s.gif"]


##We created a GIF for the GUI by taking a series of photos and put them all together in an array. When called for,
##we cycle the pictures with a delay ("time.sleep(0.05)") of 50 milliseconds. 
gifimagelist = ["MoveGIF/1.gif","MoveGIF/2.gif","MoveGIF/3.gif","MoveGIF/4.gif","MoveGIF/5.gif","MoveGIF/6.gif","MoveGIF/7.gif","MoveGIF/8.gif",
                "MoveGIF/9.gif","MoveGIF/10.gif","MoveGIF/11.gif","MoveGIF/12.gif","MoveGIF/13.gif","MoveGIF/14.gif","MoveGIF/15.gif","MoveGIF/16.gif",
                "MoveGIF/17.gif","MoveGIF/18.gif","MoveGIF/19.gif","MoveGIF/20.gif","MoveGIF/21.gif","MoveGIF/22.gif","MoveGIF/23.gif","MoveGIF/24.gif",
                "MoveGIF/25.gif"]


CameraModeGIFBackground = ["Spiral/Spiral (1).gif","Spiral/Spiral (2).gif","Spiral/Spiral (3).gif","Spiral/Spiral (4).gif"]
##Here is where we start defining a new window ("win") for our tkinter GUI. We set it up for a 1280x1024 resolution screen
##but in our code, if you just change the display width and height at the top, you can really use any size screen.
win = Tk()
win.geometry('%dx%d+0+0' % (displayWidth,displayHeight))#calibrate screen size for the GUI
win.title("Motion Synthesizer")
win.config(cursor='none')
bgColor = '#000d4d'#Background color for all the canvas'. It is a very dark blue defined in hexidecimal values.


SonicPiLoadingcanvas = Canvas(win, height=displayHeight, width=displayWidth,  bg=bgColor)
SonicPiloadingBackground = PhotoImage(file='SonicPiLoadingBackground.ppm')
SonicPiloadingBackgroundSize=[1280,1024]
SonicPiloadingTitle= PhotoImage(file='SonicPiLoadingTitle.ppm')
SonicPiloadingTitleSize=[936,147]
SonicPiloadingMessage = PhotoImage(file='SonicPiLoadingMessage.ppm')
SonicPiloadingMessageSize = [1102,173]
SonicPiinitialloadingGIF= PhotoImage(file='SonicPiLoadingInitialGIF.ppm')
SonicPiinitialloadingGIFSize = [560,173]
SonicPiLoadingcanvas.create_image((HalfDisplayWidth-(SonicPiloadingBackgroundSize[0]/2)),0,image=SonicPiloadingBackground, anchor='nw')
SonicPiLoadingcanvas.create_image((HalfDisplayWidth-(SonicPiloadingTitleSize[0]/2)),0,image=SonicPiloadingTitle, anchor='nw')
SonicPiLoadingcanvas.create_image((HalfDisplayWidth-(SonicPiloadingMessageSize[0]/2)),displayHeight/4,image=SonicPiloadingMessage, anchor='nw')
loadGIFimager = SonicPiLoadingcanvas.create_image((HalfDisplayWidth-(SonicPiinitialloadingGIFSize[0]/2)),displayHeight*3/4,image=SonicPiinitialloadingGIF, anchor='nw')
SonicPiLoadingcanvas.pack()#Pack the canvas so it displays on the screen
win.update()

loadGIF = [] #We cycle through all the GIF images making a loop to show the GIF video. 
loadGIFSize = [200,200]
for imfile in loadgifimagelist:
    GIFphoto = PhotoImage(file=imfile)# Convert All GIF images into "PhotoImage" for Tkinter, and load them into an array. 
    loadGIF.append(GIFphoto)
    

LoadingCount = 0
while LoadingCount < 30:
    LoadingCount += 1
    for giff in loadGIF:  #Loop the GIF images to create the viseo displayed in the GUI.
        SonicPiLoadingcanvas.delete(loadGIFimager)#Start by deleting the previous GIF image.
        loadGIFimager = SonicPiLoadingcanvas.create_image((HalfDisplayWidth-(loadGIFSize[0]/2)),displayHeight*3/4,image=giff, anchor='nw')
        SonicPiLoadingcanvas.update()#Put the next GIF image on the screen.
        win.update()
        win.lift()
        time.sleep(0.005)


SonicPiLoadingcanvas.destroy()
##We need to define which pictures are on the 'HOME' screen. We also convert them into PhotoImages because tkinter
##needs to keep a reference of each photo. The picture formats that are accepted by the tkinter canvas widget  are
##".ppm" and ".gif". We used an online image converting tool to convert ".png" and ".jpeg" to the formats specified. 
HomeBackground = PhotoImage(file='Background.ppm')
HomeBackgroundSize = [1280,1024]#We need the size of each picture so that they can be placed on the GUI according to the screen's resolution.
titlemessage = PhotoImage(file='Title.ppm')#Change all images to "PhotoImage" for the Tkinter GUI.
titlemessageSize=[920,185]
devicephoto = PhotoImage(file='Device.ppm')
devicePhotoSize = [659,399]
startinstruction = PhotoImage(file='Startinstruction.ppm')
startinstructionSize=[664,219]
can1 = Canvas(win, height=displayHeight, width=displayWidth,  bg=bgColor)#Creating the Home canvas and then putting all the images on it.
can1.create_image((HalfDisplayWidth-(HomeBackgroundSize[0]/2)),0,image=HomeBackground, anchor='nw')#using the specified screen resolution, we determine where each image will go.
can1.create_image((HalfDisplayWidth-(titlemessageSize[0]/2)),0,image=titlemessage, anchor='nw')
can1.create_image((HalfDisplayWidth-(devicePhotoSize[0]/2)), displayHeight/4,image=devicephoto, anchor='nw')
startinst = can1.create_image((HalfDisplayWidth-(startinstructionSize[0]/2)),displayHeight*3/4,image=startinstruction, anchor='nw')
can1.pack()#Pack the canvas so it displays on the screen
win.update()#update the window to activate the updates made the the GUI's window. Display the Home screen.
#win.lift()

##Now that the home screen is set up, the next while loop is to flash and image on and off by settign its state to "hidden" and then
##"normal" again. This is to catch the attention of the user so that their eyes are drawn to the instructions to start the Synthesizer.
flashinstartinstcount = 0
while GPIO.input(ModeChangeButton)== 1:
    flashinstartinstcount += 1
    if flashinstartinstcount > 4000:
        can1.itemconfigure(startinst, state='hidden')
        flashinstartinstcount += 1
    if flashinstartinstcount > 5500:
        can1.itemconfigure(startinst, state='normal')
        flashinstartinstcount = 0
    
    win.update()#keep updating the window for any changes that someone makes with a mouse. A mouse should not be used,
                #but in the case someone does use one, the screen stays updated if they manipulate the screen.



##If the user presses the Middle Mode Change button, we are nopw ready to leave the start menu and to move on to the actual
##music system. Here we are dbouncing the switch so that we can wait untill the user releases the switch before moving on.
####   ACTIVE LOW SWITCHES!
time.sleep(0.3)#Debounce mechanical switch.
while GPIO.input(ModeChangeButton)== 0:#Wait for the switch to be released.
    pass
time.sleep(0.3)#Debounce the switch release.

can1.destroy()    #Clear the screen for the ultrasonic Music Mode. Gets rid of the Home canvas.
    
while True:
    
    
    
    

    #Here we are setting up the Ultrasonic music mode Canvas.
    ultracan = Canvas(win, height=displayHeight, width=displayWidth,  bg=bgColor)#Dimesnions of the canvas are all based on the screens resolution.
    ultrabackground = PhotoImage(file='UltraBackground.ppm')#Background Image
    ultraBackgroundSize = [1280,1024]
    ultraTitle = PhotoImage(file='UltraTitle.ppm')
    ultraTitleSize = [920,185]
    ultraMessage = PhotoImage(file='UltraMessage.ppm')
    ultraMessageSize = [955,194]
    gifBorder = PhotoImage(file='gifBorder.ppm')#For the Ultrasonic sensor GUI uses a GIF, all the GIF frames are located in one folder.
    gifBorderSize = [624,377]
    initialultraGif = PhotoImage(file='MoveGIF/1.gif')
    initialultraGifSize = [568,320]

    #Put all the images on the Ultrasonic music canvas.
    ultracan.create_image((HalfDisplayWidth-(ultraBackgroundSize[0]/2)),0,image=ultrabackground, anchor='nw')
    ultracan.create_image((HalfDisplayWidth-(gifBorderSize[0]/2)),((displayHeight*3/4)-(gifBorderSize[1]/2)),image=gifBorder, anchor='nw')
    gifimage = ultracan.create_image((HalfDisplayWidth-(initialultraGifSize[0]/2)),(displayHeight*3/4)-(initialultraGifSize[1]/2),image=initialultraGif, anchor='nw')#Start witht the first GIF image.
    ultracan.create_image((HalfDisplayWidth-(ultraTitleSize[0]/2)),0,image=ultraTitle, anchor='nw')
    ultracan.create_image((HalfDisplayWidth-(ultraMessageSize[0]/2)),displayHeight/4,image=ultraMessage, anchor='nw')
    ultracan.pack()#Show ultra canvas.
    win.update()#Update the GUI window. 

    
    Ultra = subprocess.Popen(['python3', './Ultra.py'])#Open the ultrasonic music mode
    
    UltraGIF = [] #We cycle through all the GIF images making a loop to show the GIF video. 
    GIFSize = [568,320]
    for imagefile in gifimagelist:
        photo = PhotoImage(file=imagefile)# Convert All GIF images into "PhotoImage" for Tkinter, and load them into an array. 
        UltraGIF.append(photo)
        
    while GPIO.input(ModeChangeButton)== 1:#loop thisn until the next button press (ModeChangeButton or HelpMenu button).
        for gif in UltraGIF:  #Loop the GIF images to create the viseo displayed in the GUI.
            ultracan.delete(gifimage)#Start by deleting the previous GIF image.
            gifimage = ultracan.create_image((HalfDisplayWidth-(GIFSize[0]/2)),((displayHeight*3/4)-(GIFSize[1]/2)),image=gif, anchor='nw')
            ultracan.update()#Put the next GIF image on the screen. 
            win.update()
            if GPIO.input(ModeChangeButton)== 0 or GPIO.input(HelpMenu)== 0:
                break 
            time.sleep(0.05)#delay for each of the GIF images. Makes a smooth video. Not too fast or not too slow.
        if GPIO.input(HelpMenu)== 0:
            help=True#Boolean used to indicate the user has pressed the helpMenu button.
            break
        
    file = open("test.txt", "w")
    file.write("2") #stops ultrasonic mode properly and releases necessary GPIO pins. The camera mode can now run without interfence.
    file.close()
    
    time.sleep(0.3)#debounce the switches and wait until the user releases them to continue.
    while GPIO.input(HelpMenu)== 0:
        pass
    time.sleep(0.3)
    while GPIO.input(ModeChangeButton)== 0:
        pass
    time.sleep(0.3)
    
    ultracan.destroy()#Destroy the Ultramusic canvas and make room for the next.
    if help is True:# If the user hit the help button, the help menu will display until the user presses the help mode button again. 
        helpcanvas = Canvas(win, height=displayHeight, width=displayWidth,  bg=bgColor)
        helpPhoto = PhotoImage(file='HelpMenu.ppm')
        helpPhotoSize=[1256,976]
        helpcanvas.create_image((HalfDisplayWidth-(helpPhotoSize[0]/2)),0,image=helpPhoto, anchor='nw')
        helpcanvas.pack()
        while GPIO.input(HelpMenu)== 1:
            helpcanvas.update()
            win.update()#continually update the GUI window while waiting for the user to exit the Menu screen.
            pass
        time.sleep(0.3)#Debounce
        help = False# reset the help Bool for the next time a user presses the button.
        helpcanvas.destroy()#Destroy the Help canvas for the next canvas.
    
        
    #Camera mode, setting up all images and the canvas for the GUI.
    #The camera needs to load up and so when the User presses the button to change into this mode, the screen must display a "Please Wait" message.
    cameracan = Canvas(win, height=displayHeight, width=displayWidth,  bg=bgColor)
    camerabackground = PhotoImage(file='Spiral/Spiral (1).gif')
    cameraBackgroundSize = [1280,1024]
    cameraTitle = PhotoImage(file='CameraTitle.ppm')
    cameraTitleSize = [920,185]
    cameraPleaseWait = PhotoImage(file='CameraPleaseWait.ppm')
    cameraPleaseWaitSize = [522,256]
    cameraBack = cameracan.create_image((HalfDisplayWidth-(cameraBackgroundSize[0]/2)),0,image=camerabackground, anchor='nw')
    camTitle = cameracan.create_image((HalfDisplayWidth-(cameraTitleSize[0]/2)),0,image=cameraTitle, anchor='nw')
    plzwait = cameracan.create_image((HalfDisplayWidth-(cameraPleaseWaitSize[0]/2)),(HalfDisplayHeight-(cameraPleaseWaitSize[1]/2)),image=cameraPleaseWait, anchor='nw')
    cameracan.pack()
    win.update()
    
    
    CameraMode = subprocess.Popen(['python3', './CameraMode.py']) #Run the Camera Mode subprocess.
    
    CamGIF = [] #We cycle through all the GIF images making a loop to show the GIF video. 
    CamGIFSize = [1280,1024]
    
    for imagefile in CameraModeGIFBackground:
        photo = PhotoImage(file=imagefile)# Convert All GIF images into "PhotoImage" for Tkinter, and load them into an array. 
        CamGIF.append(photo)
    
        
    while GPIO.input(ModeChangeButton)== 1:#loop until the next mode is requested.
        for cameragif in CamGIF:  #Loop the GIF images to create the viseo displayed in the GUI.
            cameracan.delete(camerabackground)#Start by deleting the previous GIF image.
            cameracan.delete(camTitle)
            cameracan.delete(plzwait)
            camerabackground = cameracan.create_image((HalfDisplayWidth-(CamGIFSize[0]/2)),0,image=cameragif, anchor='nw')
            plzwait = cameracan.create_image((HalfDisplayWidth-(cameraPleaseWaitSize[0]/2)),(HalfDisplayHeight-(cameraPleaseWaitSize[1]/2)),image=cameraPleaseWait, anchor='nw')
            camTitle = cameracan.create_image((HalfDisplayWidth-(cameraTitleSize[0]/2)),0,image=cameraTitle, anchor='nw')

            cameracan.update()#Put the next GIF image on the screen. 
            win.update()
            if GPIO.input(ModeChangeButton)== 0 or GPIO.input(HelpMenu)== 0:
                break 
            #time.sleep(0.0005)#delay for each of the GIF images. Makes a smooth video. Not too fast or not too slow.
        if GPIO.input(HelpMenu)== 0:
            help=True#Boolean used to indicate the user has pressed the helpMenu button.
            break
    
    
    file = open("test.txt", "w")
    file.write("1") #Stops Camera mode properly, and releases the camera for use in the future. 
    file.close()
    
    time.sleep(0.3)#debounce the switches and wait for the user to release the button to continue.
    while GPIO.input(HelpMenu)== 0:
        pass
    time.sleep(0.3)
    while GPIO.input(ModeChangeButton)== 0:
        pass
    time.sleep(0.3)
    
    cameracan.destroy()#Destroy the camera mode canvas.
    
    if help is True: # If the help button was pressed, show the help menu until they hit the button again to escape.
        helpcanvas = Canvas(win, height=1024, width=1280,  bg=bgColor)
        helpPhoto = PhotoImage(file='HelpMenu.ppm')
        helpPhotoSize=[1256,976]
        helpcanvas.create_image((HalfDisplayWidth - (helpPhotoSize[0]/2)),0,image=helpPhoto, anchor='nw')
        helpcanvas.pack()
        while GPIO.input(HelpMenu)== 1:
            helpcanvas.update()
            win.update()
            pass
        time.sleep(0.3)
        help = False
        helpcanvas.destroy()



