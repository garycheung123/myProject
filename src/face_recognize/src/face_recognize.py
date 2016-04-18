#!/usr/bin/env python
# coding=utf-8

import roslib
import rospy
import cv2
import json
import sys
import re
import numpy
import time
import math
import random
import ImageTk
import vision_definitions
import tkFileDialog
import os , shutil , glob
import Image as Im
import threading
from random import randint
from std_srvs.srv import Empty
from Tkinter import *
from std_msgs.msg import String
from nao_interaction_msgs.msg import FaceDetected
from sensor_msgs.msg import Image, Range
from cv_bridge import CvBridge, CvBridgeError
from naoqi_driver.naoqi_node import NaoqiNode
from naoqi import (ALBroker, ALProxy, ALModule)
from nao_interaction_msgs.srv import (LearnFace, LearnFaceResponse)


class Speech(NaoqiNode):

    def __init__(self):

        self.destination = os.getcwd()
        self.params = list()
        self.params.append(cv2.cv.CV_IMWRITE_PNG_COMPRESSION)
        self.params.append(8)
        self.spokenName = {}

        self.notes = { 0:" Hello " , 1:" 好耐冇見呀 " , 2:" 你好 " }
        self.language = { 0:"English" , 1:"CantoneseHK" , 2:"Chinese" }
        self.string = { 0:{ 0:" Welcome to Bank of China " } , 1:{ 0:" 歡迎來臨中國銀行 " , 1:" 中國銀行歡迎你 " } , 2:{ 0:" 歡迎來臨中國銀行 " , 1:" 中國銀行歡迎你 " } }

    	# init nao node
        NaoqiNode.__init__(self, 'face_recognize')
        self.connectNaoQi()
        self.tts.setParameter("doubleVoiceTimeShift", 0.5)
        # subscribe camera
        self.image_sub = rospy.Subscriber("/nao_robot/camera/top/camera/image_raw",Image,self.cameraCallBack)

        # subscribe face detection
        self.faceDetect = rospy.Subscriber("nao_vision/faces_detected",FaceDetected,self.faceDetected)
        # enable face track
        #self.aLTrackerProxy.registerTarget('Face', 0.1)
        #self.aLTrackerProxy.track('Face')

        # enable Autonomous Life
        self.aLAutonomousLifeProxy.setState('solitary')
        #self.aLAutonomousLifeProxy.switchFocus('interactive')
        self.aLSpeechRecognitionProxy.setAudioExpression(False)
        self.aLSpeechRecognitionProxy.setVisualExpression(False)

        # init face name
        self.recordedFaces = self.faceDetectionProxy.getLearnedFacesList()
        rospy.loginfo(self.recordedFaces)
        self.recordedFaces = [ k.split('--')[0] for k in self.recordedFaces ]

        self.printit()

        # python gui
        self.dir_opt = options = {}
        self.root = Tk()
        self.inputbox = Entry()
        self.inputbox.place(x=10,y=10)
        Button(text="Learn",command=self.facefrontLearn).place(x=10,y=40)
        '''Button(text="Learn left",command=self.faceleftLearn).place(x=110,y=40)
        Button(text="Learn right",command=self.facerightLearn).place(x=10,y=70)
        Button(text="Clear dict",command=self.clearDict).place(x=110,y=70)'''
        self.inputboxRemove = Entry()
        self.inputboxRemove.place(x=10,y=80)
        Button(text="Forget",command=self.faceDelete).place(x=10,y=110)
        Button(text="Forget All",command=self.faceDeleteAll).place(x=10,y=140)
        Button(text='Directory', command=self.askdirectory).place(x=10,y=170)
        self.directoryLabel = Label(self.root, text=self.destination)
        self.directoryLabel.place(x=10,y=200)

        self.voiceVolumnv = Scale(self.root, label="voiceVolumn", from_=0, to=100, length=150, resolution=5,tickinterval=5, orient=HORIZONTAL ,command=self.voiceVolumn)
        self.voiceVolumnv.set(self.aLAudioDevice.getOutputVolume())
        self.voiceVolumnv.place(x=10,y=230)

        self.panel = Label(self.root)
        self.panel.place(x=520,y=0)
        self.camera = Label(self.root)
        self.camera.place(x=200,y=0)
        self.root.geometry("840x240")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def printit(self):
        threading.Timer(1.0, self.printit).start()
        self.spokenName = { k:v-1 for k,v in self.spokenName.iteritems() }
        self.spokenName = { x:y for x,y in self.spokenName.items() if y!=0}

    def voiceVolumn(self,event):
        self.aLAudioDevice.setOutputVolume(self.voiceVolumnv.get())

    def connectNaoQi(self):
        self.motionProxy = self.get_proxy("ALMotion")
        self.tts = self.get_proxy("ALTextToSpeech")
        self.faceDetectionProxy = self.get_proxy("ALFaceDetection")
        self.getImageProxy = self.get_proxy("ALVideoDevice")
        self.aLSpeechRecognitionProxy = self.get_proxy("ALSpeechRecognition")
        self.aLTrackerProxy = self.get_proxy("ALTracker")
        self.aLAutonomousLifeProxy = self.get_proxy("ALAutonomousLife")
        self.aLAudioDevice = self.get_proxy("ALAudioDevice")
        if self.motionProxy is None or self.tts is None or self.faceDetectionProxy is None or self.getImageProxy is None or self.aLTrackerProxy is None or self.aLAutonomousLifeProxy is None :
            exit(1)

        self.bridge = CvBridge()

        resolution = vision_definitions.kQVGA
        colorSpace = vision_definitions.kBGRColorSpace

        self.nameId = self.getImageProxy.subscribe("python_client", resolution, colorSpace, 5)

    def faceDetected(self,data):
        #rospy.loginfo(self.recordedFaces)
        if( data.score_reco.data < 0.6 ):
            return

        name = data.face_label.data
        #stringPos = name.index('--')
        #name = name[:(stringPos)]
        #rospy.loginfo(name)

        if name not in self.spokenName:
            #rospy.loginfo(name)
            chineseCheck = re.findall(ur'[\u4e00-\u9fff]+', name.decode('utf-8'))
            #rospy.loginfo(chineseCheck)
            if len(chineseCheck) > 0 :
                lang = randint(1,2)
            else :
                lang = randint(0,2)

            speech = randint(0,2)

            self.tts.setLanguage(self.language[lang])
            self.aLSpeechRecognitionProxy.setAudioExpression(False)
            # init speech speed
            greet = self.notes[lang] if speech > 1 else self.getGreet(lang)

            if '--' in name: 
                speakName = name[:name.index('--')]
            else:
                speakName = name

            self.tts.say("\\rspd=90\\"+greet+speakName+self.string[lang][speech % len(self.string[lang])] + ",,,,,,,,,,,")
            self.logFile('see',[name])

        self.spokenName[name] = 8

    def facefrontLearn(self):
        self.faceLearn('--front')
    def faceleftLearn(self):
        self.faceLearn('--left')
    def facerightLearn(self):
        self.faceLearn('--right')

    def getGreet(self,lang):
        currentTime = int(time.strftime('%H:%M').split(':')[0])   

        greet = { 0:{ 0:'Good morning',1:'Good afternoon',2:'Good evening' }, 1:{ 0:'早上好',1:'下午好',2:'晚上好' } , 2:{ 0:'早安',1:'午安',2:'晚安' } }

        if currentTime < 12 :
            return greet[lang][0]
        if currentTime >= 12 :
            return greet[lang][1]
        if currentTime > 6 :
            return greet[lang][2]

    def faceLearn(self,face):

        # no check side face 
        face = ''

        data = self.inputbox.get() 
        cache = data
        data = data.encode('utf-8')
        encodedCache = data

        rospy.loginfo(self.recordedFaces)
        rospy.loginfo(data)

        if data in self.recordedFaces:
            data = data + '--' + str(self.recordedFaces.count(data))

        rospy.loginfo(data)  

        if( self.faceDetectionProxy.learnFace(data+face) ):
            self.recordedFaces.append(encodedCache)
            dataImage = self.getImageProxy.getImageRemote(self.nameId)
            image = (numpy.reshape(numpy.frombuffer(dataImage[6], dtype='%iuint8' % dataImage[2]), (dataImage[1], dataImage[0], dataImage[2])))

            folderName = cache[0]

            if not os.path.exists(folderName):
                os.makedirs(folderName)

            imagePathList = [self.destination,'/FaceRecord/',folderName,'/',data.decode('utf-8'),'.png']
            imagePath = ''.join(x.encode('utf-8') for x in imagePathList)

            cv2.imwrite(imagePath,image,self.params)

            imgTk=PhotoImage(file=imagePath)

            self.panel.configure(image=imgTk)
            self.panel.image = imgTk

            self.logFile('learn',[data])

        time.sleep(0.05)

    def clearDict(self):
        self.spokenName.clear()

    def faceDelete(self):
        data = self.inputboxRemove.get().strip()
        data = data.encode('utf-8')

        if data:
            self.faceDetectionProxy.forgetPerson(data)
            self.backUpDelete(data);

        if '--' in data: 
            data = data[:data.index('--')]

        self.recordedFaces.remove(data);

    def faceDeleteAll(self):
        self.recordedFaces = []
        self.faceDetectionProxy.clearDatabase()
        self.backUpDelete('all');

    def logFile(self,action,customer):
        logStatement = "[%s ~ %s] System %s %s customer(s) named %s" % ( time.strftime("%d-%m-%Y") , time.strftime("%H:%M:%S") , action , len(customer) , ' , '.join(customer) )
        if not os.path.exists(self.destination+'/FaceRecord/logRecord.txt'):
            os.mknod(self.destination+'/FaceRecord/logRecord.txt')
        target = open(self.destination+'/FaceRecord/logRecord.txt', 'ab')
        target.write(logStatement)
        target.write("\n")
        target.close()

    def backUpDelete(self,data):

        allFile = os.listdir(self.destination+'/FaceRecord')
        if 'deleteRecord' in allFile :
            allFile.remove('deleteRecord')
        if 'logRecord.txt' in allFile :
            allFile.remove('logRecord.txt')

        if len(allFile) == 0 :
            return

        folderName = data.decode('utf-8')
        folderName = folderName[0]

        timeFolder = self.destination+'/FaceRecord/deleteRecord/'+time.strftime("%d-%m-%Y")+'/'+time.strftime("%H:%M:%S")

        Folder = timeFolder +'/'+ folderName

        imageFile = [self.destination,'/FaceRecord/',folderName,'/',data.decode('utf-8'),'.png']
        imageFile = ''.join(x.encode('utf-8') for x in imageFile)

        destinationFile = [timeFolder,'/',folderName,'/',data.decode('utf-8'),'.png']
        destinationFile = ''.join(x.encode('utf-8') for x in destinationFile)

        if data != 'all':
            self.logFile('delete',[data])
            if not os.path.exists(Folder):
                os.makedirs(Folder)

            os.rename( imageFile , destinationFile )
            if not os.listdir(self.destination+'/FaceRecord/'+folderName) : 
                os.rmdir(self.destination+'/FaceRecord/'+folderName)
        else:
            customer = []
            self.logFile('delete',customer)
            if not os.path.exists(timeFolder):
                os.makedirs(timeFolder)
            for folder in allFile :
                if not os.path.exists(timeFolder + '/' + folder):
                    customerList = os.listdir(self.destination+'/FaceRecord/'+ folder)
                    customerList = [ x.replace('.png','') for x in customerList ]
                    customer.extend(customerList)
                    shutil.copytree( self.destination+'/FaceRecord/'+ folder , timeFolder + '/' + folder )
                else :
                    for filename in glob.glob(os.path.join( self.destination+'/FaceRecord/'+ folder , '*.*')):
                        shutil.copy(filename, timeFolder + '/' + folder )
                shutil.rmtree( self.destination+'/FaceRecord/'+ folder )

    def askdirectory(self): 
        dialogReturn = tkFileDialog.askdirectory(**self.dir_opt)
        if dialogReturn:
            self.destination = dialogReturn
            self.directoryLabel.config(text=self.destination)
            os.chdir(self.destination)
            if not os.path.exists('FaceRecord'):
                os.makedirs('FaceRecord')
            os.chdir(self.destination+'/FaceRecord')

    def cameraCallBack(self,dataImage):
        cv_image = self.bridge.imgmsg_to_cv2(dataImage, "bgr8")
        b,g,r = cv2.split(cv_image)
        cv_image = cv2.merge((r,g,b))
        im = Im.fromarray(cv_image)
        imgtk = ImageTk.PhotoImage(image=im)
        self.camera.configure(image=imgtk)
        self.camera.image = imgtk

    def on_closing(self):
        
        self.image_sub.unregister()
        rospy.sleep(1)

        self.faceDetect.unregister()
        rospy.sleep(1)      

        self.aLAutonomousLifeProxy.setState('disabled')

        self.root.destroy()

if __name__ == '__main__':
    try:
        Speech()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("face_recognize node terminated.")