# Crypto-Display

/images/crypto-display.jpg

### The ticker displays one cryptocurrency at a time, showing: symbol, price, and 24hr % change.

This document breaks down processes used to call live market data, parse it, and post it to the board (in technical terms). For a simplified logic breakdown please check out my Medium article.

------------------------------------------------

## How it works:
### Components:
- LED Matrix Dispay (64 by 32 pixels, 3mm pitch)
- Arduino ESP8266 Controller



#### Picking Symbols:
This project uses the CoinMarketCap API to fetch live market data. Before it's called, we need to initialize *SYMBOLS[]* with the cryptos we want data on. For example:
```python
SYMBOLS = ['BTC', 'ETH', 'NEAR', 'AMPL']
```


#### *MatrixPortal* class object (*matrixportal* module):
Using the *matrixportal* module from Adafruit's library, we create an class object called *MatrixPortal*. We can use this object to both call data and set the text on the display. We'll initialize our object with: 
* *DATA_SOURCE* -- URL which has been concatenated with our list of symbols
* *HEADERS* -- the API key tied to our CMC account
* Formatting for our text

Important methods:
> .fetch() -- will fetch JSON data from the object's data source, which is then stored in the variable r

> .set_text(string) -- will show the passed string on the display



#### *Display* Class:
We create a class called *Display* to store our parsed data, and create methods for changing the display.
* *COUNTER* -- pointer used for iterating through our data one symbol at a time
* *SYM_DICT* -- dictionary of dictionaries (key: *COUNTER*, value: latest data on a **single** crypto)

Important methods:
> .refresh() -- Refreshes *SYM_DICT* with new data: Uses matrixportal.fetch() to get new JSON data, parses it into *SYMBOL*, *PRICE*, and *DAY_CHANGE* and stores it in *SYM_DICT* under the *COUNTER*, increments *COUNTER*, then does it again with the next crypto until it reaches the end of our list.

> .next() and .prev() -- increments up and down respectively through the list of symbols

> .post() -- Puts data on the display: Creates a string from the data indexed at the current value of *COUNTER*, uses matrixportal.set_text(string) to display it.



#### Loop:
When the device boots, it begins a loop to cycle through all of the symbols to display. 
They are set to cycle every 5 seconds, and the data refreshes every 5 minutes.
