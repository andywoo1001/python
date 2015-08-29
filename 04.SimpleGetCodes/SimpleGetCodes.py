import win32com.client
import pythoncom

class XASessionEvents:
    logInState = 0
    def OnLogin(self, code, msg):
        print("OnLogin method is called")
        print(str(code))
        print(str(msg))
        if str(code) == '0000':
            XASessionEvents.logInState = 1

    def OnLogout(self):
        print("OnLogout method is called")

    def OnDisconnect(self):
        print("OnDisconnect method is called")

class XAQueryEvents:
    queryState = 0
    def OnReceiveData(self, szTrCode):
        print("ReceiveData")
        XAQueryEvents.queryState = 1
    def OnReceiveMessage(self, systemError, mesageCode, message):
        print("ReceiveMessage")

if __name__ == "__main__":
    #--------------------------------------------------------------------------
    # Login Session
    #--------------------------------------------------------------------------
    inXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
    inXASession.ConnectServer("demo.etrade.co.kr", 20001)
    inXASession.Login("userid", "passwd", "", 1, 0)

    while XASessionEvents.logInState == 0:
        pythoncom.PumpWaitingMessages()

    #--------------------------------------------------------------------------
    # Get single data 
    #--------------------------------------------------------------------------
    inXAQuery = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    inXAQuery.LoadFromResFile("C:\\eBEST\\xingAPI\\Res\\t8430.res")
    inXAQuery.SetFieldData('t8430InBlock', 'gubun', 0, 1)
    inXAQuery.Request(0)

    while XAQueryEvents.queryState == 0:
        pythoncom.PumpWaitingMessages()

    # Get FieldData
    nCount = inXAQuery.GetBlockCount('t8430OutBlock')
    for i in range(nCount):
        print(i, ":", inXAQuery.GetFieldData('t8430OutBlock', 'shcode', i), inXAQuery.GetFieldData('t8430OutBlock', 'hname', i), )
