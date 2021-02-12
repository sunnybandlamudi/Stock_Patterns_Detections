from nsetools import nse;
from nse import Nse
import numpy as np;
import pandas as pd
import requests as req;
from datetime import date,timedelta;
import math #needed for definition of pi




def get_historic_data(stock):
    params = {
        'symbol':stock,
        'series':'["EQ"]',
        'from': (date.today() - timedelta(days=90)).strftime("%d-%m-%Y"),
        'to': date.today().strftime('%d-%m-%Y')
    }
    data = req.get('https://www.nseindia.com/api/historical/cm/equity',params = params,headers = head)

    # pprint(data.json())
    return data.json()['data']


def getMaxMin( STOCK , pmx = False ):
    historic_data = get_historic_data(STOCK)

    df = pd.DataFrame(historic_data)
    # x = np.arange(0, 5*1, 1)
    # y = ['2020-11-17','2020-11-16','2020-11-15','2020-11-14','2020-11-13']

    x= df['CH_TIMESTAMP'][::]
    y= df['CH_CLOSING_PRICE'][::]
    z = df['CH_TRADE_HIGH_PRICE'][::]
    return  list(zip(x,y,z))


def getNR(mapping):
    maxpoint = None;
    localMax = []
    
    for j in range(2,len(mapping)-30):
        if( (mapping[j-1][CLOSE] > mapping[j][CLOSE] < mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] > mapping[j][CLOSE] < mapping[j+2][CLOSE])):
            localMin = mapping[j]
            break;
    for j in range(2,len(mapping)-30):
        if( (mapping[j-1][CLOSE] < mapping[j][CLOSE] > mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] < mapping[j][CLOSE] > mapping[j+2][CLOSE])):
            localMax.append(mapping[j])
    count = 0;
    for i in range(len(mapping)):
        if(localMin[CLOSE] < mapping[i][CLOSE] < localMax[0][CLOSE]):
            count+=1;
        else:
            nr = mapping[i]  
            break;
    trend = 1;
    for i in range(1,len(localMax)):
        if(localMax[i-1][CLOSE] > localMax[i][CLOSE]):
            trend += 1;
        else:
            break;
    return localMax[0],localMin,nr,count,trend;

def getNRone():
    stk = "JKTYRE";
    mapping = getMaxMin(stk);
    #print(mapping)
    localMax,localMin,nr,count = getNR(mapping);
    print("STK: {}\nMax {}\nMin {}\nNR {}\nCount {}\n".format(stk,localMax,localMin,nr,count))

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

req = req.Session()
req.get('https://www.nseindia.com',headers=head)
# req.get('https://www.nseindia.com',headers=head)

db = Nse()
fno = nse.Nse()
fno_lot = fno.get_fno_lot_sizes(as_json=False);
nifty200 = ["ACC","AUBANK","AARTIIND","ABBOTINDIA","ADANIENT","ADANIGREEN","ADANIPORTS","ATGL","ADANITRANS","ABCAPITAL","ABFRL","AJANTPHARM","APLLTD","ALKEM","AMARAJABAT","AMBUJACEM","APOLLOHOSP","APOLLOTYRE","ASHOKLEY","ASIANPAINT","AUROPHARMA","DMART","AXISBANK","BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BAJAJHLDNG","BALKRISIND","BANDHANBNK","BANKBARODA","BANKINDIA","BATAINDIA","BERGEPAINT","BEL","BHARATFORG","BHEL","BPCL","BHARTIARTL","BIOCON","BBTC","BOSCHLTD","BRITANNIA","CESC","CADILAHC","CANBK","CASTROLIND","CHOLAFIN","CIPLA","CUB","COALINDIA","COFORGE","COLPAL","CONCOR","COROMANDEL","CROMPTON","CUMMINSIND","DLF","DABUR","DALBHARAT","DHANI","DIVISLAB","LALPATHLAB","DRREDDY","EDELWEISS","EICHERMOT","EMAMILTD","ENDURANCE","ESCORTS","EXIDEIND","FEDERALBNK","FORTIS","FRETAIL","GAIL","GMRINFRA","GICRE","GLENMARK","GODREJAGRO","GODREJCP","GODREJIND","GODREJPROP","GRASIM","GUJGASLTD","GSPL","HCLTECH","HDFCAMC","HDFCBANK","HDFCLIFE","HAVELLS","HEROMOTOCO","HINDALCO","HINDPETRO","HINDUNILVR","HINDZINC","HUDCO","HDFC","ICICIBANK","ICICIGI","ICICIPRULI","ISEC","IDFCFIRSTB","ITC","IBULHSGFIN","INDHOTEL","IOC","IRCTC","IGL","INDUSTOWER","INDUSINDBK","NAUKRI","INFY","INDIGO","IPCALAB","JSWENERGY","JSWSTEEL","JINDALSTEL","JUBLFOOD","KOTAKBANK","L&TFH","LTTS","LICHSGFIN","LTI","LT","LUPIN","MRF","MGL","M&MFIN","M&M","MANAPPURAM","MARICO","MARUTI","MFSL","MINDTREE","MOTHERSUMI","MPHASIS","MUTHOOTFIN","NATCOPHARM","NMDC","NTPC","NATIONALUM","NAVINFLUOR","NESTLEIND","NAM-INDIA","OBEROIRLTY","ONGC","OIL","OFSS","PIIND","PAGEIND","PETRONET","PFIZER","PIDILITIND","PEL","POLYCAB","PFC","POWERGRID","PRESTIGE","PGHH","PNB","RBLBANK","RECLTD","RAJESHEXPO","RELIANCE","SBICARD","SBILIFE","SRF","SANOFI","SHREECEM","SRTRANSFIN","SIEMENS","SBIN","SAIL","SUNPHARMA","SUNTV","SYNGENE","TVSMOTOR","TATACHEM","TCS","TATACONSUM","TATAMOTORS","TATAPOWER","TATASTEEL","TECHM","RAMCOCEM","TITAN","TORNTPHARM","TORNTPOWER","TRENT","UPL","ULTRACEMCO","UNIONBANK","UBL","MCDOWELL-N","VGUARD","VBL","IDEA","VOLTAS","WHIRLPOOL","WIPRO","YESBANK","ZEEL"];
nifty500 =  ["3MINDIA" ,"ABB" ,"POWERINDIA" ,"ACC" ,"AIAENG" ,"APLAPOLLO" ,"AUBANK" ,"AARTIDRUGS" ,"AARTIIND" ,"AAVAS" ,"ABBOTINDIA" ,"ADANIENT" ,"ADANIGREEN" ,"ADANIPORTS" ,"ATGL" ,"ADANITRANS" ,"ABCAPITAL" ,"ABFRL" ,"ADVENZYMES" ,"AEGISCHEM" ,"AFFLE" ,"AJANTPHARM" ,"AKZOINDIA" ,"ALEMBICLTD" ,"APLLTD" ,"ALKEM" ,"ALKYLAMINE" ,"ALOKINDS" ,"AMARAJABAT" ,"AMBER" ,"AMBUJACEM" ,"APOLLOHOSP" ,"APOLLOTYRE" ,"ASHOKLEY" ,"ASHOKA" ,"ASIANPAINT" ,"ASTERDM" ,"ASTRAZEN" ,"ASTRAL" ,"ATUL" ,"AUROPHARMA" ,"AVANTIFEED" ,"DMART" ,"AXISBANK" ,"BASF" ,"BEML" ,"BSE" ,"BAJAJ-AUTO" ,"BAJAJCON" ,"BAJAJELEC" ,"BAJFINANCE" ,"BAJAJFINSV" ,"BAJAJHLDNG" ,"BALKRISIND" ,"BALMLAWRIE" ,"BALRAMCHIN" ,"BANDHANBNK" ,"BANKBARODA" ,"BANKINDIA" ,"MAHABANK" ,"BATAINDIA" ,"BAYERCROP" ,"BERGEPAINT" ,"BDL" ,"BEL" ,"BHARATFORG" ,"BHEL" ,"BPCL" ,"BHARATRAS" ,"BHARTIARTL" ,"BIOCON" ,"BIRLACORPN" ,"BSOFT" ,"BLISSGVS" ,"BLUEDART" ,"BLUESTARCO" ,"BBTC" ,"BOMDYEING" ,"BOSCHLTD" ,"BRIGADE" ,"BRITANNIA" ,"CARERATING" ,"CCL" ,"CESC" ,"CRISIL" ,"CSBBANK" ,"CADILAHC" ,"CANFINHOME" ,"CANBK" ,"CAPLIPOINT" ,"CGCL" ,"CARBORUNIV" ,"CASTROLIND" ,"CEATLTD" ,"CENTRALBK" ,"CDSL" ,"CENTURYPLY" ,"CENTURYTEX" ,"CERA" ,"CHALET" ,"CHAMBLFERT" ,"CHENNPETRO" ,"CHOLAHLDNG" ,"CHOLAFIN" ,"CIPLA" ,"CUB" ,"COALINDIA" ,"COCHINSHIP" ,"COFORGE" ,"COLPAL" ,"CONCOR" ,"COROMANDEL" ,"CREDITACC" ,"CROMPTON" ,"CUMMINSIND" ,"CYIENT" ,"DBCORP" ,"DCBBANK" ,"DCMSHRIRAM" ,"DLF" ,"DABUR" ,"DALBHARAT" ,"DEEPAKNTR" ,"DELTACORP" ,"DHANI" ,"DHANUKA" ,"DBL" ,"DISHTV" ,"DCAL" ,"DIVISLAB" ,"DIXON" ,"LALPATHLAB" ,"DRREDDY" ,"EIDPARRY" ,"EIHOTEL" ,"EPL" ,"ESABINDIA" ,"EDELWEISS" ,"EICHERMOT" ,"ELGIEQUIP" ,"EMAMILTD" ,"ENDURANCE" ,"ENGINERSIN" ,"EQUITAS" ,"ERIS" ,"ESCORTS" ,"EXIDEIND" ,"FDC" ,"FEDERALBNK" ,"FINEORG" ,"FINCABLES" ,"FINPIPE" ,"FSL" ,"FORTIS" ,"FCONSUMER" ,"FRETAIL" ,"GAIL" ,"GEPIL" ,"GHCL" ,"GMMPFAUDLR" ,"GMRINFRA" ,"GALAXYSURF" ,"GRSE" ,"GARFIBRES" ,"GICRE" ,"GILLETTE" ,"GLAXO" ,"GLENMARK" ,"GODFRYPHLP" ,"GODREJAGRO" ,"GODREJCP" ,"GODREJIND" ,"GODREJPROP" ,"GRANULES" ,"GRAPHITE" ,"GRASIM" ,"GESHIP" ,"GREAVESCOT" ,"GRINDWELL" ,"GUJALKALI" ,"GAEL" ,"FLUOROCHEM" ,"GUJGASLTD" ,"GMDCLTD" ,"GNFC" ,"GPPL" ,"GSFC" ,"GSPL" ,"GULFOILLUB" ,"HEG" ,"HCLTECH" ,"HDFCAMC" ,"HDFCBANK" ,"HDFCLIFE" ,"HFCL" ,"HATHWAY" ,"HATSUN" ,"HAVELLS" ,"HEIDELBERG" ,"HERITGFOOD" ,"HEROMOTOCO" ,"HSCL" ,"HINDALCO" ,"HAL" ,"HINDCOPPER" ,"HINDPETRO" ,"HINDUNILVR" ,"HINDZINC" ,"HONAUT" ,"HUDCO" ,"HDFC" ,"HUHTAMAKI" ,"ICICIBANK" ,"ICICIGI" ,"ICICIPRULI" ,"ISEC" ,"ICRA" ,"IDBI" ,"IDFCFIRSTB" ,"IDFC" ,"IFBIND" ,"IIFL" ,"IIFLWAM" ,"IOLCP" ,"IRB" ,"IRCON" ,"ITC" ,"ITI" ,"INDIACEM" ,"IBULHSGFIN" ,"IBREALEST" ,"INDIAMART" ,"INDIANB" ,"IEX" ,"INDHOTEL" ,"IOC" ,"IOB" ,"IRCTC" ,"INDOCO" ,"IGL" ,"INDUSTOWER" ,"INDUSINDBK" ,"NAUKRI" ,"INFY" ,"INGERRAND" ,"INOXLEISUR" ,"INDIGO" ,"IPCALAB" ,"JBCHEPHARM" ,"JKCEMENT" ,"JKLAKSHMI" ,"JKPAPER" ,"JKTYRE" ,"JMFINANCIL" ,"JSWENERGY" ,"JSWSTEEL" ,"JTEKTINDIA" ,"JAGRAN" ,"JAICORPLTD" ,"J&KBANK" ,"JAMNAAUTO" ,"JINDALSAW" ,"JSLHISAR" ,"JSL" ,"JINDALSTEL" ,"JCHAC" ,"JUBLFOOD" ,"JUSTDIAL" ,"JYOTHYLAB" ,"KEI" ,"KNRCON" ,"KRBL" ,"KSB" ,"KAJARIACER" ,"KALPATPOWR" ,"KANSAINER" ,"KTKBANK" ,"KARURVYSYA" ,"KSCL" ,"KEC" ,"KOLTEPATIL" ,"KOTAKBANK" ,"L&TFH" ,"LTTS" ,"LICHSGFIN" ,"LAOPALA" ,"LAXMIMACH" ,"LTI" ,"LT" ,"LAURUSLABS" ,"LEMONTREE" ,"LINDEINDIA" ,"LUPIN" ,"LUXIND" ,"MASFIN" ,"MMTC" ,"MOIL" ,"MRF" ,"MGL" ,"MAHSCOOTER" ,"MAHSEAMLES" ,"M&MFIN" ,"M&M" ,"MAHINDCIE" ,"MHRIL" ,"MAHLOG" ,"MANAPPURAM" ,"MRPL" ,"MARICO" ,"MARUTI" ,"MFSL" ,"METROPOLIS" ,"MINDTREE" ,"MINDACORP" ,"MINDAIND" ,"MIDHANI" ,"MOTHERSUMI" ,"MOTILALOFS" ,"MPHASIS" ,"MCX" ,"MUTHOOTFIN" ,"NATCOPHARM" ,"NBCC" ,"NCC" ,"NESCO" ,"NHPC" ,"NLCINDIA" ,"NMDC" ,"NOCIL" ,"NTPC" ,"NH" ,"NATIONALUM" ,"NFL" ,"NAVINFLUOR" ,"NAVNETEDUL" ,"NESTLEIND" ,"NETWORK18" ,"NILKAMAL" ,"NAM-INDIA" ,"OBEROIRLTY" ,"ONGC" ,"OIL" ,"OMAXE" ,"OFSS" ,"ORIENTCEM" ,"ORIENTELEC" ,"ORIENTREF" ,"PIIND" ,"PNBHOUSING" ,"PNCINFRA" ,"PSPPROJECT" ,"PTC" ,"PVR" ,"PAGEIND" ,"PERSISTENT" ,"PETRONET" ,"PFIZER" ,"PHILIPCARB" ,"PHOENIXLTD" ,"PIDILITIND" ,"PEL" ,"POLYMED" ,"POLYCAB" ,"POLYPLEX" ,"PFC" ,"POWERGRID" ,"PRAJIND" ,"PRESTIGE" ,"PRSMJOHNSN" ,"PGHL" ,"PGHH" ,"PNB" ,"QUESS" ,"RBLBANK" ,"RECLTD" ,"RITES" ,"RADICO" ,"RVNL" ,"RAIN" ,"RAJESHEXPO" ,"RALLIS" ,"RCF" ,"RATNAMANI" ,"RAYMOND" ,"REDINGTON" ,"RELAXO" ,"RELIANCE" ,"SBICARD" ,"SBILIFE" ,"SIS" ,"SJVN" ,"SKFINDIA" ,"SRF" ,"SANOFI" ,"SCHAEFFLER" ,"SCHNEIDER" ,"SEQUENT" ,"SFL" ,"SHILPAMED" ,"SCI" ,"SHOPERSTOP" ,"SHREECEM" ,"SHRIRAMCIT" ,"SRTRANSFIN" ,"SIEMENS" ,"SOBHA" ,"SOLARINDS" ,"SOLARA" ,"SONATSOFTW" ,"SOUTHBANK" ,"SPICEJET" ,"STARCEMENT" ,"SBIN" ,"SAIL" ,"SWSOLAR" ,"STLTECH" ,"STAR" ,"SUDARSCHEM" ,"SUMICHEM" ,"SPARC" ,"SUNPHARMA" ,"SUNTV" ,"SUNDARMFIN" ,"SUNDRMFAST" ,"SUNTECK" ,"SUPRAJIT" ,"SUPREMEIND" ,"SUPPETRO" ,"SUVENPHAR" ,"SUZLON" ,"SWANENERGY" ,"SWARAJENG" ,"SYMPHONY" ,"SYNGENE" ,"TCIEXP" ,"TCNSBRANDS" ,"TTKPRESTIG" ,"TVTODAY" ,"TV18BRDCST" ,"TVSMOTOR" ,"TASTYBITE" ,"TATACHEM" ,"TATACOFFEE" ,"TATACOMM" ,"TCS" ,"TATACONSUM" ,"TATAELXSI" ,"TATAINVEST" ,"TATAMTRDVR" ,"TATAMOTORS" ,"TATAPOWER" ,"TATASTLBSL" ,"TATASTEEL" ,"TEAMLEASE" ,"TECHM" ,"NIACL" ,"RAMCOCEM" ,"THERMAX" ,"THYROCARE" ,"TIMKEN" ,"TITAN" ,"TORNTPHARM" ,"TORNTPOWER" ,"TRENT" ,"TRIDENT" ,"TIINDIA" ,"UCOBANK" ,"UFLEX" ,"UPL" ,"UJJIVAN" ,"UJJIVANSFB" ,"ULTRACEMCO" ,"UNIONBANK" ,"UBL" ,"MCDOWELL-N" ,"VGUARD" ,"VMART" ,"VIPIND" ,"VRLLOG" ,"VSTIND" ,"VAIBHAVGBL" ,"VAKRANGEE" ,"VTL" ,"VARROC" ,"VBL" ,"VENKEYS" ,"VINATIORGA" ,"IDEA" ,"VOLTAS" ,"WABCOINDIA" ,"WELCORP" ,"WELSPUNIND" ,"WESTLIFE" ,"WHIRLPOOL" ,"WIPRO" ,"WOCKPHARMA" ,"YESBANK" ,"ZEEL" ,"ZENSARTECH" ,"ZYDUSWELL" ,"ECLERX"];
fno_list = nifty200;
# fno_list = nifty500;
# fno_list= list(fno_lot.keys());


global df,historic_data,x,y,mapping,mn,mx, maxY,minY ,mindate, maxdate, closingPrice,STOCK

def callMain():
    for stk in fno_list:
        try:
            mapping = getMaxMin(stk);
            #print(mapping)
            localMax,localMin,nr,count,trend = getNR(mapping);
            if(count > 0 and trend > 1):
                print("STK: {}\nMax {}\nMin {}\nNR {}\nCount {}\nTrend {}\n".format(stk,localMax,localMin,nr,count,trend))

        except:
            #print(stk);
            pass
CLOSE = 1;
HIGH = 2;
#getNRone()
callMain();


    


