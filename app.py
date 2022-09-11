# MAIN CODE FILE

import signal
import sys
import time
import epaper
from PIL import Image,ImageDraw,ImageFont
import renderstats

epd = epaper.epaper('epd2in13_V2').EPD()
epd.init(epd.FULL_UPDATE)
epd.Clear(0xFF)

# if control c is pressed, exit
def signal_handler(sig, frame):    
    epd.sleep()
    sys.exit(0)

def RenderScreen():
    renderstats.RenderStats()
    # render the image on the display
    image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    bmp = Image.open('data.bmp')
    image1.paste(bmp, (0, 0))
    epd.init(epd.FULL_UPDATE)
    epd.display(epd.getbuffer(image1))    
    # add signal handler
    signal.signal(signal.SIGINT, signal_handler)    

while True:
    try:
        RenderScreen()
    except:
        RenderScreen()    