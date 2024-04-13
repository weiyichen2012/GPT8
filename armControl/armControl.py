import requests
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtGui, QtWidgets
import time
from threading import Thread
import os

def postRequest(url, cmd):
    r = requests.post(url, json = cmd).json()
    return r

class ArmControlRunner():
    def __init__(self, baseDir, ifDebug = True):
        self.baseDir = baseDir
        self.selfBaseDir = baseDir + '/armControl/'
        self.ifDebug = ifDebug
        self.url = "http://127.0.0.1:9030/jsonrpc"
        self.cmd = {
            "method":"",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
            }
        initPos = [500, 500, 388, 871, 150, 500]
        self.currentPos = initPos
        self.moveArm(1000, initPos)

    def getArmPos(self):
        return self.currentPos

    def moveSingleServo(self, time, servoId, servoPulse):
        self.cmd["method"] = "SetBusServoPulse"
        self.cmd["params"] = [time, 1]
        self.cmd["params"].append(servoId)
        self.cmd["params"].append(servoPulse)
        self.currentPos[servoId - 1] = servoPulse
        r = postRequest(self.url, json = self.cmd).json()
        if self.ifDebug:
            print(self.cmd)
            print(r)

    def moveArm(self, time, servoPulse):
        self.cmd["method"] = "SetBusServoPulse"
        self.cmd["params"] = [time, 6]
        for i in range(0, 6):
            self.cmd["params"].append(i + 1)
            self.cmd["params"].append(servoPulse[i])
            self.currentPos[i] = servoPulse[i]
        r = postRequest(self.url, json = self.cmd).json()
        if self.ifDebug:
            print(self.cmd)
            print(r)

    def moveArmAction(self, action):
        self.moveArm(action['time'], action['servoPulse'])
    
    def actionRunner(self, actionList):
        for action in actionList:
            self.moveArmAction(action)
            time.sleep(action['time'] / 1000.0)

    def moveArmActionList(self, actionList):
        # self.actionRunner(actionList)
        self.actionThread = Thread(target = self.actionRunner, args = (actionList,))
        if self.ifDebug:
            print("thread start")
        self.actionThread.start()
    
    def waitActionFinish(self):
        self.actionThread.join()
        if self.ifDebug:
            print("thread join")
    
    def readArmFile(self, fileName):
        path = self.selfBaseDir + fileName
        actionList = []
        rbt = QSqlDatabase.addDatabase("QSQLITE")
        if os.path.exists(path):
            rbt.setDatabaseName(path)
            if rbt.open():
                actgrp = QSqlQuery()
                if (actgrp.exec("select * from ActionGroup ")):
                    while (actgrp.next()):
                        servoPulse = []
                        time = actgrp.value(1)                    
                        for i in range(2, 8):
                            servoPulse.append(actgrp.value(i))
                        action = {'time': time, 'servoPulse': servoPulse}
                        if self.ifDebug:
                            print(action)
                        actionList.append(action)
        else:
            print("Error in readArmFile, path doesn't exist.")
        rbt.close()
        if self.ifDebug:
            print(actionList)
        return actionList

if __name__ == "__main__":
    armControlRunner = ArmControlRunner()
    armControlRunner.moveArmActionList(armControlRunner.readArmFile("reset.d6a"))
