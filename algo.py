def initialize(context): #alleviates need to call functions
    set_benchmark(symbol('XLK'))
    context.stocks=symbol('XLK') #XLK=company ticker. sid=stock ID. tickers can change over time from being bought/sold, copmanies closing down etc. sid used to ensure investment in desired company TECH
    context.stocks2=symbol('XLE')
    #context.stocks2=symbol('XLE') #ENERGY
    context.stocks3=symbol('XLV') #HEALTH
    
    context.bought = False # Store that we've not bought anything yet
    context.bought_price = 0.0 # We've not bought anything yet
    context.sold_price = 999999.9
    
def handle_data(context, data): #function takes data; universe of information. contains everything, eg stock prices
    hist1=data.history(context.stocks, 'price', 75, '1d') #50 periods of 1 day data history prices for Apple
    #hist2=data.history(context.stocks2, 'price', 30, '1d')
    #hist3=data.history(context.stocks3, 'price', 50, '1d')
    '''
    log.info(hist1.head())#uses pandas data
    hist1_sma_75=hist1.mean() #sma is simple moving average, hist takes it from the above defined data set
    log.info(hist1.head())
    hist1_sma_30=hist1[-30:].mean() #mean of the last 20 days of the history

    log.info(hist2.head())
    hist2_sma_75=hist2.mean()
    log.info(hist2.head())
    hist2_sma_30=hist2[-30].mean()
    
    log.info(hist3.head())
    hist3_sma_75=hist3.mean()
    log.info(hist3.head())
    hist3_sma_30=hist3[-30].mean()
    '''
    #Just deal with tech
    
    tech_day = hist1[-1] # Today's price
    tech_3_day = hist1[-3:].mean() # The mean of the last 3 days
    tech_5_day = hist1[-5:].mean() # The mean of the last 5 days
    
    percentage_change = abs((float(tech_day - tech_3_day) / tech_3_day)) # Calculate the change
    # If today's price is better than the 3 day average, and the 3 day average is better than the 5 day average, 
    # and we've not bought yet and the percentage change is greater than 0.5%
    if tech_day > tech_3_day and tech_3_day > tech_5_day and not context.bought and percentage_change > 0.005:
        print "Full buy"
        order_target_percent(context.stocks, 1) # Buy 100% tech
        context.bought = True # Set bought to true to log that we've bought
        context.bought_price = tech_day # Store the price that we bought at
    
    # If today's price is less than the 3 day average, and the 3 day average is worse than the 5 day average,
    # and we've got stuff to sell, and today's price is greater than the price that we bought it for
    # and the percentage change is greater than 0.5%
    elif tech_day < tech_3_day and tech_3_day < tech_5_day and context.bought and tech_day > context.bought_price and percentage_change > 0.005:
        print "Full sell"
        order_target_percent(context.stocks, -1) # Fully short in tech
        context.bought = False # Set bought to False to log that we've sold
        context.sold_price = tech_day # Store the price that we sold at
    '''
    if hist1_sma_30>hist1_sma_75:
        if hist2_sma_30>hist2_sma_75:
            if hist3_sma_30>hist3_sma_75:
                
                order_target_percent(context.stocks, 0.33) #sid and amount. 1.0 is 100%, 0.33 is 30 percent. splitting each equally into 3 baskets t0 maximise returns from each
                order_target_percent(context.stocks2, 0.33)
                order_target_percent(context.stocks3, 0.33)
        else:
            order_target_percent(context.stocks, 0.25)
            order_target_percent(context.stocks2, 0.25)
            order_target_percent(context.stocks3, 0.25)   
                
    elif hist1_sma_75>hist1_sma_30:
        order_target_percent(context.stocks,-0.75) #shorting the company as share price decreases
        order_target_percent(context.stocks2, -1.0)
    '''
