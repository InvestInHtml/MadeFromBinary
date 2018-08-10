def initialize(context): #alleviates need to call functions
    set_benchmark(symbol('XLV')) # Set the benchmark shown on the graph
    
    context.stocks=symbol('XLK') # Tech
    context.stocks2=symbol('XLE') # Energy
    context.stocks3=symbol('XLV') # Health
    
    # Tracks tech
    context.bought_tech = False # Store that we've not bought anything yet
    context.bought_price_tech = 0.0 # Stores the price we buy at
    context.sold_price_tech = 999999.9 # Unused - Stores the price we sold at
    
    # Tracks energy
    context.bought_energy = False # Store that we've not bought anything yet
    context.bought_price_energy = 0.0 # Stores the price we buy at
    context.sold_price_energy = 999999.9 # Unused - Stores the price we sold at
    
    # Tracks health
    context.bought_health = False # Store that we've not bought anything yet
    context.bought_price_health = 0.0 # Stores the price we buy at
    context.sold_price_health = 999999.9 # Unused - Stores the price we sold at
    
    context.minute_counter = 0 # To track how many minutes have run
    
def handle_data(context, data): # Function takes data; universe of information. contains everything, eg stock prices. Is called every simulated minute
    
    # This function runs every minute
    # but for speed we only want it to run every 5 minutes
    context.minute_counter += 1 # Increment the minute counter
    
    if (context.minute_counter < 5): # If its not been 5 minutes yet
        return # Wait another minute stop executing the function
    else: # Its been 5 minutes
        context.minute_counter = 0 # Reset the counter 
    
    # Get 30 days of data for each basket
    hist1=data.history(context.stocks, 'price', 30, '1d') # Technology
    hist2=data.history(context.stocks2, 'price', 30, '1d') # Energy
    hist3=data.history(context.stocks3, 'price', 30, '1d') # Health

    #Just deal with tech
    tech_day = hist1[-1] # Today's price
    tech_2_day = hist1[-2:].mean() # The mean of the last 3 days
    tech_4_day = hist1[-4:].mean() # The mean of the last 5 days
    
    percentage_change = abs((float(tech_day - tech_2_day) / tech_2_day)) # Calculate the absolutepercentage change between the most recent price and the moving average
    
    # If today's price is better than the 2 day average, 
    # the 2 day average is better than the 4 day average, 
    # we've not bought yet, and the percentage change is greater than 0.5%
    if tech_day > tech_2_day and tech_2_day > tech_4_day and not context.bought_tech and percentage_change > 0.005:
        print "Tech: Full buy" # Log what the algorithm is doing
        order_target_percent(context.stocks, 1) # Buy 100% tech
        context.bought_tech = True # Set bought to true to log that we've bought
        context.bought_price_tech = tech_day # Store the price that we bought at
    
    # If today's price is worse than the 2 day average, 
    # the 2 day average is worse than the 4 day average, 
    # we've not bought yet, the price is greater than what we bought it for,
    # and the percentage change is greater than 0.5%
    elif tech_day < tech_2_day and tech_2_day < tech_4_day and context.bought_tech and tech_day > context.bought_price_tech and percentage_change > 0.005:
        print "Tech: Full sell" # Log what the algorithm is doing
        order_target_percent(context.stocks, -1) # Fully short in tech
        context.bought_tech = False # Set bought to False to log that we've sold
        context.sold_price_tech = tech_day # Store the price that we sold at
    
    
    #Just deal with energy
    energy_3_day = hist2[-3:].mean() # The mean of the last 3 days
    energy_5_day = hist2[-5:].mean() # The mean of the last 5 days
    energy_8_day = hist2[-8:].mean() # The mean of the last 8 days
    
    percentage_change = abs((float(energy_3_day - energy_5_day) / energy_8_day)) # Calculate the change
    # If the 3 day average is better than the 5 day average, 
    # the 5 day average is better than the 8 day average, 
    # we've not bought yet, and the percentage change is greater than 0.5%
    if energy_3_day > energy_5_day and energy_3_day > energy_5_day and not context.bought_energy and percentage_change > 0.005:
        print "Energy: Full buy" # Log what the algorithm is doing
        order_target_percent(context.stocks2, 1) # Buy 100% energy
        context.bought_energy = True # Set bought to true to log that we've bought
        context.bought_price_energy = energy_3_day # Store the price that we bought at
    
    # If the 3 day average is worse than the 5 day average, 
    # the 5 day average is worse than the 8 day average, 
    # we've not bought yet, the price is greater than what we bought it for,
    # and the percentage change is greater than 0.5%
    elif energy_3_day < energy_5_day and energy_3_day < energy_5_day and context.bought_energy and energy_3_day > context.bought_price_energy and percentage_change > 0.005:
        print "Energy: Full sell" # Log what the algorithm is doing
        order_target_percent(context.stocks2, -1) # Fully short in energy
        context.bought_energy = False # Set bought to False to log that we've sold
        context.sold_price_energy = energy_3_day # Store the price that we sold at
    
    #Just deal with health
    health_day = hist3[-1] # Today's price
    health_2_day = hist3[-2:].mean() # The mean of the last 3 days
    health_4_day = hist3[-4:].mean() # The mean of the last 5 days
    
    percentage_change = abs((float(health_day - health_2_day) / health_2_day)) # Calculate the change
    # If today's price is better than the 2 day average, 
    # the 2 day average is better than the 4 day average, 
    # we've not bought yet, and the percentage change is greater than 0.5%
    if health_day > health_2_day and health_2_day > health_4_day and not context.bought_health and percentage_change > 0.005:
        print "Health: Full buy" # Log what the algorithm is doing
        order_target_percent(context.stocks3, 1) # Buy 100% health
        context.bought_health = True # Set bought to true to log that we've bought
        context.bought_price_health = health_day # Store the price that we bought at
    
    # If today's price is worse than the 2 day average, 
    # the 2 day average is worse than the 4 day average, 
    # we've not bought yet, the price is greater than what we bought it for,
    # and the percentage change is greater than 0.5%
    elif health_day < health_2_day and health_2_day < health_4_day and context.bought_health and health_day > context.bought_price_health and percentage_change > 0.005:
        print "Health: Full sell" # Log what the algorithm is doing
        order_target_percent(context.stocks3, -1) # Fully short in health
        context.bought_health = False # Set bought to False to log that we've sold
        context.sold_price_health = health_day # Store the price that we sold at
  
