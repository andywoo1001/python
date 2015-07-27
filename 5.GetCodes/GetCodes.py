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

class XAQueryEvents:
    queryState = False
    def OnReceiveData(self, szTrCode):
        #print("OnReceiveData: " + str(szTrCode))
        XAQueryEvents.queryState = True

    def OnReceiveMessage(self, bIsSystemError,szMessageCode,szMessage ):
        print ("OnReceiveMessage:  " + "ErrCode:" + str(bIsSystemError) + " MsgCode: " + str(szMessageCode), "Msg: " + str(szMessage))
        time.sleep(1)
  
class XAQuery_t8430():
    def __init__(self):
        self.event  = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        self.event.parent = proxy(self)
        self.event.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
      
    def SetFieldData(self,gubun):
        self.event.SetFieldData('t8430InBlock','gubun', 0, gubun) 

    def Request(self,bFlag=False):
        #self.event.queryState = False           # init queryState
        XAQueryEvents.queryState = False
        self.event.Request(bFlag)
        while self.event.queryState == False:   # wait util logInState is True
            pythoncom.PumpWaitingMessages()

    def GetFieldData(self,szBlockName,szFieldName,nOccur=-1):
        if nOccur == -1:
            return self.event.GetFieldData(szBlockName,szFieldName)
        else:
            return self.event.GetFieldData(szBlockName,szFieldName,nOccur)

    def OnReceive(self):
        nCount = self.event.GetBlockCount('t8430OutBlock')                
        for i in range(nCount):
            print(i, ":", self.GetFieldData('t8430OutBlock', 'shcode', i), self.GetFieldData('t8430OutBlock', 'hname', i))            
 
                   
          
if __name__ == '__main__':
    #--------------------------------------------------------------------------
    # Login Session
    #--------------------------------------------------------------------------
    XServer = XASession()
    XServer.ConnectServer(DEMOSERVER, PORT)
    XServer.Login(ID, PW, CERT_PW)

    XAQuery = XAQuery_t8430()
    XAQuery.SetFieldData('0') # '0' ALL, '1' KOSPI, '2' KOSDAQ
    XAQuery.Request(False)
    XAQuery.OnReceive()
