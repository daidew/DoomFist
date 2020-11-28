import random
import pyautogui as pg
import threading
import time
import numpy as np
import ctypes
from ctypes import *
from sklearn.neural_network import MLPClassifier
from joblib import dump,load
import pickle
import itertools
pg.FAILSAFE = False

defaultdict = {'gx':0.0,'gy':0.0,'gz':0.0,'ax':0.0,'ay':0.0,'az':0.0}
defaultlist = [0.0 for i in range(5)]
class AIdata:
        def __init__(self):
                self.mCap = 5 #change size here
                self.mSize = 0
                self.mData = [defaultlist for i in range(5)]
        def __len__(self):
                return len(self.mData)

        def update(self,data):
                result = []
                for key in defaultdict.keys():
                        result.append(data[0][key])
                self.mData.insert(0,result)
                self.mData.pop()
                if self.mSize != self.mCap: self.mSize += 1
                return
        def reset(self):
                self.mData = [defaultlist for i in range(5)]
                self.mSize = 0
                return

        def isReady(self):
                return self.mSize == self.mCap

        def __getitem__(self,key):
                return self.mData[key]
        def determineClass(self):
                clf = load('model.joblib')
                X_test = [list(itertools.chain.from_iterable(self.mData))]
                Y_pred = clf.predict(X_test)
                return Y_pred[0]


class data:
        def __init__(self):
                self.mData = [0]
                #for i in range(10): self.mData.append({})

        def update(self,ax,ay,az,gx,gy,gz,touch,b1,up,down,left,right):
                self.mData[0] = {'gx':float(gx),'gy':float(gy),'gz':float(gz),'ax':float(ax),'ay':float(ay),'az':float(az),'touch':touch,'b1':b1,'up':up,'down':down,'left':left,'right':right}
                

                #self.mFront+=1
                return



        def __getitem__(self,key):
                return self.mData[0]

        def __len__(self):
                return len(self.mData)

        #debug

        def fakeUpdate(self):
                self.mData[0] = {'gx':random.random(),'gy':random.random()
                        ,'gz':random.random(),'ax':random.random(),'ay':random.random()
                        ,'az':random.random(),'touch':True,'b1':True
                        ,'up':False,'down':False,'left':False,'right':False}
        
                return


        def __str__(self):
                return str(self.mData)



#-----------------------------------------------------------------------------------------------------------------------------------#
thrsh = 20
mlt = 1.6
comp = -32

def moveMouseRel(xOffset, yOffset):
        #ctypes.windll.user32.mouse_event(0x0001, xOffset, yOffset, 0, 0)
        tx = threading.Thread(target = __mmx__, args = (xOffset,))
        ty = threading.Thread(target = __mmy__, args = (yOffset,))
        tx.start()
        ty.start()

def __mmx__(xOffset):
        spd = xOffset//5
        for i in range(5):
                ctypes.windll.user32.mouse_event(0x0001, spd, 0, 0, 0)
                time.sleep(0.01)

def __mmy__(yOffset):
        spd = yOffset//5
        for i in range(5):
                ctypes.windll.user32.mouse_event(0x0001, 0, spd, 0, 0)
                time.sleep(0.01)


class processor:
        def __init__(self,data):
                self.mData = data;
                self.aiData = AIdata();
                self.state = 0;

                self.isPushed = {'touch':False, 'b1':False,'up':False,'down':False,'left':False,'right':False};


        #------------------------------------update---------------------------------------

        def update(self):

                if(self.state == 0):
                        if(self.mData[0]['touch']=='1'):
                                self.aiData.reset() ###ai
                                self.state = 1
                        #self.cursor_process()
                        self.fire_process()
                        

                elif(self.state == 1):
                        self.aiData.update(self.mData) ###ai
                        action = 0
                        if(self.aiData.isReady()): action = self.aiData.determineClass()
                        if(self.state == 1 and self.mData[0]['touch']=='0'): self.state = 0 #if untouch goback to state 0
                        
                        elif(self.slam_process(action)):
                                self.aiData.reset() ###ai
                                self.state = 0
                        elif(self.uppercut_process(action)):
                                self.aiData.reset() ###ai
                                self.state = 0
                        elif(self.charge_init_process(action)):
                                self.aiData.reset() ###ai
                                self.state = 2


                
                elif(self.state == 2):
                        self.aiData.update(self.mData) ###ai

                        if(self.charge_release_process()): 
                                self.aiData.reset() ###ai
                                self.state = 0
                        #self.cursor_process()
                
                self.walk_process()
                print(self.state)
                
                return


        

#------------------------------------process---------------------------------------
        def slam_process(self,action):
                if(action == 1):
                        print("slam")
                        pg.keyDown('e')
                        pg.keyUp('e')
                        return True
                return False

        def uppercut_process(self,action):
                if(action == 3):
                        print("uppercut")
                        pg.keyDown('shiftleft')
                        pg.keyUp('shiftleft')
                        return True
                return False

        def charge_init_process(self,action):

                if(action == 2):
                        print("charge")
                        pg.mouseDown(button = 'right')
                        return True
                return False

        def charge_release_process(self):
                print('release')
                return True
        def not_moving_process(self,action):
                if(action == 0):
                        print('not moving')
                        return True
                return False


        # def  meteor_strike_process(self):

        #       return

        def cursor_process(self):
                move = False
                yspd = 0
                xspd = 0
                gx = self.mData[0]['gx']
                gz = self.mData[0]['gz']
                if(gx > thrsh):
                        yspd = -mlt*(gx)-comp
                        move = True
                elif(gx < -thrsh):
                        yspd = -mlt*(gx)+comp
                        move = True
                if(gz > thrsh):
                        xspd = -mlt*(gz)-comp
                        move = True
                elif(gz < -thrsh):
                        xspd = -mlt*(gz)+comp
                        move = True
                if(move): pg.moveTo(int(xspd),int(yspd))

                return

        def fire_process(self):
                if(self.isButtonDown('b1')): pg.mouseDown(button = 'left')
                elif(self.isButtonUp('b1')): pg.mouseUp(button = 'left')
                return

        def walk_process(self):
                if(self.isButtonDown('left')): pg.keyDown('left')
                elif(self.isButtonUp('left')): pg.keyUp('left')

                if(self.isButtonDown('right')): pg.keyDown('up')
                elif(self.isButtonUp('right')): pg.keyUp('up')

                if(self.isButtonDown('up')): pg.keyDown('up')
                elif(self.isButtonUp('up')): pg.keyUp('up')

                if(self.isButtonDown('down')): pg.keyDown('left')
                elif(self.isButtonUp('down')): pg.keyUp('left')

                return
#------------------------------------button check---------------------------------------

        def isButtonDown(self,button):
                if(self.mData[0][button] == '1' and self.isPushed[button] == False):
                        self.isPushed[button] = True
                        return True
                return False
        def isButtonUp(self,button):
                if(self.mData[0][button] == '0' and self.isPushed[button] == True):
                        self.isPushed[button] = False
                        return True
                return False;
        def isPress(self,Button):
                return self.mData[0][button] == '1'

        #debug
        def printfirst(self):
                print(self.mData[0])
                return

        def realtimeUpdate(self):
                self.isButtonDown('b1')
                if():
                        print("Ax:"+str(self.mData[0]['ax'])+" Ay:"+str(self.mData[0]['ay'])+" Az:"+str(self.mData[0]['az'])+" Gx:"+str(self.mData[0]['gx'])+" Gy:"+str(self.mData[0]['gy'])+" Gz:"+str(self.mData[0]['gz']))
                if(self.isButtonUp('b1')):
                        print("------------------end------------------")
                return
        def getSample(self):
                result = ''
                self.isButtonDown('touch')
                if(self.mData[0]['touch'] == '1'):
                    for key in defaultdict.keys():
                        result += str(self.mData[0][key]) + " "
                    print(result)
                if(self.isButtonUp('touch')):
                    print("--------------end----------------")

## main
