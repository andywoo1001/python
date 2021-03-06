BEGIN_FUNCTION_MAP
.Feed, 주식주문체결, SC1, key=8, group=1;
    BEGIN_DATA_MAP
    InBlock,입력,input;
    begin
    end
    OutBlock,출력,output;
    begin
		라인일련번호,   		lineseq,		    lineseq,    	long,   10;
		계좌번호,				accno,				accno,			char,	11;
		조작자ID,				user,	   			 user,	   		char,	8;
		헤더길이,				len,				len,			long,	6;
		헤더구분,				gubun,				gubun,			char,	1;
		압축구분,				compress,			compress,		char,	1;
		암호구분,				encrypt,			encrypt,		char,	1;
		공통시작지점,			offset,				offset,			long,	3;
		TRCODE,					trcode,				trcode,			char,	8;
		이용사번호,				comid,				compid,			char,	3;
		사용자ID,				userid,				userid,			char,	16;
		접속매체,				media,				media,			char,	2;
		I/F일련번호,			ifid,				ifid,			char,	3;
		전문일련번호,			seq,				seq,			char,	9;
		TR추적ID,				trid,				trid,			char,	16;
		공인IP,					pubip,				pubip,			char,	12;
		사설IP,					prvip,				prvip,			char,	12;
		처리지점번호,			pcbpno,				pcbpno,			char,	3;
		지점번호,				bpno,				bpno,			char,	3;
		단말번호,				termno,				termno,			char,	8;
		언어구분,				lang,				lang,			char,	1;
		AP처리시간,				proctm,				proctm,			long,	9;
		메세지코드,				msgcode,			msgcode,		char,	4;
		메세지출력구분,			outgu,				outgu,			char,	1;
		압축요청구분,			compreq,			compreq,		char,	1;
		기능키,					funckey,			funckey,		char,	4;
		요청레코드개수,			reqcnt,				reqcnt,			long,	4;
		예비영역,				filler,				filler,			char,	6;
		연속구분,				cont,				cont,			char,	1;
		연속키값,				contkey,			contkey,		char,	18;
		가변시스템길이,			varlen,				varlen,			long,	2;
		가변해더길이,			varhdlen,			varhdlen,		long,	2;
		가변메시지길이,			varmsglen,			varmsglen,		long,	2;
		조회발원지,				trsrc,				trsrc,			char,	1;
		I/F이벤트ID,			eventid,			eventid,		char,	4;
		I/F정보,				ifinfo,				ifinfo,			char,	4;
		예비영역,				filler1,			filler1,		char,	41;
		주문체결유형코드,		ordxctptncode,		ordxctptncode,	char,	2;
		주문시장코드,			ordmktcode,			ordmktcode,		char,	2;
		주문유형코드,			ordptncode,			ordptncode,		char,	2;
		관리지점번호,			mgmtbrnno,			mgmtbrnno,		char,	3;
		계좌번호,				accno1,				accno1,			char,	11;
		계좌번호,				accno2,				accno2,			char,	9;
		계좌명,					acntnm,				acntnm,			char,	40;
		종목번호,				Isuno,				Isuno,			char,	12;
		종목명,					Isunm,				Isunm,			char,	40;
		주문번호,				ordno,				ordno,			long,	10;
		원주문번호,				orgordno,			orgordno,		long,	10;
		체결번호,				execno,				execno,			long,	10;
		주문수량,				ordqty,				ordqty,			long,	16;
		주문가격,				ordprc,				ordprc,			long,	13;
		체결수량,				execqty,			execqty,		long,	16;
		체결가격,				execprc,			execprc,		long,	13;
		정정확인수량,			mdfycnfqty,			mdfycnfqty,		long,	16;
		정정확인가격,			mdfycnfprc,			mdfycnfprc,		long,	16;
		취소확인수량,			canccnfqty,			canccnfqty,		long,	16;
		거부수량,				rjtqty,				rjtqty,			long,	16;
		주문처리유형코드,		ordtrxptncode,		ordtrxptncode,	long,	4;
		복수주문일련번호,		mtiordseqno,		mtiordseqno,	long,	10;
		주문조건,				ordcndi,			ordcndi,		char,	1;
		호가유형코드,			ordprcptncode,		ordprcptncode,	char,	2;
		비저축체결수량,			nsavtrdqty,			nsavtrdqty,		long,	16;
		단축종목번호,			shtnIsuno,			shtnIsuno,		char,	9;
		운용지시번호,			opdrtnno,			opdrtnno,		char,	12;
		반대매매주문구분,		cvrgordtp,			cvrgordtp,		char,	1;
		미체결수량(주문),		unercqty,			unercqty,		long,	16;
		원주문미체결수량,		orgordunercqty,		orgordunercqty,	long,	16;
		원주문정정수량,			orgordmdfyqty,		orgordmdfyqty,	long,	16;
		원주문취소수량,			orgordcancqty,		orgordcancqty,	long,	16;
		주문평균체결가격,		ordavrexecprc,		ordavrexecprc,	long,	13;
		주문금액,				ordamt,				ordamt,			long,	16;
		표준종목번호,			stdIsuno,			stdIsuno,		char,	12;
		전표준종목번호,			bfstdIsuno,			bfstdIsuno,		char,	12;
		매매구분,				bnstp,				bnstp,			char,	1;
		주문거래유형코드,		ordtrdptncode,		ordtrdptncode,	char,	2;
		신용거래코드,			mgntrncode,			mgntrncode,		char,	3;
		수수료합산코드,			adduptp,			adduptp,		char,	2;
		통신매체코드,			commdacode,			commdacode,		char,	2;
		대출일,					Loandt,				Loandt,			char,	8;
		회원/비회원사번호,		mbrnmbrno,			mbrnmbrno,		long,	3;
		주문계좌번호,			ordacntno,			ordacntno,		char,	20;
		집계지점번호,			agrgbrnno,			agrgbrnno,		char,	3;
		관리사원번호,			mgempno,			mgempno,		char,	9;
		선물연계지점번호,		futsLnkbrnno,		futsLnkbrnno,	char,	3;
		선물연계계좌번호,		futsLnkacntno,		futsLnkacntno,	char,	20;
		선물시장구분,			futsmkttp,			futsmkttp,		char,	1;
		등록시장코드,			regmktcode,			regmktcode,		char,	2;
		현금증거금률,			mnymgnrat,			mnymgnrat,		long,	7;
		대용증거금률,			substmgnrat,		substmgnrat,	long,	9;
		현금체결금액,			mnyexecamt,			mnyexecamt,		long,	16;
		대용체결금액,			ubstexecamt,		ubstexecamt,	long,	16;
		수수료체결금액,			cmsnamtexecamt,		cmsnamtexecamt,	long,	16;
		신용담보체결금액,		crdtpldgexecamt,	crdtpldgexecamt, long,	16;
		신용체결금액,			crdtexecamt,		crdtexecamt,	long,	16;
		전일재사용체결금액,		prdayruseexecval,	prdayruseexecval, long,	16;
		금일재사용체결금액,		crdayruseexecval,	crdayruseexecval, long,	16;
		실물체결수량,			spotexecqty,		spotexecqty,	long,	16;
		공매도체결수량,			stslexecqty,		stslexecqty,	long,	16;
		전략코드,				strtgcode,			strtgcode,		char,	6;
		그룹Id,					grpId,				grpId,			char,	20;
		주문회차,				ordseqno,			ordseqno,		long,	10;
		포트폴리오번호,			ptflno,				ptflno,			long,	10;
		바스켓번호,				bskno,				bskno,			long,	10;
		트렌치번호,				trchno,				trchno,			long,	10;
		아이템번호,				itemno,				itemno,			long,	10;
		주문자Id,				orduserId,			orduserId,		char,	16;
		차입관리여부,			brwmgmtYn,			brwmgmtYn,		long,	1;
		외국인고유번호,			frgrunqno,			frgrunqno,		char,	6;
		거래세징수구분,			trtzxLevytp,		trtzxLevytp,	char,	1;
		유동성공급자구분,		lptp,				lptp,			char,	1;
		체결시각,				exectime,			exectime,		char,	9;
		거래소수신체결시각,		rcptexectime,		rcptexectime,	char,	9;
		잔여대출금액,			rmndLoanamt,		rmndLoanamt,	long,	16;
		잔고수량,				secbalqty,			secbalqty,		long,	16;
		실물가능수량,			spotordableqty,		spotordableqty,	long,	16;
		재사용가능수량(매도),	ordableruseqty,		ordableruseqty,	long,	16;
		변동수량,				flctqty,			flctqty,		long,	16;
		잔고수량(d2),			secbalqtyd2,		secbalqtyd2,	long,	16;
		매도주문가능수량,		sellableqty,		sellableqty,	long,	16;
		미체결매도주문수량,		unercsellordqty,	unercsellordqty, long,	16;
		평균매입가,				avrpchsprc,			avrpchsprc,		long,	13;
		매입금액,				pchsant,			pchsant,		long,	16;
		예수금,					deposit,			deposit,		long,	16;
		대용금,					substamt,			substamt,		long,	16;
		위탁증거금현금,			csgnmnymgn,			csgnmnymgn,		long,	16;
		위탁증거금대용,			csgnsubstmgn,		csgnsubstmgn,	long,	16;
		신용담보재사용금,		crdtpldgruseamt,	crdtpldgruseamt, long,	16;
		주문가능현금,			ordablemny,			ordablemny,		long,	16;
		주문가능대용,			ordablesubstamt,	ordablesubstamt, long,	16;
		재사용가능금액,			ruseableamt,		ruseableamt,	long,	16;
    end
    END_DATA_MAP
END_FUNCTION_MAP
