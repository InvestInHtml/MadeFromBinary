# Import Algorithm API functions
from quantopian.algorithm import (
    attach_pipeline,
    pipeline_output,
    order_optimal_portfolio,
)

# Import Optimize API module
import quantopian.optimize as opt

# Pipeline imports
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.psychsignal import stocktwits
from quantopian.pipeline.factors import SimpleMovingAverage
from quantopian.pipeline.data.builtin import USEquityPricing
# Import built-in universe and Risk API method
from quantopian.pipeline.filters import QTradableStocksUS
from quantopian.pipeline.classifiers.morningstar import Sector


def initialize(context):
    # Constraint parameters
    context.max_leverage = 1.0 # Don't spend more than what we have
    context.max_pos_size = 0.015
    context.max_turnover = 0.95
    
    # Attach data pipelines
    attach_pipeline(
        make_pipeline(),
        'data_pipe'
    )
    # Schedule rebalance function
    schedule_function(
        rebalance,
        date_rules.week_start(),
        time_rules.market_open(),
    )


def before_trading_start(context, data):
    # Get pipeline outputs and
    # store them in context
    context.output = pipeline_output('data_pipe')
    
    #print(context.output.sort_values('longs', ascending=False).head(5))
    #print(context.output.sort_values('shorts', ascending=False).head(5))
    
    # Create a list of the stocks that we want to go long in
    context.longs = [] # To store the stocks that we want to go long in
    if 'longs' in context.output.keys():
        for sec in context.output[context.output['longs']].index.tolist(): # For each security
            if data.can_trade(sec): # If we can trade
                context.longs.append(sec) # Add it to the list
            
    # Create a list of the stocks that we want to go short in
    context.shorts = [] # To store the stocks that we want to go short in
    if 'shorts' in context.output.keys():
        for sec in context.output[context.output['shorts']].index.tolist(): # For each security
            if data.can_trade(sec): # If we can trade
                context.shorts.append(sec) # Add it to the list

# Pipeline definition
def make_pipeline():

    my_sectors = [  # A list of the sectors that we want to trade based on their sector id
       206, #"Healthcare"  
       309, #"Energy"
       311, #"Technology"  
    ] 

    sector_filter = Sector().element_of(my_sectors) # Create a sector filter
    
    base_universe = QTradableStocksUS() & sector_filter # The stock universe that we want to use
    
    just_health = base_universe & Sector().element_of([206])
    just_energy = base_universe & Sector().element_of([309])
    just_technology = base_universe & Sector().element_of([311])
    
    just_health_sma_75 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=75, mask=just_health) # 75 day moving average
    just_energy_sma_75 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=75, mask=just_health) # 75 day moving average
    just_technology_sma_75 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=75, mask=just_health) # 75 day moving average
    
    just_health_sma_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=just_health) # 75 day moving average
    just_energy_sma_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=just_health) # 75 day moving average
    just_technology_sma_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=just_health) # 75 day moving average
    
    
    sentiment_score_technology = SimpleMovingAverage(
        inputs=[stocktwits.bull_minus_bear], # How the tweets are
        window_length=20,
        mask=just_technology # Us stocks
    )
    
    sentiment_score_health = SimpleMovingAverage(
        inputs=[stocktwits.bull_minus_bear], # How the tweets are
        window_length=20,
        mask=just_health # Us stocks
    )
    
    sentiment_score_energy = SimpleMovingAverage(
        inputs=[stocktwits.bull_minus_bear], # How the tweets are
        window_length=20,
        mask=just_energy # Us stocks
    )
    

    
   
    #sma_20 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=base_universe) # 20 day moving average
    
    #sma_50 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=50, mask=base_universe) # 50 day moving average
     
    #above_average = sma_20 > sma_50 # The stocks that are doing better than normal
    #below_average = sma_20 < sma_50 # The stocks that are doing worse than normal
    
    #middle_75_bull = ~(sentiment_score.top(100) & sentiment_score.top(25))
    #middle_75_bear = ~(sentiment_score.bottom(100) & sentiment_score.bottom(25))
    
    longs = shorts = None
    
    if just_technology_sma_30 > just_technology_sma_75:
        if just_energy_sma_30 > just_energy_sma_75:
            if just_health_sma_30 > just_health_sma_75:
                just_technology_long = sentiment_score_technology.top(40)
                just_energy_long = sentiment_score_energy.top(40)
                just_health_long = sentiment_score_health.top(20)
        else:
            just_technology_long = sentiment_score_technology.top(30)
            just_energy_long = sentiment_score_energy.top(20)
            just_health_long = sentiment_score_health.top(50)
           
        longs = just_technology_long | just_energy_long | just_health_long 
    else:
        just_technology_short = sentiment_score_technology.bottom(50)
        just_energy_short = sentiment_score_energy.bottom(30)
        just_health_short = sentiment_score_health.bottom(20)
        
        shorts = just_technology_short | just_energy_short | just_health_short
    
    
    #longs = above_average & (sentiment_score_20 > sentiment_score_50) # Go long on the above average stocks that everyone else also thinks are going to increase
    

    
    #shorts = below_average & (sentiment_score_50 > sentiment_score_20) # Go short on the below average stocks that everyone else also thinks are going to decrease
    
    pipeline = Pipeline()
    try:
        pipeline.add(longs, 'longs')
    except:
        pass
    
    try:
        pipeline.add(shorts, 'shorts')
    except:
        pass
    #securities_to_trade = (longs | shorts) # All of the stocks that are either in long or short and are in energy, technology or health
    
    return pipeline
    #return Pipeline( # Declare a new pipeline
    #   columns={ # The columns of data
    #       'longs': longs, # One for longs
    #       'shorts': shorts # One for shorts
    #   },
    #   screen=(securities_to_trade), # Filter to show only the ones that that in either of the columns i.e. no irrelevant data.
    #)

def compute_target_weights(context, data):
    # Weights are a number that we use to rank each stock. Stocks with high weights are ones
    # that we want to action on and low weights are ones to ignore

    # Initialize empty target weights dictionary.
    # This will map securities to their target weight.
    weights = {}
    
    if context.longs and context.shorts: # If there are securities in our longs and shorts lists
        # 0.5 in each means that we want half of our portfolio to be longs and the other half
        # to be shorts
        context.longs = context.longs[0:74]
        context.shorts = context.shorts[0:74]
        long_weight = 0.5 / len(context.longs) # Divde 0.5 by the number of longs so each long is equally weighted (it's the same percentage of the porfolio)
        short_weight = -0.5 / len(context.shorts) # Same for the shorts
    else:
        return weights # Return the empty weights if there were no shorts or longs
    
    # Look through the securities in our portfolio and if they are not to be shorted or longed give them a weight of 0 so that no action is taken on them.
    for security in context.portfolio.positions:
        if security not in context.longs and security not in context.shorts and data.can_trade(security): # If it's no in longs or shorts and it's tradable
            weights[security] = 0 # Give it a weight of zero so that we do nothing with it

    for security in context.longs: # For each long
        weights[security] = long_weight # Give it the weight calculated above.

    for security in context.shorts: # For each short
        weights[security] = short_weight # Give it the weight calculated above
    
    return weights # Return the weights


def rebalance(context, data):
    # Calculate target weights to rebalance
    target_weights = compute_target_weights(context, data)
    #print (target_weights)
    # Ensure long and short books
    # are roughly the same size
    dollar_neutral = opt.DollarNeutral()

    # Constrain target portfolio's leverage i.e. don't spend more than we have
    max_leverage = opt.MaxGrossExposure(context.max_leverage)

    # If we have target weights, rebalance our portfolio
    if target_weights:
        order_optimal_portfolio(
            objective=opt.TargetWeights(target_weights),
            constraints=[dollar_neutral, max_leverage],
        )
