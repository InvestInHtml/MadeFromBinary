# Algorithm goes here please
import pandas
def initialize(context): #alleviates need to call functions
    context.aapl=sid(24) #aapl=company ticker. sid=stock ID. tickers can change over time from being bought/sold, copmanies closing down etc. sid used to ensure investment in desired company
def handle_data(context, data): #function takes data; universe of information. contains everything, eg stock prices
    hist=data.history(context, 'price', 50, '1d') #50 periods of 1 day data history prices for Apple
    log.info(hist.head())#uses pandas data
    sma_50=hist.mean() #sma is simple moving average, hist takes it from the above defined data set
    sma_20=hist[-20:].mean() #mean of the last 20 days of the history

    if sma_20>sma_50: # If the stock is doing better than normal
        order_target_percent(context.aapl, 1.0) #sid and amount. 1.0 is 100%. Try to buy more
    elif sma_50>sma_20: # If the stock is doing worse than normal
        order_target_percent(context.aapl,-1.0) #shorting the company as share price decreases
        
    
    
    
    
