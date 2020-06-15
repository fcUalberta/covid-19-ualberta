"""
Module for Weekly Forecasting using Auto Regression
"""
from random import random
from statsmodels.tsa.statespace.sarimax import SARIMAX
def forecast(data):
    """
    Function to predict the next 7 values for the input data using SARIMAX
    Auto regression function

    Returns: A list of predictions for next 7 days
    """
    predictions = []
    for i in range(7):
        # Initializing the model
        model = SARIMAX(data, order=(1, 1, 1),
            trace=True, error_action="ignore")
        # Fitting the model
        model_fit = model.fit(disp=False)
        # Predicting the values one by one
        yhat = model_fit.predict(len(data), len(data))
        data.append(int(yhat))
        # Appending each prediction to a list
        predictions.append(int(yhat))
    return predictions
