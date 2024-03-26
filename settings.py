from dataclasses import dataclass
@dataclass
class settings:
    ticker: list
    interval: int
    Source:str
    macd_fastLength:float
    macd_slowLength: float 
    macd_signalLength:float
    buy_amount:float
    sell_amount:float
    williams_period:int
    overBought:float
    overSold:float
    instruction_period:str
    password:str
    email:str
setting = settings(ticker = ['STX40.JO','STXDIV.JO','STXFIN.JO','STXIND.JO','STXRAF.JO','STXSWX.JO','STXRES.JO','STXQUA.JO','STXMMT.JO','STXWDM.JO','STXEMG.JO','STX500.JO','STXNDQ.JO','STXILB.JO','STXPRO.JO','ETFGGB.JO','ETFGRE.JO','ETFWLD.JO','ETF500.JO','ETF5IT.JO','ETFBND.JO','ETFSAP.JO','ETFSWX.JO','ETFT40.JO','ETFGLD.JO','ETFPLD.JO','ETFPLT.JO','ETFRHO.JO','DIVTRX.JO','PREFTX.JO','GLPROP.JO','CSP500.JO','SMART.JO','CSPROP.JO','CTOP50.JO','NFEMOM.JO','NFEVOL.JO','MAPPSG.JO','GIVISA.JO','NFSH40.JO','NFTRCI.JO','NFEDEF.JO','NFEHGE.JO','NFEMOD.JO','GLD.JO','NGPLD.JO','NGPLT.JO','SYG4IR.JO','SYGEU.JO','SYGUK.JO','SYGP.JO','SYGEMF.JO','SYGJP.JO','SYGUS.JO','SYGWD.JO','SYG500.JO','SYGSW4.JO','SYGT40.JO','EURUSD=X','ZARUSD=X','ZAR=X','GC=F','SI=F','BZ=F','CL=F','SBPP.JO','BTC-USD','ETH-USD','ADA-USD','SOL-USD','BNB-USD','XRP-USD','DOT-USD','DOGE-USD','LUNA1-USD','AVAX-USD','ABG.JO','ARI.JO','AMS.JO','AGL.JO','ANG.JO','ANH.JO','APN.JO','BID.JO','BVT.JO','BTI.JO','CPI.JO','CLS.JO','CFR.JO','DSY.JO','EXX.JO','FSR.JO','GLN.JO','GFI.JO','IMP.JO','KIO.JO','MNP.JO','MRP.JO','MTN.JO','NPN.JO','NED.JO','NRP.JO','PPH.JO','PRX.JO','REM.JO','SLM.JO','SOL.JO','SHP.JO','SSW.JO','S32.JO','SBK.JO','VOD.JO','WHL.JO'],interval=1,
                   Source='Close',macd_fastLength=50, macd_slowLength=100, 
                   macd_signalLength=25,buy_amount=9,sell_amount=9,
                   williams_period=100,overBought=-23,overSold=-60,
                   instruction_period=['1d','1wk'],
                   password='NEWPASSWORD',
                   email='startinvestingza@gmail.com')

setting_crypto = settings(ticker = ['BTC-USD'],interval=1,
                   Source='Close',macd_fastLength=25, macd_slowLength=50, 
                   macd_signalLength=15,buy_amount=9,sell_amount=9,
                   williams_period=125,overBought=-20,overSold=-75,
                   instruction_period='5m',
                   password='NEWPASSWORD',
                   email='startinvestingza@gmail.com')