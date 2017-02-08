import json, urllib2, hashlib,struct,sha,time, sys
import logging
import logging.handlers
import ConfigParser

#import msvcrt

import smtplib
from email.mime.text import MIMEText
from email.header import Header

cancalTime_BuyOrder = 5
cancalTime_SellOrder = 10
#access_key_chbtc    = 'bd3cd9b0-c244-49b1-8f4f-a559202368f1'
#access_secret_chbtc = '065dea3c-eaa3-4fd7-9004-7530a277e656'

access_key_chbtc    = '1ec4b319-74fb-4751-bc8f-8cdf92a73a50'
access_secret_chbtc = '61e66f7c-536b-4fd8-b157-731501ff587f'

 

'''
class btcc_api:

    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey)
        value  = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue)
        print (value)
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params+= '&sign=%s&reqTime=%d'%(sign, reqTime)
            #url = 'https://trade.chbtc.com/api/' + path + '?' + params
            url = "https://data.btcchina.com/data/ticker?market=btccny"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
            #return response.read()
        except Exception(ex):
            print >>sys.stderr, 'chbtc request ex: ', ex
            return None

    def query_market(self):
        try:
            url = "https://data.btcchina.com/data/ticker?market=btccny"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=3)
            obj = json.loads(response.read())
            
            return obj
        except Exception,ex:
            print >>sys.stderr, 'chbtc query_account exception,',ex
            return "error"
'''

class Logger():
    def __init__(self, logname, loglevel, logger):
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #formatter = logging.format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger

class chbtc_api:

    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey)
        value  = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue)
        print (value)
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params+= '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.chbtc.com/api/' + path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
            #return response.read()
        except Exception,ex:
            print >>sys.stderr, 'chbtc request ex: ', ex
            return "error"

    def query_account(self):
        try:
            params = "method=getAccountInfo&accesskey="+self.mykey
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            return obj
        except Exception,ex:
            print >>sys.stderr, 'chbtc query_account exception,',ex
            return "error"

    def sell_order(self, price, amount):
        try:
            params = "method=order&accesskey="+self.mykey+"&price=" + price + "&amount=" + amount + "&tradeType=0&currency=btc_cny"
            path = 'order'

            obj = self.__api_call(path, params)
            if obj["code"] != 1000 :
                logger.error('sell_order : %s : %s', obj["code"], obj["message"])
                return "error"
            return obj
        except Exception,ex:
            print >>sys.stderr, 'chbtc sell_order exception,',ex
            return "error"
        
    def buy_order(self, price, amount):
        try:
            params = "method=order&accesskey="+self.mykey+"&price=" + price + "&amount=" + amount + "&tradeType=1&currency=btc_cny"
            path = 'order'

            obj = self.__api_call(path, params)
            if obj["code"] != 1000 :
                logger.error('buy_order : %s : %s', obj["code"], obj["message"])
                return "error"
            return obj
        except Exception , ex:
            print >>sys.stderr, 'chbtc buy_order exception,',ex
            return "error"

    def cancel_order(self, orderId):
        try:
            params = "method=cancelOrder&accesskey="+self.mykey+"&id=" + orderId + "&currency=btc_cny"
            path = 'cancelOrder'
            obj = self.__api_call(path, params)
            
            if obj["code"] != 1000 :
                logger.error('cannel_order : %s : %s : %s', orderId, obj["code"], obj["message"])
                return "error"
            return obj
        
        except Exception , ex:
            print >>sys.stderr, 'chbtc cannel_order exception,',ex
            return "error"

    def query_order(self, orderId):
        try:
            params = "method=getOrder&accesskey="+self.mykey+"&id=" + orderId + "&currency=btc_cny"
            path = 'getOrder'
            obj = self.__api_call(path, params)
            return obj
        
        except Exception , ex:
            print >>sys.stderr, 'chbtc query_order exception,',ex
            return "error"

    def query_market(self):
        try:
            url = "http://api.chbtc.com/data/v1/ticker?currency=btc_cny"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=3)
            obj = json.loads(response.read())
            return obj
        except Exception,ex:
            print >>sys.stderr, 'chbtc query_market exception,',ex
            return "error"

    def query_depth(self):
        try:
            url = "http://api.chbtc.com/data/v1/depth?currency=btc_cny&size=5&merge=1"
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=3)
            obj = json.loads(response.read())            
            return obj
        except Exception,ex:
            print >>sys.stderr, 'chbtc query_depth exception,',ex
            return "error"


logger = Logger(logname='log.txt', loglevel=1, logger="CHBTC").getlog() 

if __name__ == '__main__':
    
    cf = ConfigParser.ConfigParser()

    cf.read("Info.conf")

    cancalTime_BuyOrder = cf.get("globe", "cancalTime_BuyOrder")
    cancalTime_SellOrder = cf.get("globe", "cancalTime_SellOrder")
    winPer = cf.get("globe", "winPer")
    lossPer = cf.get("globe", "lossPer")
    everydaytask = cf.get("globe", "everydaytask")

    access_key_chbtc    = cf.get("xiongding@gmail.com", "access_key")
    access_secret_chbtc = cf.get("xiongding@gmail.com", "access_secret")
    initial_value = cf.get("xiongding@gmail.com", "initial_value")
    startworktime = cf.get("xiongding@gmail.com", "startworktime")
    stopworktime = cf.get("xiongding@gmail.com", "stopworktime")
    startworkvalue = cf.get("xiongding@gmail.com", "startworkvalue")
    stopworkvalue = cf.get("xiongding@gmail.com", "stopworkvalue")

    if startworkvalue == "" :
        startworkvalue = initial_value
        cf.set("xiongding@gmail.com", "startworkvalue", (startworkvalue))

    cf.set("xiongding@gmail.com", "startworktime", (int)(time.time()*1000))
    cf.write(open("info.conf", "w"))

    
    max_value = 0.0
    
    chbtc = chbtc_api(access_key_chbtc, access_secret_chbtc)

    CHBTC_BigThan_BTCC = 0
    BTCC_BigThan_CHBTC = 0

    CHBTC_BigThan_BTCC_Total = 0.0
    BTCC_BigThan_CHBTC_Total = 0.0

    CHBTC_Asks_Depth = 0.0
    CHBTC_Bids_Depth = 0.0

    orderPrice = 0.0
    curMoney_CNY = 0.0
    curMoney_BTC = 0.0
    
    totalAssets = 0.0

    sell_order_id = 0
    buy_order_id = 0
    sell_order_state = 0
    sell_order_timer = 0
    buy_order_state = 0
    buy_order_timer = 0

    totalAssets = 0
    timestamp = 0

#    done = False
#while not done:
while 1:
    '''
    if msvcrt.kbhit():
        print "you pressed",msvcrt.getch(),"so now i will quit"
        cf.set("xiongding@gmail.com", "stopworkvalue", (totalAssets))
        cf.write(open("info.conf", "w"))
        break 
        #done = True
    '''
    
    txtJson = chbtc.query_account()

    if txtJson == "error" :
        continue
    
    curMoney_CNY = txtJson["result"]["balance"]["CNY"]["amount"]
    curMoney_BTC = txtJson["result"]["balance"]["BTC"]["amount"]
    totalAssets = txtJson["result"]["totalAssets"]
    #if totalAssets > max_value :
    #    max_value = totalAssets

    if float(totalAssets) > float(initial_value) * float(winPer) and buy_order_id == 0 and sell_order_id == 0 : 
        logger.info('I win money : 10% ')
        break
    elif float(totalAssets) < float(startworkvalue) * float(lossPer) : 
        chbtc.cancel_order(str(buy_order_id))
        chbtc.cancel_order(str(sell_order_id))
        chbtc.sell_order(str(1000), str(("%.3f" % (curMoney_BTC))))
        logger.info("I lost money : 5% : %s : %s", str(startworkvalue), str(totalAssets))
        break
    elif float(totalAssets) > float(startworkvalue) + float(everydaytask) and buy_order_id == 0 and sell_order_id == 0 and curMoney_BTC == 0:
        cf.set("xiongding@gmail.com", "stopworkvalue", (totalAssets))
        cf.set("xiongding@gmail.com", "stopworktime", (int)(time.time()*1000))
        stopworktime = (int)(time.time()*1000)
        logger.info("I done my daily work : %s : %s : %s : %s ", str(startworkvalue), str(totalAssets), str(startworktime), str(stopworktime))
        startworkvalue = stopworkvalue
        cf.write(open("info.conf", "w"))
        while 1:
            time.sleep(600)
            if (int)(time.time()*1000) > (stopworktime + (3600 * 1000 * 24)):
                startworktime = (int)(time.time()*1000)
                cf.set("xiongding@gmail.com", "startworktime", startworktime)
                cf.write(open("info.conf", "w"))
                break
            
    elif (int)(time.time()*1000) - (int)(startworktime) > (3600 * 1000 * 24) :
        logger.info("I do not my daily work : %s : %s : %s", str(startworkvalue),  str(totalAssets), str(startworktime))
        startworkvalue = totalAssets
        


    resCHBTC = chbtc.query_market()
    txtJson = chbtc.query_depth()

    if txtJson == "error" or resCHBTC == "error" :
        continue

    #print ("asks: %s", txtJson["asks"])
    #print ("bids: %s", txtJson["bids"])
    #print ("timestamp: %s", txtJson["timestamp"])
    
    timestamp = txtJson["timestamp"]

    powerAsksPrice = 0.0
    powerBidsPrice = 0.0
    powerBidsNumber = 0.0
    powerAsksNumber = 0.0

    AsksPriceLower = 0.0
    timer_cancel_SellOrder = 0.0
    
    AsksPriceLower = 0.0
    BidsPriceHigh = 0.0
    BidsPriceLower = 0.0

    for i in range(0,len(txtJson["asks"])):

        if i == 0 :
            powerAsksPrice = powerAsksPrice + float(txtJson["asks"][i][0]) * 0.05
            powerBidsPrice = powerBidsPrice + float(txtJson["bids"][i][0]) * 0.35
        elif i == 1 :
            powerAsksPrice = powerAsksPrice + float(txtJson["asks"][i][0]) * 0.10
            powerBidsPrice = powerBidsPrice + float(txtJson["bids"][i][0]) * 0.30
        elif i == 2 :
            powerAsksPrice = powerAsksPrice + float(txtJson["asks"][i][0]) * 0.20
            powerBidsPrice = powerBidsPrice + float(txtJson["bids"][i][0]) * 0.20
        elif i == 3 :
            powerAsksPrice = powerAsksPrice + float(txtJson["asks"][i][0]) * 0.30
            powerBidsPrice = powerBidsPrice + float(txtJson["bids"][i][0]) * 0.10
        elif i == 4 :
            powerAsksPrice = powerAsksPrice + float(txtJson["asks"][i][0]) * 0.35
            powerBidsPrice = powerBidsPrice + float(txtJson["bids"][i][0]) * 0.05

        powerAsksNumber = powerAsksNumber + float(txtJson["asks"][i][1])
        powerBidsNumber = powerBidsNumber + float(txtJson["bids"][i][1])

        AsksPriceLower = float(txtJson["asks"][4][0])
        BidsPriceHigh = float(txtJson["bids"][0][0])
        BidsPriceLower = float(txtJson["bids"][4][0])

    if powerBidsNumber - 4 > powerAsksNumber and curMoney_BTC == 0 and powerBidsPrice - BidsPriceLower < 6 and AsksPriceLower - BidsPriceHigh < 3:
        if (curMoney_CNY / powerBidsPrice) >= 0.001  :
            txtJson = chbtc.buy_order(str(powerBidsPrice), str(((curMoney_CNY / powerBidsPrice))) )
            if txtJson != "error" :
                logger.info("buy_order: %s : %s : %s", str(txtJson["id"]), str(powerBidsPrice), str(((curMoney_CNY / powerBidsPrice))))
                buy_order_id = txtJson["id"]
                #orderPrice = powerBidsPrice
            else :
                logger.debug("buy_order: %s : %f : %f : %s", txtJson, curMoney_CNY, powerBidsPrice, str(("%.4f" % (curMoney_CNY / powerBidsPrice) )) )
                

    if curMoney_BTC != 0 and powerAsksNumber > powerBidsNumber:
        if(powerAsksNumber - 10 > powerBidsNumber):
            txtJson = chbtc.sell_order(str(AsksPriceLower - 0.01), str(("%.3f" % (curMoney_BTC)))) #powerBidsNumber is error value
        elif(powerAsksNumber - 4 > powerBidsNumber):
            txtJson = chbtc.sell_order(str(AsksPriceLower), str(("%.3f" % (curMoney_BTC))))
        #elif(powerAsksNumber - 2 > powerBidsNumber):
        #    txtJson = chbtc.sell_order(str(AsksPriceLower), str(("%.3f" % (curMoney_BTC))))
        else:
        		sell_price = 0.0
        		sell_price = powerAsksPrice - timer_cancel_SellOrder
        		if sell_price - AsksPriceLower > 4:
        			 sell_price = AsksPriceLower
            txtJson = chbtc.sell_order(str(sell_price), str(("%.3f" % (curMoney_BTC))))
        
        if txtJson != "error" :
            logger.info("sell_order: %s : %s : %s", str(txtJson["id"]), str(powerAsksPrice), str(("%.3f" % (curMoney_BTC))))
            sell_order_id = txtJson["id"]
        else :
            logger.debug('sell_order: %s', txtJson)

    if sell_order_id != 0 :
        txtJson = chbtc.query_order(str(sell_order_id))
        if txtJson != "error" :
            sell_order_timer = txtJson["trade_date"]
            sell_order_state = txtJson["status"]
            print ("sell_order_id :%d, %d, %d", sell_order_id, sell_order_timer, sell_order_state)
            if sell_order_state == 0 and (timestamp - sell_order_timer/1000) > int(cancalTime_SellOrder):
                txtJson = chbtc.cancel_order(str(sell_order_id))
                if txtJson != "error" :
                    logger.info("sell_order_Cancel: %s : %s : %s", str(sell_order_id), str(timestamp), str(sell_order_timer/1000))
                    sell_order_id = 0
                    timer_cancel_SellOrder = timer_cancel_SellOrder + 0.01
            if sell_order_state == 2 :
                sell_order_id = 0
                timer_cancel_SellOrder = 0
                logger.info("sell_order_Done: %s : %s : %s", str(txtJson["price"]), str(txtJson["trade_price"]), str(txtJson["trade_amount"]))

    if buy_order_id != 0 :
        txtJson = chbtc.query_order(str(buy_order_id))
        
        if txtJson != "error" :
            buy_order_timer = txtJson["trade_date"]
            buy_order_state = txtJson["status"]
            print ("buy_order_id :%d, %d, %d", buy_order_id, buy_order_timer, buy_order_state)
            if buy_order_state == 0 and (timestamp - buy_order_timer/1000) > int(cancalTime_BuyOrder):
                txtJson = chbtc.cancel_order(str(buy_order_id))
                logger.info("buy_order_Cancel: %s : %s : %s", str(buy_order_id), str(timestamp), str(buy_order_timer/1000))
                if txtJson != "error" :
                    buy_order_id = 0
            if buy_order_state == 2 :
                buy_order_id = 0
                logger.info('buy_order_Done: %s : %s : %s', str(txtJson["price"]), str(txtJson["trade_price"]), str(txtJson["trade_amount"]))

    
    ###time.sleep(0.1)

logger.info ("end app")


