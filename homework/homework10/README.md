## part A

MARK DOWN: Assumption is that the relation is linear. As the data imported is the stock market. I think we can generalise it to a slightly positive line, of course in longer sequences one could argue that the relation is exponential, which would be correct, but due to the limited access to data in yfinance, I was able to achieve a way better score with a simple linear model R^2 = ~0.96, yet I found MSE to be a little too high for comfort (44, which makes the mean error ~6.5, which is a lot for the SPY)

I find this result satisfactory. Thought the parameters include the opening price, making this model limited in usage, practically, it would be impossible to predict more than one day into the future accurately, since the opening price depends on the previous closing price, and so on, therefore, while it may have a high accuracy for usage after 930 stock market open, it can only really be used then for the desired prediction.

## part B

the features I made were 30 day SMA an 30 day volatility. These are calculated based on the last 30 trading days' closing prices. Another thing I did was I shifted up the closing price. so each entry also knows what is the closing of the next day. This is used to train and testing the model. The final results are plotted, and RMSE achieved was ~25.
