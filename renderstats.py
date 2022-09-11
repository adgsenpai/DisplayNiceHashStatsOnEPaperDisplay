# CODE TO RENDER DISPLAY STATS TO `data.bmp`

from io import BytesIO
from nicehash import nicehash as nh
import yfinance
import ast

host =              'https://api2.nicehash.com'
organisation_id =   'supersecret'
key =               'supersecret'
secret =            'supersecret'
walletaddress =     'mywalletaddress'

def returnWalletData():
    api = nh.private_api(host, organisation_id, key, secret)
    data = api.get_accounts()
    wallet = data['total']
    return wallet


def get_rigs():
    devicedata = []
    api = nh.private_api(host, organisation_id, key, secret)
    data = api.get_rigs()
    for rigitem in data['miningRigs']:
        rigname = rigitem['name']
        minerstatus = rigitem['minerStatus']
        devices = rigitem['devices']
        powerusage = 0
        totalspeed = 0.0000000
        for device in devices:
            dictdata = {}
            dictdata['name'] = (device['name'])
            powerusage += device['powerUsage']
            dictdata['powerusage'] = device['powerUsage']
            strspeed = str(device['speeds']).replace('[', '').replace(']', '')
            try:
                dictdata['algorithm'] = ast.literal_eval(strspeed)['algorithm']
                dictdata['speed'] = int(
                    float(ast.literal_eval(strspeed)['speed']))
                totalspeed += (int(float(dictdata['speed'])))
                dictdata['displaySuffix'] = ast.literal_eval(strspeed)[
                    'displaySuffix']
            except Exception as e:
                print(e)
                pass
            if device['deviceType']['enumName'] == 'CPU':
                pass
            else:
                dictdata['devicetype'] = device['deviceType']['enumName']
                devicedata.append(dictdata)
    devicedata.append({'powerusage': powerusage, 'totalspeed': totalspeed})
    return devicedata


def BTCtoZAR(btc):
    try:
        btc = float(btc)
        # get the current BTC price
        btcprice = yfinance.Ticker("BTC-USD").info['regularMarketPrice']
        zarprice = yfinance.Ticker("ZAR=X").info['regularMarketPrice']
        zar = float(btcprice) * float(zarprice) * btc
    except:
        return BTCtoZAR(btc)
    return zar


def getWalletAddress():
    api = nh.private_api(host, organisation_id, key, secret)
    data = api.get_accounts()
    wallet = data['total']
    return wallet


def RenderStats():
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('L', (250, 122), 255)  # 255: clear the frame 
    draw = ImageDraw.Draw(image)

    # get font where script is located
    import os
    scriptdir = os.path.dirname(os.path.realpath(__file__))
    font = ImageFont.truetype(scriptdir + '/Product Sans Regular.ttf', 12)
    fontBold = ImageFont.truetype(scriptdir+'/ProductSansBold.ttf', 15)
    # draw rigs
    rigs = get_rigs()
    y = 0
        # current btc price
    cP = BTCtoZAR(1)
    draw.text((0, y), 'Total Pool Speed:', font=font, fill=0)
    draw.text(
        (0, y+15), str(rigs[-1]['totalspeed'])+'H/s', font=fontBold, fill=0)
    draw.text((0, y+30), 'Power Usage:', font=font, fill=0)
    draw.text(
        (0, y+45), str(rigs[-1]['powerusage'])+'W', font=fontBold, fill=0)
    draw.text((0, y+80), 'Wallet Balance:', font=font, fill=0)
    draw.text((0, y+100), 'R'+str(round(float(returnWalletData()
              ['totalBalance'])*cP, 2)), font=fontBold, fill=0)
    # render walletQRCode
    from pyqrcode import QRCode
    url = QRCode(walletaddress)
    url.png('walletQRCode.png', scale=2)
    # render walletQRCode
    from PIL import Image
    import png
    # my walletQRCODE
    img = Image.open('walletQRCode.png')
    image.paste(img, (150, y))
    # print date time
    import datetime
    now = datetime.datetime.now()
    # print wallet address
    draw.text((125, y+100), now.strftime("%Y-%m-%d %H:%M"),
              font=ImageFont.truetype('Product Sans Regular.ttf', 15), fill=0)
    # print 1BTC = ZAR
    draw.text((0, y+60), '1 BTC = R' + str(round(cP, 2)),
              font=ImageFont.truetype('Product Sans Regular.ttf', 15), fill=0)
    image.save('data.bmp')

if __name__ == '__main__':
    RenderStats()
