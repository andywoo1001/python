BEGIN_FUNCTION_MAP
	.Func,ETFLP호가(t1906),t1906,attr,block,headtype=A;
	BEGIN_DATA_MAP
	t1906InBlock,기본입력,input;
	begin
		단축코드,shcode,shcode,char,6;
	end
	t1906OutBlock,출력,output;
	begin
		한글명,hname,hname,char,20;
		현재가,price,price,long,8;
		전일대비구분,sign,sign,char,1;
		전일대비,change,change,long,8;
		등락율,diff,diff,float,6.2;
		누적거래량,volume,volume,long,12;
		LP매도호가수량1,lp_offerrem1,lp_offerrem1,long,12;
		LP매수호가수량1,lp_bidrem1,lp_bidrem1,long,12;
		LP매도호가수량2,lp_offerrem2,lp_offerrem2,long,12;
		LP매수호가수량2,lp_bidrem2,lp_bidrem2,long,12;
		LP매도호가수량3,lp_offerrem3,lp_offerrem3,long,12;
		LP매수호가수량3,lp_bidrem3,lp_bidrem3,long,12;
		LP매도호가수량4,lp_offerrem4,lp_offerrem4,long,12;
		LP매수호가수량4,lp_bidrem4,lp_bidrem4,lnog,12;
		LP매도호가수량5,lp_offerrem5,lp_offerrem5,long,12;
		LP매수호가수량5,lp_bidrem5,lp_bidrem5,long,12;
		LP매도호가수량6,lp_offerrem6,lp_offerrem6,long,12;
		LP매수호가수량6,lp_bidrem6,lp_bidrem6,long,12;
		LP매도호가수량7,lp_offerrem7,lp_offerrem7,long,12;
		LP매수호가수량7,lp_bidrem7,lp_bidrem7,long,12;
		LP매도호가수량8,lp_offerrem8,lp_offerrem8,long,12;
		LP매수호가수량8,lp_bidrem8,lp_bidrem8,long,12;
		LP매도호가수량9,lp_offerrem9,lp_offerrem9,long,12;
		LP매수호가수량9,lp_bidrem9,lp_bidrem9,long,12;
		LP매도호가수량10,lp_offerrem10,lp_offerrem10,long,12;
		LP매수호가수량10,lp_bidrem10,lp_bidrem10,long,12;
		전일종가,jnilclose,jnilclose,long,8;
		매도호가1,offerho1,offerho1,long,8;
		매수호가1,bidho1,bidho1,long,8;
		매도호가수량1,offerrem1,offerrem1,long,12;
		매수호가수량1,bidrem1,bidrem1,long,12;
		직전매도대비수량1,preoffercha1,preoffercha1,long,12;
		직전매수대비수량1,prebidcha1,prebidcha1,long,12;
		매도호가2,offerho2,offerho2,long,8;
		매수호가2,bidho2,bidho2,long,8;
		매도호가수량2,offerrem2,offerrem2,long,12;
		매수호가수량2,bidrem2,bidrem2,long,12;
		직전매도대비수량2,preoffercha2,preoffercha2,long,12;
		직전매수대비수량2,prebidcha2,prebidcha2,long,12;
		매도호가3,offerho3,offerho3,long,8;
		매수호가3,bidho3,bidho3,long,8;
		매도호가수량3,offerrem3,offerrem3,long,12;
		매수호가수량3,bidrem3,bidrem3,long,12;
		직전매도대비수량3,preoffercha3,preoffercha3,long,12;
		직전매수대비수량3,prebidcha3,prebidcha3,long,12;
		매도호가4,offerho4,offerho4,long,8;
		매수호가4,bidho4,bidho4,long,8;
		매도호가수량4,offerrem4,offerrem4,long,12;
		매수호가수량4,bidrem4,bidrem4,long,12;
		직전매도대비수량4,preoffercha4,preoffercha4,long,12;
		직전매수대비수량4,prebidcha4,prebidcha4,long,12;
		매도호가5,offerho5,offerho5,long,8;
		매수호가5,bidho5,bidho5,long,8;
		매도호가수량5,offerrem5,offerrem5,long,12;
		매수호가수량5,bidrem5,bidrem5,long,12;
		직전매도대비수량5,preoffercha5,preoffercha5,long,12;
		직전매수대비수량5,prebidcha5,prebidcha5,long,12;
		매도호가6,offerho6,offerho6,long,8;
		매수호가6,bidho6,bidho6,long,8;
		매도호가수량6,offerrem6,offerrem6,long,12;
		매수호가수량6,bidrem6,bidrem6,long,12;
		직전매도대비수량6,preoffercha6,preoffercha6,long,12;
		직전매수대비수량6,prebidcha6,prebidcha6,long,12;
		매도호가7,offerho7,offerho7,long,8;
		매수호가7,bidho7,bidho7,long,8;
		매도호가수량7,offerrem7,offerrem7,long,12;
		매수호가수량7,bidrem7,bidrem7,long,12;
		직전매도대비수량7,preoffercha7,preoffercha7,long,12;
		직전매수대비수량7,prebidcha7,prebidcha7,long,12;
		매도호가8,offerho8,offerho8,long,8;
		매수호가8,bidho8,bidho8,long,8;
		매도호가수량8,offerrem8,offerrem8,long,12;
		매수호가수량8,bidrem8,bidrem8,long,12;
		직전매도대비수량8,preoffercha8,preoffercha8,long,12;
		직전매수대비수량8,prebidcha8,prebidcha8,long,12;
		매도호가9,offerho9,offerho9,long,8;
		매수호가9,bidho9,bidho9,long,8;
		매도호가수량9,offerrem9,offerrem9,long,12;
		매수호가수량9,bidrem9,bidrem9,long,12;
		직전매도대비수량9,preoffercha9,preoffercha9,long,12;
		직전매수대비수량9,prebidcha9,prebidcha9,long,12;
		매도호가10,offerho10,offerho10,long,8;
		매수호가10,bidho10,bidho10,long,8;
		매도호가수량10,offerrem10,offerrem10,long,12;
		매수호가수량10,bidrem10,bidrem10,long,12;
		직전매도대비수량10,preoffercha10,preoffercha10,long,12;
		직전매수대비수량10,prebidcha10,prebidcha10,long,12;
		매도호가수량합,offer,offer,long,12;
		매수호가수량합,bid,bid,long,12;
		직전매도대비수량합,preoffercha,preoffercha,long,12;
		직전매수대비수량합,prebidcha,prebidcha,long,12;
		수신시간,hotime,hotime,char,8;
		예상체결가격,yeprice,yeprice,long,8;
		예상체결수량,yevolume,yevolume,long,12;
		예상체결전일구분,yesign,yesign,char,1;
		예상체결전일대비,yechange,yechange,long,8;
		예상체결등락율,yediff,yediff,float,6.2;
		시간외매도잔량,tmoffer,tmoffer,long,12;
		시간외매수잔량,tmbid,tmbid,long,12;
		동시구분,ho_status,ho_status,char,1;
		단축코드,shcode,shcode,char,6;
		상한가,uplmtprice,uplmtprice,long,8;
		하한가,dnlmtprice,dnlmtprice,long,8;
		시가,open,open,long,8;
		고가,high,high,long,8;
		저가,low,low,long,8;
	end
	END_DATA_MAP
END_FUNCTION_MAP

