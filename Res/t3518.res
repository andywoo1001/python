BEGIN_FUNCTION_MAP
	.Func,해외실시간지수(t3518),t3518,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t3518InBlock,입력,input;
	begin
		종목종류,kind,kind,char,1;
		SYMBOL,symbol,symbol,char,16;
		입력건수,cnt,cnt,long,4;
		조회구분,jgbn,jgbn,char,1;
		N분,nmin,nmin,long,3;
		CTS_DATE,cts_date,cts_date,char,8;
		CTS_TIME,cts_time,cts_time,char,6;
	end
	t3518OutBlock,단일출력,output;
	begin
		CTS_DATE,cts_date,cts_date,char,8;
		CTS_TIME,cts_time,cts_time,char,6;
	end
	t3518OutBlock1,멀티출력,output,occurs;
	begin
		일자,date,date,char,8;
		시간,time,time,char,8;
		시가,open,open,double,9.4;
		고가,high,high,double,9.4;
		저가,low,low,double,9.4;
		현재가,price,price,double,9.4;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,double,9.4;
		등락율,uprate,uprate,double,9.4;
		누적거래량,volume,volume,double,12.0;
		매수호가,bidho,bidho,double,9.4;
		매도호가,offerho,offerho,double,9.4;
		매수잔량,bidrem,bidrem,double,12.0;
		매도잔량,offerrem,offerrem,double,12.0;
		종목종류,kind,kind,char,1;
		SYMBOL,symbol,symbol,char,16;
		EXID,exid,exid,char,4;
		한국일자,kodate,kodate,char,8;
		한국시간,kotime,kotime,char,8;
	end
	END_DATA_MAP
END_FUNCTION_MAP

