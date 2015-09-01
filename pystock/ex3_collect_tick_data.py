#ex3_collect_tick_data.py

import queue
import time
from pystock_xingAPI import *

def main():
    with Xing("demo.ebestsec.co.kr", 20001, 1, 1, "아이디", "패스워드", "") as xing:
        #1. 종목코드 선청(코스피, 코스닥 한종목씩 받아봅시다)
        shcode0 = '035420' # 네이버 tick 데이터를 받아 화면에 출력 해 봅시다.(코스피)
        shcode1 = '035720' # 다음 tick 데이터도 받아 화면에 출력 해 봅시다.(코스닥)

        # KOSPI체결(S3)
        inblock_subscription_S3_ = {
            'InBlock' : {
                # 단축코드
                'shcode' : shcode0
            }
        }

        # KOSDAQ체결(K3)
        inblock_subscription_K3_ = {
            'InBlock' : {
                # 단축코드
                'shcode' : shcode1
            }
        }

        # queue 하나를 만들고
        q = queue.Queue()

        try:
            # 2. 구독신청
            # 해당큐에 지금부터 tick데이터 구독을 시작합니다
            # 한개의 큐에다 네이버와 다음을 모두 넣어보죠
            # 당연히 큐를 여러개 만들어 종목별로 넣을 수 도 있겠죠
            xing.subscribe('xing.S3_', inblock_subscription_S3_, q)
            xing.subscribe('xing.K3_', inblock_subscription_K3_, q)

            # 3. queue를 확인하여 수신된 데이터 출력
            # 여기서부터는 큐에 자동으로 데이터가 차곡차곡 쌓입니다.
            # 우리는 주기적으로(여기서는 1초마다) 큐에 뭔가 들어왔나? 보고
            # 들어왔으면 출력 해 주면 됩니다
            while True:
                time.sleep(1)
                while not q.empty():
                    print(q.get())
            # 이 예제에서는 while True: 로 무한루프를 돌고 있기 때문에 중단시키는 방법은 ctrl+c 를 눌러 종료할 수 밖에 없습니다;

        finally:
            # 3. 구독해제
            # ctrl+c 를 누르면 키보드 인터럽트 예외가 발생하며 프로그램이 종료되는데
            # 종료하기전에 구독을 해제 시킵니다.
            # subscribe 중 unsubscribe를 하게되면 데이터 수신이 중단됩니다
            xing.unsubscribe('xing.S3_', inblock_subscription_S3_, q)
            xing.unsubscribe('xing.K3_', inblock_subscription_K3_, q)

if __name__ == '__main__':
    main()