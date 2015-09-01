#xingTest.py

import pystock_xingAPI

def main():
	xing = pystock_xingAPI.Xing()
	if xing.open("demo.ebestsec.co.kr", 20001, 1, 1, "아이디", "패스워드", ""):
		#서버시간조회
		inblock_query_t0167 = {'t0167InBlock':{'id':None}}
		ret = xing.query('xing.t0167', inblock_query_t0167)
		print(str(ret))
		xing.close()

if __name__ == '__main__':
	main()