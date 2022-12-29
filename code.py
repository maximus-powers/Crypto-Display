import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal
import json
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise


# CALL DATA FROM API  &  SETUP DISPLAY ----------------------------------------------------------------------
# CREATE VARIABLES
CURRENCY = "USD"
SYMBOLS = ['BTC', 'ETH', 'NEAR', 'AMPL', 'GRT']
DATA_SOURCE = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + ','.join(SYMBOLS) + '&convert=USD'
CMC_SECRET = secrets["coin-market-cap"]
HEADERS = {
  'X-CMC_PRO_API_KEY': CMC_SECRET,
}

# CALLING THE URL, AND PUT THE DATA ON THE DISPLAY (THIS IS LIKE A SESSION BETWEEN THE DISPLAY AND URL)
matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    headers=HEADERS,
    status_neopixel=board.NEOPIXEL,
    #default_bg=cwd + "/bitcoin_background.bmp",
    debug=False,
    rotation=180,
    )

# INITIALIZE TEXT FORMATTING
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(3, 15),
    text_color=0x3d1f5c,
    line_spacing=0.85,
    # scrolling=True
    )
matrixportal.preload_font(b"$012345789")  # preload numbers
matrixportal.preload_font((0x00A3, 0x20AC))  # preload gbp/euro symbol
# ----------------------------------------------------------------------------------------------------------


# CREATE A CLASS FOR THE DISPLAY
class Display:
    SYM_DICT = {}
    counter = 0

    def refresh(self):
        self.counter = 0
        r = matrixportal.fetch()
        data = json.loads(r)
        for X in SYMBOLS:
            SYMBOL = data['data'][X]['symbol']
            PRICE = round(data['data'][X]['quote']['USD']['price'], 2)
            DAY_CHANGE = str(round(data['data'][X]['quote']['USD']['percent_change_24h'], 1)) + '%'
            self.SYM_DICT[self.counter] = {'symbol':SYMBOL,'price':PRICE,'day_change':DAY_CHANGE}
            self.counter += 1
        self.counter = 0
        print('Data refreshed')

    def next(self):
        self.counter += 1
        if self.counter >= (len(SYMBOLS) - 1):
            self.counter = 0

    def prev(self):
        self.counter =- 1
        if self.counter < 0:
            self.counter = len(SYMBOLS) - 1

    def post(self):
        matrixportal.set_text(self.SYM_DICT[self.counter]['symbol'] + ' ' + self.SYM_DICT[self.counter]['day_change'] + '\n' + '$' + str(self.SYM_DICT[self.counter]['price']))
        

display = Display()        


# Loop to run display
while True:
    display.refresh()
    temp_time = time.monotonic()
    while temp_time + (5*60) > time.monotonic():
        display.post()
        display.next()
        time.sleep(5)
