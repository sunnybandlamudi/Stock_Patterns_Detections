from nsetools import nse;
from threading import Thread
import numpy as np;
import pandas as pd;
import  os;
import  functools;
import requests as req;
from datetime import date,timedelta,datetime;
import math #needed for definition of pi

#https://query2.finance.yahoo.com/v8/finance/chart/SBIN.NS?interval=1d&period1=1581773796&period2=1613396196

def getYahooData(stock):

    if containsIndex:
        stock = stock
    else:
        stock = stock+'.NS'

    params = {
        'interval':INTERVAL,
        'period1': int((datetime.today() - timedelta(FROM)).timestamp()),
        'period2': int((datetime.today()).timestamp())
    }

    data = req.get('https://query2.finance.yahoo.com/v8/finance/chart/'+stock,params = params,headers = head)
    # print(data);
    if(data.status_code  == 422):
        print(data.content)
    close = data.json()['chart']['result'][0]['indicators']['quote'][0]['close'][::-1];
    high = data.json()['chart']['result'][0]['indicators']['quote'][0]['high'][::-1];
    low = data.json()['chart']['result'][0]['indicators']['quote'][0]['low'][::-1];
    open = data.json()['chart']['result'][0]['indicators']['quote'][0]['open'][::-1];
    volume = data.json()['chart']['result'][0]['indicators']['quote'][0]['volume'][::-1];
    timestamp = data.json()['chart']['result'][0]['timestamp'][::-1];
    if containsIndex:
        timestamp = list(map( lambda item: datetime.fromtimestamp(item).strftime(FORMAT),timestamp));
    else:
        timestamp = list(map( lambda item: datetime.fromtimestamp(item).strftime(FORMAT),timestamp));
    data = list(zip(timestamp,close,open,high,low,volume));
    data = list(filter(lambda item: item[0] and item[1] and item[2] and item[3],data))
    return data

def spreadPercent(up, lo):
    return abs(up-lo)*100/lo

def isBulishOrHammer(candle):
    isGreen = candle[CLOSE] > candle[OPEN]
    upperTail = candle[HIGH] - candle[CLOSE];
    lowerTail = candle[OPEN] - candle[LOW];
    spread = candle[CLOSE] - candle[OPEN];
    spreadPercentage = spreadPercent(candle[CLOSE], candle[OPEN])
    tailPercent = spreadPercent(candle[CLOSE], candle[OPEN])
    if( isGreen ):
        if(spread > 2*(upperTail+lowerTail) and spreadPercentage > 1):
            # print("bulish",candle)
            return True
        elif(lowerTail > 3*upperTail and tailPercent > 1):
            # print("Hammer",candle)
            return True
        return  True;
    return False

def getNR(mapping):
    maxpoint = None;
    localMax = []
    obj = None;
    avgVolume = sum(map(lambda item: item[VOLUME],mapping[100:]))/len(mapping[100:]);
    mapping = list(reversed(mapping[:100]))

    for i in range(1,len(mapping)-1):
        current = mapping[i];
        count = 0 ;
        # added to get the trend 5 days before
        if(CHECK_PAST_TREND and current[CLOSE] < max(map(lambda item: item[CLOSE] ,mapping[i if i-PAST_TREND_NUMBER > i-PAST_TREND_NUMBER else 0:i]))):
            continue;

        for j in range(i+1,len(mapping)):
            if(getPercent(current[HIGH],BREAKOUTPERCENT) > mapping[j][HIGH] and current[LOW] < mapping[j][LOW]):
                count += 1;
            else:
                if((count > MIN_BREAKOUT_SIZE) and (not CHECK_AVERAGE or (CHECK_AVERAGE and mapping[j][VOLUME] >= avgVolume))):
                    obj = {
                        'current':current,
                        'last': mapping[j],
                        'count': count
                    }
                break;
            if(not BREAKOUT and count > MIN_BREAKOUT_SIZE ):
                obj = {
                    'current':current,
                    'last': mapping[j],
                    'count': count
                }
    return  obj

def getMinMax(mapping):
    localMax = [];
    localMin = [];
    for j in range(2,len(mapping)-2):
        if( (mapping[j-1][CLOSE] < mapping[j][CLOSE] > mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] < mapping[j][CLOSE] > mapping[j+2][CLOSE])):
            localMax.append(mapping[j]);
        elif( (mapping[j-1][CLOSE] > mapping[j][CLOSE] < mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] > mapping[j][CLOSE] < mapping[j+2][CLOSE])):
            localMin.append(mapping[j]);
    current = mapping[0]
    total = [*localMax,*localMin];
    total.sort(key= lambda item:datetime.strptime(item[0],FORMAT))
    return total;

def flagPattern(mapping):
    min_max = getMinMax(mapping);
    obj = None
    # print(min_max)
    for i in range(len(min_max)-1):
        percent_change = (min_max[i+1][CLOSE] - min_max[i][CLOSE])/min_max[i][CLOSE]
        percent_change *= 100;
        if(percent_change > BREAKOUTPERCENT):
            # print(min_max[i+1])
            local_low = min_max[i];
            local_high = min_max[i+1];
            mapping = mapping[::-1]
            index = mapping.index(min_max[i+1]);
            lower_quartile = getPercent(min_max[i+1][CLOSE], -(percent_change/3));
            upper_quartile = getPercent(min_max[i+1][CLOSE],1);
            count = 0;

            if(index):
                for i in range(index,len(mapping)):
                    if( lower_quartile < mapping[i][CLOSE] < upper_quartile):
                            count += 1;
                            if(count > MIN_BREAKOUT_SIZE and mapping[i][CLOSE] > lower_quartile and BREAKOUT == False):
                                obj = {
                                    'flag_high': local_high,
                                    'flag_start':local_low,
                                    'break_out':mapping[i],
                                    'count': count
                                }
                            continue;
                    else:
                        if(count > MIN_BREAKOUT_SIZE and mapping[i][CLOSE] > lower_quartile):
                            # print('breakup happened' , mapping[i])
                            obj = {
                                'flag_high': local_high,
                                'flag_start':local_low,
                                'break_out':mapping[i],
                                'count': count
                            }
                        break;

    return obj;








    # for j in range(2,len(mapping)-30):
    #     if( (mapping[j-1][CLOSE] > mapping[j][CLOSE] < mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] > mapping[j][CLOSE] < mapping[j+2][CLOSE])):
    #         localMin = mapping[j]
    #         break;
    # for j in range(2,len(mapping)-30):
    #     if( (mapping[j-1][CLOSE] < mapping[j][CLOSE] > mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] < mapping[j][CLOSE] > mapping[j+2][CLOSE])):
    #         localMax.append(mapping[j])
    # count = 0;
    # for i in range(len(mapping)):
    #     if(localMin[CLOSE] < mapping[i][CLOSE] < localMax[0][CLOSE]):
    #         count+=1;
    #     else:
    #         nr = mapping[i]
    #         break;
    # trend = 1;
    # for i in range(1,len(localMax)):
    #     if(localMax[i-1][CLOSE] > localMax[i][CLOSE]):
    #         trend += 1;
    #     else:
    #         break;
    # return localMax[0],localMin,nr,count,trend;

def getPercent(price,n):
    return price+(price*n)/100;


def rectangle(mapping):
    localMax = [];
    localMin = [];
    for j in range(2,len(mapping)-2):
        if( (mapping[j-1][CLOSE] < mapping[j][CLOSE] > mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] < mapping[j][CLOSE] > mapping[j+2][CLOSE])):
            localMax.append(mapping[j]);
        elif( (mapping[j-1][CLOSE] > mapping[j][CLOSE] < mapping[j+1][CLOSE]) and (mapping[j-2][CLOSE] > mapping[j][CLOSE] < mapping[j+2][CLOSE])):
            localMin.append(mapping[j]);
    current = mapping[0]
    lowPercent = getPercent(current[CLOSE],-PRECENT);
    highPercent = getPercent(current[CLOSE],PRECENT);
    count = 1;
    total = [*localMax,*localMin];
    total.sort(key= lambda item:datetime.strptime(item[0],FORMAT),reverse=True)
    line = [];

    for i in range(len(total)):
        if (
                # lowPercent < localMax[i][HIGH] < highPercent or
                # lowPercent < localMax[i][HIGH]+getPercent(localMax[i][HIGH] , PRECENT) < highPercent or
                # lowPercent < localMax[i][HIGH]+getPercent(localMax[i][HIGH] , -PRECENT) < highPercent or
                lowPercent < total[i][CLOSE] < highPercent or
                lowPercent < total[i][CLOSE] + getPercent(current[CLOSE], PRECENT) < highPercent or
                lowPercent < total[i][CLOSE] + getPercent(current[CLOSE], -PRECENT) < highPercent
        ):
            line.append(total[i])
    return (line);

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

# req = req.Session()
# req.get('https://in.finance.yahoo.com/',headers=head)
# req.get('https://www.nseindia.com',headers=head)

fno = nse.Nse()
fno_lot = fno.get_fno_lot_sizes(as_json=False);
nifty200 = ["3MINDIA","ABB","POWERINDIA","ACC","AIAENG","APLAPOLLO","AUBANK","AARTIDRUGS","AARTIIND","AAVAS","ABBOTINDIA","ADANIENT","ADANIGREEN","ADANIPORTS","ATGL","ADANITRANS","ABCAPITAL","ABFRL","ADVENZYMES","AEGISCHEM","AFFLE","AJANTPHARM","AKZOINDIA","ALEMBICLTD","APLLTD","ALKEM","ALKYLAMINE","ALOKINDS","AMARAJABAT","AMBER","AMBUJACEM","ANGELBRKG","APOLLOHOSP","APOLLOTYRE","ASAHIINDIA","ASHOKLEY","ASHOKA","ASIANPAINT","ASTERDM","ASTRAZEN","ASTRAL","ATUL","AUROPHARMA","AVANTIFEED","DMART","AXISBANK","BASF","BEML","BSE","BAJAJ-AUTO","BAJAJCON","BAJAJELEC","BAJFINANCE","BAJAJFINSV","BAJAJHLDNG","BALAMINES","BALKRISIND","BALMLAWRIE","BALRAMCHIN","BANDHANBNK","BANKBARODA","BANKINDIA","MAHABANK","BATAINDIA","BAYERCROP","BERGEPAINT","BDL","BEL","BHARATFORG","BHEL","BPCL","BHARATRAS","BHARTIARTL","BIOCON","BIRLACORPN","BSOFT","BLISSGVS","BLUEDART","BLUESTARCO","BBTC","BOSCHLTD","BRIGADE","BRITANNIA","CCL","CESC","CRISIL","CSBBANK","CADILAHC","CANFINHOME","CANBK","CAPLIPOINT","CGCL","CARBORUNIV","CASTROLIND","CEATLTD","CENTRALBK","CDSL","CENTURYPLY","CENTURYTEX","CERA","CHALET","CHAMBLFERT","CHOLAHLDNG","CHOLAFIN","CIPLA","CUB","COALINDIA","COCHINSHIP","COFORGE","COLPAL","CAMS","CONCOR","COROMANDEL","CREDITACC","CROMPTON","CUMMINSIND","CYIENT","DCBBANK","DCMSHRIRAM","DLF","DABUR","DALBHARAT","DEEPAKNTR","DELTACORP","DHANI","DHANUKA","DBL","DISHTV","DCAL","DIVISLAB","DIXON","LALPATHLAB","DRREDDY","EIDPARRY","EIHOTEL","EPL","EDELWEISS","EICHERMOT","ELGIEQUIP","EMAMILTD","ENDURANCE","ENGINERSIN","EQUITAS","ERIS","ESCORTS","EXIDEIND","FDC","FEDERALBNK","FINEORG","FINCABLES","FINPIPE","FSL","FORTIS","FCONSUMER","FRETAIL","GAIL","GEPIL","GHCL","GMMPFAUDLR","GMRINFRA","GALAXYSURF","GRSE","GARFIBRES","GICRE","GILLETTE","GLAXO","GLENMARK","GODFRYPHLP","GODREJAGRO","GODREJCP","GODREJIND","GODREJPROP","GRANULES","GRAPHITE","GRASIM","GESHIP","GREAVESCOT","GRINDWELL","GUJALKALI","GAEL","FLUOROCHEM","GUJGASLTD","GNFC","GPPL","GSFC","GSPL","GULFOILLUB","HEG","HCLTECH","HDFCAMC","HDFCBANK","HDFCLIFE","HFCL","HAPPSTMNDS","HATSUN","HAVELLS","HEIDELBERG","HEMIPROP","HEROMOTOCO"];
# nifty500 =  ["3MINDIA" ,"ABB" ,"POWERINDIA" ,"ACC" ,"AIAENG" ,"APLAPOLLO" ,"AUBANK" ,"AARTIDRUGS" ,"AARTIIND" ,"AAVAS" ,"ABBOTINDIA" ,"ADANIENT" ,"ADANIGREEN" ,"ADANIPORTS" ,"ATGL" ,"ADANITRANS" ,"ABCAPITAL" ,"ABFRL" ,"ADVENZYMES" ,"AEGISCHEM" ,"AFFLE" ,"AJANTPHARM" ,"AKZOINDIA" ,"ALEMBICLTD" ,"APLLTD" ,"ALKEM" ,"ALKYLAMINE" ,"ALOKINDS" ,"AMARAJABAT" ,"AMBER" ,"AMBUJACEM" ,"ANGELBRKG" ,"APOLLOHOSP" ,"APOLLOTYRE" ,"ASAHIINDIA" ,"ASHOKLEY" ,"ASHOKA" ,"ASIANPAINT" ,"ASTERDM" ,"ASTRAZEN" ,"ASTRAL" ,"ATUL" ,"AUROPHARMA" ,"AVANTIFEED" ,"DMART" ,"AXISBANK" ,"BASF" ,"BEML" ,"BSE" ,"BAJAJ-AUTO" ,"BAJAJCON" ,"BAJAJELEC" ,"BAJFINANCE" ,"BAJAJFINSV" ,"BAJAJHLDNG" ,"BALAMINES" ,"BALKRISIND" ,"BALMLAWRIE" ,"BALRAMCHIN" ,"BANDHANBNK" ,"BANKBARODA" ,"BANKINDIA" ,"MAHABANK" ,"BATAINDIA" ,"BAYERCROP" ,"BERGEPAINT" ,"BDL" ,"BEL" ,"BHARATFORG" ,"BHEL" ,"BPCL" ,"BHARATRAS" ,"BHARTIARTL" ,"BIOCON" ,"BIRLACORPN" ,"BSOFT" ,"BLISSGVS" ,"BLUEDART" ,"BLUESTARCO" ,"BBTC" ,"BOSCHLTD" ,"BRIGADE" ,"BRITANNIA" ,"CCL" ,"CESC" ,"CRISIL" ,"CSBBANK" ,"CADILAHC" ,"CANFINHOME" ,"CANBK" ,"CAPLIPOINT" ,"CGCL" ,"CARBORUNIV" ,"CASTROLIND" ,"CEATLTD" ,"CENTRALBK" ,"CDSL" ,"CENTURYPLY" ,"CENTURYTEX" ,"CERA" ,"CHALET" ,"CHAMBLFERT" ,"CHOLAHLDNG" ,"CHOLAFIN" ,"CIPLA" ,"CUB" ,"COALINDIA" ,"COCHINSHIP" ,"COFORGE" ,"COLPAL" ,"CAMS" ,"CONCOR" ,"COROMANDEL" ,"CREDITACC" ,"CROMPTON" ,"CUMMINSIND" ,"CYIENT" ,"DCBBANK" ,"DCMSHRIRAM" ,"DLF" ,"DABUR" ,"DALBHARAT" ,"DEEPAKNTR" ,"DELTACORP" ,"DHANI" ,"DHANUKA" ,"DBL" ,"DISHTV" ,"DCAL" ,"DIVISLAB" ,"DIXON" ,"LALPATHLAB" ,"DRREDDY" ,"EIDPARRY" ,"EIHOTEL" ,"EPL" ,"EDELWEISS" ,"EICHERMOT" ,"ELGIEQUIP" ,"EMAMILTD" ,"ENDURANCE" ,"ENGINERSIN" ,"EQUITAS" ,"ERIS" ,"ESCORTS" ,"EXIDEIND" ,"FDC" ,"FEDERALBNK" ,"FINEORG" ,"FINCABLES" ,"FINPIPE" ,"FSL" ,"FORTIS" ,"FCONSUMER" ,"FRETAIL" ,"GAIL" ,"GEPIL" ,"GHCL" ,"GMMPFAUDLR" ,"GMRINFRA" ,"GALAXYSURF" ,"GRSE" ,"GARFIBRES" ,"GICRE" ,"GILLETTE" ,"GLAXO" ,"GLENMARK" ,"GODFRYPHLP" ,"GODREJAGRO" ,"GODREJCP" ,"GODREJIND" ,"GODREJPROP" ,"GRANULES" ,"GRAPHITE" ,"GRASIM" ,"GESHIP" ,"GREAVESCOT" ,"GRINDWELL" ,"GUJALKALI" ,"GAEL" ,"FLUOROCHEM" ,"GUJGASLTD" ,"GNFC" ,"GPPL" ,"GSFC" ,"GSPL" ,"GULFOILLUB" ,"HEG" ,"HCLTECH" ,"HDFCAMC" ,"HDFCBANK" ,"HDFCLIFE" ,"HFCL" ,"HAPPSTMNDS" ,"HATSUN" ,"HAVELLS" ,"HEIDELBERG" ,"HEMIPROP" ,"HEROMOTOCO" ,"HSCL" ,"HINDALCO" ,"HAL" ,"HINDCOPPER" ,"HINDPETRO" ,"HINDUNILVR" ,"HINDZINC" ,"HONAUT" ,"HUDCO" ,"HDFC" ,"HUHTAMAKI" ,"ICICIBANK" ,"ICICIGI" ,"ICICIPRULI" ,"ISEC" ,"IDBI" ,"IDFCFIRSTB" ,"IDFC" ,"IFBIND" ,"IIFL" ,"IIFLWAM" ,"IOLCP" ,"IRB" ,"IRCON" ,"ITC" ,"ITI" ,"INDIACEM" ,"IBULHSGFIN" ,"IBREALEST" ,"INDIAMART" ,"INDIANB" ,"IEX" ,"INDHOTEL" ,"IOC" ,"IOB" ,"IRCTC" ,"ICIL" ,"INDOCO" ,"IGL" ,"INDUSTOWER" ,"INDUSINDBK" ,"NAUKRI" ,"INFY" ,"INGERRAND" ,"INOXLEISUR" ,"INTELLECT" ,"INDIGO" ,"IPCALAB" ,"JBCHEPHARM" ,"JKCEMENT" ,"JKLAKSHMI" ,"JKPAPER" ,"JKTYRE" ,"JMFINANCIL" ,"JSWENERGY" ,"JSWSTEEL" ,"JTEKTINDIA" ,"JAMNAAUTO" ,"JINDALSAW" ,"JSLHISAR" ,"JSL" ,"JINDALSTEL" ,"JCHAC" ,"JUBLFOOD" ,"JUSTDIAL" ,"JYOTHYLAB" ,"KPRMILL" ,"KEI" ,"KNRCON" ,"KPITTECH" ,"KRBL" ,"KSB" ,"KAJARIACER" ,"KALPATPOWR" ,"KANSAINER" ,"KARURVYSYA" ,"KSCL" ,"KEC" ,"KOTAKBANK" ,"L&TFH" ,"LTTS" ,"LICHSGFIN" ,"LAOPALA" ,"LAXMIMACH" ,"LTI" ,"LT" ,"LAURUSLABS" ,"LEMONTREE" ,"LINDEINDIA" ,"LUPIN" ,"LUXIND" ,"MASFIN" ,"MMTC" ,"MOIL" ,"MRF" ,"MGL" ,"MAHSCOOTER" ,"MAHSEAMLES" ,"M&MFIN" ,"M&M" ,"MAHINDCIE" ,"MHRIL" ,"MAHLOG" ,"MANAPPURAM" ,"MRPL" ,"MARICO" ,"MARUTI" ,"MFSL" ,"MAXHEALTH" ,"MAZDOCK" ,"METROPOLIS" ,"MINDTREE" ,"MINDACORP" ,"MINDAIND" ,"MIDHANI" ,"MOTHERSUMI" ,"MOTILALOFS" ,"MPHASIS" ,"MCX" ,"MUTHOOTFIN" ,"NATCOPHARM" ,"NBCC" ,"NCC" ,"NESCO" ,"NHPC" ,"NLCINDIA" ,"NMDC" ,"NOCIL" ,"NTPC" ,"NH" ,"NATIONALUM" ,"NFL" ,"NAVINFLUOR" ,"NESTLEIND" ,"NETWORK18" ,"NILKAMAL" ,"NAM-INDIA" ,"OBEROIRLTY" ,"ONGC" ,"OIL" ,"OFSS" ,"ORIENTELEC" ,"ORIENTREF" ,"PIIND" ,"PNBHOUSING" ,"PNCINFRA" ,"PVR" ,"PAGEIND" ,"PERSISTENT" ,"PETRONET" ,"PFIZER" ,"PHILIPCARB" ,"PHOENIXLTD" ,"PIDILITIND" ,"PEL" ,"POLYMED" ,"POLYCAB" ,"POLYPLEX" ,"PFC" ,"POWERGRID" ,"PRESTIGE" ,"PRINCEPIPE" ,"PRSMJOHNSN" ,"PGHL" ,"PGHH" ,"PNB" ,"QUESS" ,"RBLBANK" ,"RECLTD" ,"RITES" ,"RADICO" ,"RVNL" ,"RAIN" ,"RAJESHEXPO" ,"RALLIS" ,"RCF" ,"RATNAMANI" ,"RAYMOND" ,"REDINGTON" ,"RELAXO" ,"RELIANCE" ,"RESPONIND" ,"ROSSARI" ,"ROUTE" ,"SBICARD" ,"SBILIFE" ,"SIS" ,"SJVN" ,"SKFINDIA" ,"SRF" ,"SANOFI" ,"SCHAEFFLER" ,"SCHNEIDER" ,"SEQUENT" ,"SHARDACROP" ,"SFL" ,"SHILPAMED" ,"SCI" ,"SHOPERSTOP" ,"SHREECEM" ,"SHRIRAMCIT" ,"SRTRANSFIN" ,"SIEMENS" ,"SOBHA" ,"SOLARINDS" ,"SOLARA" ,"SONATSOFTW" ,"SPANDANA" ,"SPICEJET" ,"STARCEMENT" ,"SBIN" ,"SAIL" ,"SWSOLAR" ,"STLTECH" ,"STAR" ,"SUDARSCHEM" ,"SUMICHEM" ,"SPARC" ,"SUNPHARMA" ,"SUNTV" ,"SUNCLAYLTD" ,"SUNDARMFIN" ,"SUNDRMFAST" ,"SUNTECK" ,"SUPRAJIT" ,"SUPREMEIND" ,"SUPPETRO" ,"SUVENPHAR" ,"SUZLON" ,"SWANENERGY" ,"SYMPHONY" ,"SYNGENE" ,"TCIEXP" ,"TCNSBRANDS" ,"TTKPRESTIG" ,"TV18BRDCST" ,"TVSMOTOR" ,"TANLA" ,"TASTYBITE" ,"TATACHEM" ,"TATACOFFEE" ,"TATACOMM" ,"TCS" ,"TATACONSUM" ,"TATAELXSI" ,"TATAINVEST" ,"TATAMTRDVR" ,"TATAMOTORS" ,"TATAPOWER" ,"TATASTLBSL" ,"TATASTEEL" ,"TEAMLEASE" ,"TECHM" ,"NIACL" ,"RAMCOCEM" ,"THERMAX" ,"THYROCARE" ,"TIMKEN" ,"TITAN" ,"TORNTPHARM" ,"TORNTPOWER" ,"TRENT" ,"TRIDENT" ,"TRITURBINE" ,"TIINDIA" ,"UCOBANK" ,"UFLEX" ,"UPL" ,"UTIAMC" ,"UJJIVAN" ,"UJJIVANSFB" ,"ULTRACEMCO" ,"UNIONBANK" ,"UBL" ,"MCDOWELL-N" ,"VGUARD" ,"VMART" ,"VIPIND" ,"VSTIND" ,"VAIBHAVGBL" ,"VAKRANGEE" ,"VALIANTORG" ,"VTL" ,"VARROC" ,"VBL" ,"VEDL" ,"VENKEYS" ,"VINATIORGA" ,"IDEA" ,"VOLTAS" ,"WABCOINDIA" ,"WELCORP" ,"WELSPUNIND" ,"WESTLIFE" ,"WHIRLPOOL" ,"WIPRO" ,"WOCKPHARMA" ,"YESBANK" ,"ZEEL" ,"ZENSARTECH" ,"ZYDUSWELL" ,"ECLERX"]
# fno_list = nifty200;
# fno_list = nifty500;
fno_list= list(fno_lot.keys());
# fno_list = ['^NSEI','^NSEBANK']

def dateCountCompare(item1, item2):
    if(datetime.strptime(item1['break_out'][0],FORMAT) < datetime.strptime(item2['break_out'][0],FORMAT)):
        return 1;
    elif(datetime.strptime(item1['break_out'][0],FORMAT) == datetime.strptime(item2['break_out'][0],FORMAT) ):
        return  item2['count'] - item1['count'];
    else:
        return -1;

def writetofile(items):
    with open('stocks.txt','w') as f:
        for item in items:
            data = '\n{} - {:.2f}\nFlag-Start  {} - {:.2f}\nFlag-End  {} - {:.2f}\nBreak Out  {} - {:.2f}\nCount {}'.format(item['stk'],item['lastPrice'],item['flag_start'][0],item['flag_start'][1],item['flag_high'][0],item['flag_high'][1],item['break_out'][0],item['break_out'][1],item['count'])
            print(data)
            f.write(data)
            if(item['sr']):
                for dt in item['sr']:
                    tr = '- Bullish' if isBulishOrHammer(dt) else ""
                    bldata = "\n( {} {:.2f} {:.2f} {:.2f} {:.2f} ) {}".format(*dt[0:5],tr);
                    print(bldata)
                    f.write(bldata)
        pass

def callMain(*STOCK):
    items = []
    stock_list = fno_list;
    if(bool(STOCK)):
        stock_list = list(STOCK)
    for stk in stock_list:
        try:
            # thread  = Thread(target = getYahooData,args=(stk,))
            # thread.start();
            # mapping = thread.join();
            print(stk,end=',')
            mapping = getYahooData(stk);
            obj = flagPattern(mapping)
            # obj = getNR(mapping)

            if(obj):
                obj['stk'] = stk;
                obj['lastPrice'] = mapping[0][1];
                # print(obj['stk'],obj['count'],obj['flag_high'])
                items.append(obj);
                sr = rectangle(mapping)
                obj['sr'] = sr;


        except :
            #print(stk);
            pass
    items = sorted(items,key=functools.cmp_to_key(dateCountCompare));

    # for item in items:
    #     print('\n{} - {:.2f}\nFlag-Start  {} - {:.2f}\nFlag-End  {} - {:.2f}\nBreak Out  {} - {:.2f}\nCount {}'.format(item['stk'],item['lastPrice'],item['flag_start'][0],item['flag_start'][1],item['flag_high'][0],item['flag_high'][1],item['break_out'][0],item['break_out'][1],item['count']))
    #     if(item['sr']):
    #         for dt in item['sr']:
    #             tr = '- Bullish' if isBulishOrHammer(dt) else ""
    #             print("( {} {:.2f} {:.2f} {:.2f} {:.2f} ) {}".format(*dt[0:5],tr))

    writetofile(items);


CLOSE = 1;
OPEN = 2;
HIGH = 3;
LOW = 4;
VOLUME = 5;

FORMAT = "%d-%m-%Y";
INTERVAL = '1d'
FROM = 100;
PRECENT = 0.5;
BREAKOUT = True;
BREAKOUTPERCENT = 15;
MIN_BREAKOUT_SIZE = 5;
PAST_TREND_NUMBER = 10;
CHECK_PAST_TREND = True
CHECK_AVERAGE = True

containsIndex = '^NSEI' in fno_list;

if INTERVAL in ['1d' , '1wk']:
    FORMAT = "%d-%m-%Y";
else:
    FORMAT = "%d-%m-%Y %H:%M";

#getNRone()

# callMain('TRENT','ITC');
# callMain('HAPPSTMNDS');
callMain();
