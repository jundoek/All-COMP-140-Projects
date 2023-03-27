"""
Stock market prediction using Markov chains.
"""

import comp140_module3 as stocks
from collections import defaultdict
import random

### Model

test_data_1 = [1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1]

def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer repesenting the desired order of the markov chain

    returns: a dictionary that represents the Markov chain
    """
    mk_chain = {}
    for data_pos in range(0, len(data) - order):
        bin_order = tuple(data[data_pos:data_pos + order])
        next_val = data[data_pos + order]
        if bin_order not in mk_chain:
            mk_chain[bin_order] = defaultdict(float)
        mk_chain[bin_order][next_val] += 1
    for bin_tuple in mk_chain:
        sum_predicted_states = 0.0
        #print(mk_chain[bin_tuple].key())
        for predicted_val in mk_chain[bin_tuple]:
            sum_predicted_states += mk_chain[bin_tuple][predicted_val]
        for predicted_val in mk_chain[bin_tuple]:
            mk_chain[bin_tuple][predicted_val] /= sum_predicted_states
    
    return mk_chain

m_model = {(0, 0): {1: 1}, (0, 1): {1: 1}, (1, 0): {2: 1}, (1, 1): {3: 1}}


def make_weighted_choice(model, bins):
    """
    Makes a random choice based on the weights of the bin values
    inputs:
        - model: a dictionary representing a Markov chain
        - bins: a tuple representing the sequence of preceding values
    returns: an integer representing a possible next value
    """
    list_of_prob = []
    prob_vals = 0.0
    for next_bins in model[bins]:
        bins_and_vals = []
        prob_vals += model[bins][next_bins]
        bins_and_vals.append(next_bins)
        bins_and_vals.append(prob_vals)
        list_of_prob.append(bins_and_vals)
    print(list_of_prob)
    choice = random.random()
    for elements in range(len(list_of_prob)):
        if elements == 0:
            if choice < list_of_prob[elements][1]:
                next_val =  list_of_prob[elements][0]
        else:
            if list_of_prob[elements - 1][1] <= choice < list_of_prob[elements][1]:
                next_val = list_of_prob[elements][0]
                
    return next_val             


### Predict




def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    list_of_predicted_bins = []
    previous_bins = list(last)
    while len(list_of_predicted_bins) < num:
        current_bins = tuple(previous_bins)
        if current_bins not in model:
            predicted_next = random.randrange(0, 4)
        else:
            predicted_next = make_weighted_choice(model, current_bins)
        list_of_predicted_bins.append(predicted_next)
        previous_bins.pop(0)
        previous_bins.append(predicted_next)
    return list_of_predicted_bins


#print(predict(m_model, [0, 0], 3))

### Error

def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    difference_squared = 0.0
    for num in range(len(result)):
        difference_squared += (result[num] - expected[num]) **2
    mean = difference_squared / len(result)
    return mean


### Experiment

def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    original_model = markov_chain(train, order)
    cumulative_mse = 0.0
    trial_counter = 0
#	The following part is used to calculate the averae mean squared error 
#	under the number of trials when given the prediction of the future of
#	the test data given the training data
    while trial_counter < trials:
        predicted_bins = predict(original_model, test, future)
        cumulative_mse += mse(predicted_bins, actual)
        trial_counter += 1
    average_mse = cumulative_mse/trials
    return average_mse


### Application

def run():
    """
    Run application.

    You do not need to modify any code in this function.  You should
    feel free to look it over and understand it, though.
    """
    # Get the supported stock symbols
    symbols = stocks.get_supported_symbols()

    # Get stock data and process it

    # Training data
    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    # Test data
    testchanges = {}
    testbins = {}
    for symbol in symbols:
        testprices = stocks.get_test_prices(symbol)
        testchanges[symbol] = stocks.compute_daily_change(testprices)
        testbins[symbol] = stocks.bin_daily_changes(testchanges[symbol])

    # Display data
    #   Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    # Run experiments
    orders = [1, 3, 5, 7, 9]
    ntrials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", testbins[symbol][-days:])
        for order in orders:
            error = run_experiment(bins[symbol], order,
                                   testbins[symbol][-order-days:-days], days,
                                   testbins[symbol][-days:], ntrials)
            print("Order", order, ":", error)
        print()

# You might want to comment out the call to run while you are
# developing your code.  Uncomment it when you are ready to run your
# code on the provided data.

# run()
