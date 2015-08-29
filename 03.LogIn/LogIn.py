import  pandas as pd
import  matplotlib.pyplot as plt
import  sys
import  win32com.client
import  pythoncom 
import  time
from    weakref import proxy

# SERVER VAR
DEMOSERVER = 'demo.etrade.co.kr'
PORT = 20001

# ACCOUNT VAR
ID = "userid"
PW = "passwd"
CERT_PW =""


class XASessionEvents:
    logInState = False
    def OnLogin(self, code, msg):
        print("OnLogin: " + " Code:" + str(code) + " Msg:" + str(msg))
        if str(code) == '0000':
            XASessionEvents.logInState = True

    def OnLogout(self):
        print("OnLogout method is called")

    def OnDisconnect(self, *args):
        print("OnDisconnect method is called")
        print(args)


class XASession():
    def __init__(self):
        self.event = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
        self.event.parent = proxy(self)

    def ConnectServer(self, server, port):
        self.event.ConnectServer(server, port)

    def Login(self, user, password, certpw, servertype = 0, showcerterror = 1):
        self.event.Login(user,password,certpw,servertype,showcerterror)
        while self.event.logInState == False: #wait util logInState is True
            pythoncom.PumpWaitingMessages()

        
if __name__ == '__main__':
    #--------------------------------------------------------------------------
    # Login Session
    #--------------------------------------------------------------------------
    XServer = XASession()
    XServer.ConnectServer(DEMOSERVER, PORT)
    XServer.Login(ID, PW, CERT_PW)
   