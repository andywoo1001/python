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

if __name__ == "__main__":
    inXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
    inXASession.ConnectServer("demo.etrade.co.kr", 20001)
    inXASession.Login("userid", "passwd", "", 1, 0)

    while XASessionEvents.logInState == 0:
        pythoncom.PumpWaitingMessages()