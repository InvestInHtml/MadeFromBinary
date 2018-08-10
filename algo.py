def initialize(context): #alleviates need to call functions
    set_benchmark(symbol('XLK')) # Set the benchmark shown on the graph
    
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
    hist1=data.history(context.stocks, 'price', 365, '1d') # Technology
    hist2=data.history(context.stocks2, 'price', 365, '1d') # Energy
    hist3=data.history(context.stocks3, 'price', 365, '1d') # Health

    #Just deal with tech
    tech_day = hist1[-1] # Today's price
    tech_2_day = hist1[-2:].mean() # The mean of the last 3 days
    tech_4_day = hist1[-4:].mean() # The mean of the last 5 days
    tech_8_day = hist1[-8:].mean() # The mean of the last 8 days
    
    percentage_change = (float(tech_day - tech_2_day) / tech_2_day) # Calculate the absolutepercentage change between the most recent price and the moving average
    
    today_last_year_tech = hist1[0:2].mean() # Get the price today last year
    three_day_future_last_year_tech = hist1[1:4].mean() # Get the mean of the 3 days after today last year
    
    went_up_tech = three_day_future_last_year_tech > today_last_year_tech # Did the price go up?
    
    #short_score = ((int(tech_day > tech_2_day)*2)-1)*1.2
    #long_score = ((int(tech_2_day > tech_4_day)*2)-1)*1.2
    long_score = int(tech_day > tech_2_day and tech_2_day > tech_4_day)
    short_score = - int(tech_day < tech_2_day and tech_2_day < tech_4_day)
    went_up = ((int(went_up_tech)*2)-1)*0.5
    percent_from_8_days = float(tech_day - tech_8_day)/tech_8_day
    percent = 0
    if percentage_change > 0.005:# and percent_from_8_days > 0.008:
        percent = 1
    elif percentage_change < -0.005:# and percent_from_8_days < -0.008:
        percent = -1
    total_score = short_score + long_score + went_up + percent
    
    # If today's price is better than the 2 day average, 
    # the 2 day average is better than the 4 day average, 
    # we've not bought yet, and the percentage change is greater than 0.5%
    if total_score > 1.8 and (not context.bought_tech):
        print total_score
        print "Tech: Full buy" # Log what the algorithm is doing
        order_target_percent(context.stocks, total_score**2/(4)) # Buy 100% tech
        context.bought_tech = True # Set bought to true to log that we've bought
        context.bought_price_tech = tech_day # Store the price that we bought at
    
    # If today's price is worse than the 2 day average, 
    # the 2 day average is worse than the 4 day average, 
    # we've not bought yet, the price is greater than what we bought it for,
    # and the percentage change is greater than 0.5%
    elif total_score < -1.8 and (context.bought_tech) and tech_day > context.bought_price_tech:
        print total_score
        print "Tech: Full sell" # Log what the algorithm is doing
        order_target_percent(context.stocks, -total_score**2/(4)) # Fully short in tech
        context.bought_tech = False # Set bought to False to log that we've sold
        context.sold_price_tech = tech_day # Store the price that we sold at
    
    #Just deal with energy
    energy_day = hist2[-1] # Today's price
    energy_2_day = hist2[-3:].mean() # The mean of the last 3 days
    energy_4_day = hist2[-5:].mean() # The mean of the last 5 days
    energy_8_day = hist2[-8:].mean() # The mean of the last 8 days
    
    percentage_change = (float(energy_day - energy_2_day) / energy_2_day) # Calculate the absolutepercentage change between the most recent price and the moving average
    
    today_last_year_energy = hist1[0:2].mean() # Get the price today last year
    three_day_future_last_year_energy = hist1[1:4].mean() # Get the mean of the 3 days after today last year
    
    went_up_energy = three_day_future_last_year_energy > today_last_year_energy # Did the price go up?
    
    #short_score = ((int(energy_day > energy_2_day)*2)-1)*1.2
    #long_score = ((int(energy_2_day > energy_4_day)*2)-1)*1.2
    long_score = int(energy_day > energy_2_day and energy_2_day > energy_4_day)
    short_score = - int(energy_day < energy_2_day and energy_2_day < energy_4_day)
    went_up = ((int(went_up_energy)*2)-1)*0.5
    percent_from_8_days = float(energy_day - energy_8_day)/energy_8_day
    percent = 0
    if percentage_change > 0.005:# and percent_from_8_days > 0.008:
        percent = 1
    elif percentage_change < -0.005:# and percent_from_8_days < -0.008:
        percent = -1
    total_score = short_score + long_score + went_up + percent
    
    # If today's price is better than the 2 day average, 
    # the 2 day average is better than the 4 day average, 
    # we've not bought yet, and the percentage change is greater than 0.5%
    if total_score > 1.8 and (not context.bought_energy):
        print total_score
        print "energy: Full buy" # Log what the algorithm is doing
        order_target_percent(context.stocks, total_score**2/(4)) # Buy 100% energy
        context.bought_energy = True # Set bought to true to log that we've bought
        context.bought_price_energy = energy_day # Store the price that we bought at
    
    # If today's price is worse than the 2 day average, 
    # the 2 day average is worse than the 4 day average, 
    # we've not bought yet, the price is greater than what we bought it for,
    # and the percentage change is greater than 0.5%
    elif total_score < -1.8 and (context.bought_energy) and energy_day > context.bought_price_energy:
        print total_score
        print "energy: Full sell" # Log what the algorithm is doing
        order_target_percent(context.stocks, -total_score**2/(4)) # Fully short in energy
        context.bought_energy = False # Set bought to False to log that we've sold
        context.sold_price_energy = energy_day # Store the price that we sold at
        
     #Just deal with health
    health_day = hist3[-1] # Today's price
    health_2_day = hist3[-2:].mean() # The mean of the last 3 days
    health_4_day = hist3[-4:].mean() # The mean of the last 5 days
    health_8_day = hist3[-8:].mean() # The mean of the last 8 days
    
    percentage_change = (float(health_day - health_2_day) / health_2_day) # Calculate the absolutepercentage change between the most recent price and the moving average
    
    today_last_year_health = hist1[0:2].mean() # Get the price today last year
    three_day_future_last_year_health = hist1[1:4].mean() # Get the mean of the 3 days after today last year
    
    went_up_health = three_day_future_last_year_health > today_last_year_health # Did the price go up?
    
    #short_score = ((int(health_day > health_2_day)*2)-1)*1.2
    #long_score = ((int(health_2_day > health_4_day)*2)-1)*1.2
    long_score = int(health_day > health_2_day and health_2_day > health_4_day)
    short_score = - int(health_day < health_2_day and health_2_day < health_4_day)
    went_up = ((int(went_up_health)*2)-1)*0.5
    percent_from_8_days = float(health_day - health_8_day)/health_8_day
    percent = 0
    if percentage_change > 0.005:# and percent_from_8_days > 0.008:
        percent = 1
    elif percentage_change < -0.005:# and percent_from_8_days < -0.008:
        percent = -1
    total_score = short_score + long_score + went_up + percent
    
    # If today's price is better than the 2 day average, 
    # the 2 day average is better than the 4 day average, 
    # we've not bought yet, and the percentage change is greater than 0.5%
    if total_score > 1.8 and (not context.bought_health):
        print total_score
        print "health: Full buy" # Log what the algorithm is doing
        order_target_percent(context.stocks, total_score**2/(4)) # Buy 100% health
        context.bought_health = True # Set bought to true to log that we've bought
        context.bought_price_health = health_day # Store the price that we bought at
    
    # If today's price is worse than the 2 day average, 
    # the 2 day average is worse than the 4 day average, 
    # we've not bought yet, the price is greater than what we bought it for,
    # and the percentage change is greater than 0.5%
    elif total_score < -1.8 and (context.bought_health) and health_day > context.bought_price_health:
        print total_score
        print "health: Full sell" # Log what the algorithm is doing
        order_target_percent(context.stocks, -total_score**2/(4)) # Fully short in health
        context.bought_health = False # Set bought to False to log that we've sold
        context.sold_price_health = health_day # Store the price that we sold at
