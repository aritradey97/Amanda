# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 04:45:09 2018

@author: 1605180
"""



class Regression:
    def execute():
        import quandl, math, datetime, sklearn, pickle
        import numpy as np
        from sklearn import preprocessing, cross_validation
        from sklearn.linear_model import LinearRegression
        import matplotlib.pyplot as plt
        from matplotlib import style
        
#        from IPython import get_ipython
#        get_ipython().run_line_magic('matplotlib', 'qt')
        
        style.use('ggplot')
        quandl.ApiConfig.api_key = 'coDzCo-DH8yvdswyd1uZ'
        
        df = quandl.get('WIKI/GOOGL', api_key = 'coDzCo-DH8yvdswyd1uZ')
        
        df['HL_PCT'] = ((df['Adj. High'] - df['Adj. Close'])/df['Adj. Close']) * 100
        df['PCT_CHANGE'] = ((df['Adj. Close'] - df['Adj. Open'])/df['Adj. Open']) * 100
        df = df[['Adj. Close', 'HL_PCT', 'PCT_CHANGE', 'Adj. Volume']]
        
        forcast_col = 'Adj. Close'
        df.fillna(-99999, inplace = True)
        forecast_out = int(math.ceil(0.01*len(df)))
        
        df['lebel'] = df[forcast_col].shift(-forecast_out)
        df.dropna(inplace = True)
        print(df.tail())
        
        X = np.array(df.drop(['lebel'], 1))
        Y = np.array(df['lebel'])
        
        X = preprocessing.scale(X)
        #X = X[:-forecast_out]
        X_lately = X[-forecast_out:]
        df.dropna(inplace = True)
        Y = np.array(df['lebel'])
        
        X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size = 0.2)
        ##plt.scatter(X, Y)
        ##plt.show()
        #clf = sklearn.linear_model.BayesianRidge()
        #clf.fit(X_train, Y_train)
        #
        #with open('linearregression.pickle', 'wb') as f:
        #    pickle.dump(clf, f)
        
        pickle_in = open('linearregression.pickle', 'rb')
        clf = pickle.load(pickle_in)
            
        accuracy = clf.score(X_test, Y_test)
        forecast_set = clf.predict(X_lately)
        print(forecast_set, accuracy, forecast_out)
        df['Forecast'] = np.nan
        
        last_date = df.iloc[-1].name
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + one_day
        
        
        for i in forecast_set:
            next_day = datetime.datetime.fromtimestamp(next_unix)
            next_unix += one_day 
            df.loc[next_day] = [np.nan for _ in range(len(df.columns) - 1)] +[i]
        
        df['Adj. Close'].plot()
        df['Forecast'].plot()
        plt.legend(loc = 4)
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.show()
        
if  __name__ == '__main__':
    r = Regression()
    Regression.execute()        




