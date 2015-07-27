import  pandas as pd
import  matplotlib.pyplot as plt
import  sys
import  win32com.client
import  pythoncom 
import  time
from    weakref import proxy

# SERVER VAR
REALSERVER = 'demo.etrade.co.kr'
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
        time.sleep(3)
     

class XAQuery_t8413():
    def __init__(self):
        self.event  = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
        self.event.parent = proxy(self)
        self.event.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8413.res")
        self.data = []
        #XAColumn = ['Date', 'Open', 'High', 'Low', 'Close', 'Vol', 'Value']
        #XAColumn = ['Date', 'Close']
        #self.data = pd.DataFrame(columns=XAColumn)

    def SetFieldData(self,shcode):
        self.event.SetFieldData('t8413InBlock','shcode', 0, shcode)
        self.event.SetFieldData('t8413InBlock','gubun', 0, '2') # Day
        self.event.SetFieldData('t8413InBlock','qrycnt', 0, None) #2000
        self.event.SetFieldData('t8413InBlock','sdate', 0, '19800101')
        self.event.SetFieldData('t8413InBlock','edate', 0, '99999999')
        self.event.SetFieldData('t8413InBlock','cts_date', 0, None)
        self.event.SetFieldData('t8413InBlock','comp_yn', 0, 'N')

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
        self.cts_date = self.GetFieldData('t8413OutBlock','cts_date',0)
        nCount = self.event.GetBlockCount('t8413OutBlock1')                
        for i in range(nCount-1, -1, -1):
            #print(i, ":", self.GetFieldData('t8413OutBlock1', 'date', i), ":", self.GetFieldData('t8413OutBlock1', 'close', i))            
            Date    = self.GetFieldData('t8413OutBlock1','date',i)
            Open    = float(self.GetFieldData('t8413OutBlock1','open',i))
            High    = float(self.GetFieldData('t8413OutBlock1','high',i))
            Low     = float(self.GetFieldData('t8413OutBlock1','low',i))
            Close   = float(self.GetFieldData('t8413OutBlock1','close',i))
            Vol     = float(self.GetFieldData('t8413OutBlock1','jdiff_vol',i))
            Value   = float(self.GetFieldData('t8413OutBlock1','value',i))
            self.data.append([Date, Open, High, Low, Close, Vol, Value])

    def OnReceiveContinue(self):
        while self.cts_date.strip():
            self.event.SetFieldData('t8413InBlock','cts_date', 0, self.cts_date)
            #XAQueryEvents.queryState = False
            self.Request(True)
        
            nCount = self.event.GetBlockCount('t8413OutBlock1')                
            for i in range(nCount-1, -1, -1):
                #print(i, ":", self.GetFieldData('t8413OutBlock1', 'date', i), ":", self.GetFieldData('t8413OutBlock1', 'close', i))            
                Date    = self.GetFieldData('t8413OutBlock1','date',i)
                Open    = float(self.GetFieldData('t8413OutBlock1','open',i))
                High    = float(self.GetFieldData('t8413OutBlock1','high',i))
                Low     = float(self.GetFieldData('t8413OutBlock1','low',i))
                Close   = float(self.GetFieldData('t8413OutBlock1','close',i))
                Vol     = float(self.GetFieldData('t8413OutBlock1','jdiff_vol',i))
                Value   = float(self.GetFieldData('t8413OutBlock1','value',i))
                self.data.append([Date, Open, High, Low, Close, Vol, Value])

            self.cts_date = self.GetFieldData('t8413OutBlock','cts_date',0)

def WriteToCVS(shcode):
    XAQuery = XAQuery_t8413()
    XAQuery.SetFieldData(shcode) #005930
    XAQuery.Request(False)
    XAQuery.OnReceive()

    XAQuery.OnReceiveContinue()
    XAColumn = ['Date', 'Open', 'High', 'Low', 'Close', 'Vol', 'Value']
    DB = pd.DataFrame(XAQuery.data, columns=XAColumn)
    #DB.sort(columns='Date',ascending=True)
    DB.to_csv(shcode+'.csv')


if __name__ == '__main__':
    #--------------------------------------------------------------------------
    # Login Session
    #--------------------------------------------------------------------------
    XServer = XASession()
    XServer.ConnectServer(REALSERVER, PORT)
    XServer.Login(ID, PW, CERT_PW)
    
    File = open("KOSPI_KOSDAQ.txt")
    lists = File.readlines()

    for item in lists:
        shcode = item.split('\n')[0]
        print("\n\n Loading " + shcode)
        WriteToCVS(shcode)
