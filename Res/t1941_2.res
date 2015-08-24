BEGIN_FUNCTION_MAP
	.Func,종목별대차거래일간추이(t1941),t1941,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1941InBlock,기본입력,input;
	begin
		종목코드,shcode,shcode,char,6;
		시작일자,sdate,sdate,char,8;
		종료일자,edate,edate,char,8;
	end
	t1941OutBlock1,출력1,output,occurs;
	begin
		일자,date,date,char,8;
		종가,price,price,long,8;
		대비구분,sign,sign,char,1;
		대비,change,change,long,8;
		등락율,diff,diff,float,6.2;
		거래량,volume,volume,long,12;
		당일체결,upvolume,upvolume,long,12;
		당일상환,dnvolume,dnvolume,long,12;
		당일잔고,tovolume,tovolume,long,12;
		잔고금액,tovalue,tovalue,long,12;
		종목코드,shcode,shcode,char,6;
	end
	END_DATA_MAP
END_FUNCTION_MAP

