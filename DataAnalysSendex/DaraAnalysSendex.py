import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


def state_list():
    # list of abbreviations of all 50 states like AR,AS,TX for quandl datasets
    fiddy_state = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    print(fiddy_state)
    return fiddy_state[0]['Name &postal abbreviation[1]']['Name &postal abbreviation[1].1'][0:]

def grab_initial_state_data():
    states = state_list()
    # print(states)
    main_df = pd.DataFrame()
    for abbv in states:
         query='FMAC/HPI_'+str(abbv)
         df = quandl.get(query,authtoken='XSLEjFZzikQyoSmtmUN6')
         df.rename(columns={'NSA Value': str(abbv) + ' NSA', 'SA Value': str(abbv)+ ' SA'} , inplace=True)
         # PCT
         # df[abbv] = (df[abbv]- df[abbv][0])/(df[abbv][0]*100)
         if main_df.empty:
             main_df = df
         else:
             main_df = main_df.join(df)
    # create pickle files for write
    pickle_out = open('fiddy_state.pickle','wb')
    pickle.dump(main_df,pickle_out)
    pickle_out.close()

grab_initial_state_data() # Run to have new state of dataframe

def HPI_benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken='XSLEjFZzikQyoSmtmUN6')
    df.rename(columns={'NSA Value': 'United States'}, inplace=True)
    df['United States'] = (df['United States'] - df['United States'][0]) / (df['United States'][0] * 100)
    return df

def mortage_30y():
    df = quandl.get("FMAC/MORTG",trim_start='1975-01-01', authtoken='XSLEjFZzikQyoSmtmUN6')
    df['Value'] = (df['Value'] - df['Value'][0]) / (df['Value'][0] * 100)
    df = df.resample('1D').mean()
    df = df.resample('M').mean() # resample do end of month day from 01 01 ro 31 01
    df.rename(columns={'Value':'M30'},inplace=True)
    return df

def sp500_data():
    df = quandl.get("MULTPL/SP500_REAL_PRICE_MONTH", trim_start="1975-01-01", authtoken='XSLEjFZzikQyoSmtmUN6')
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'SP500'}, inplace=True)
    df = df['SP500']
    return df

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken='XSLEjFZzikQyoSmtmUN6')
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value': 'GDP'}, inplace=True)
    df = df['GDP']
    return df

def us_unemployment():
    df = quandl.get("BLSE/CEU0500000001", trim_start="1975-01-01", authtoken='XSLEjFZzikQyoSmtmUN6')
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df.rename(columns={'Value': 'US_UNEMPLY'}, inplace=True)
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    df = df['US_UNEMPLY']
    return df

pickle_in = open('fiddy_state.pickle','rb')

HPI_data = pickle.load(pickle_in) # whole dataframe

sp500 = sp500_data()
gdp = gdp_data()
unemployment = us_unemployment()
m30 = mortage_30y()
benchmark = HPI_benchmark()


# Visualization

fig = plt.figure()
ax1 = plt.subplot2grid((2,1),(0,0))
ax2 = plt.subplot2grid((2,1),(1,0), sharex=ax1)

# benchmark.plot(ax=ax1, color='k',linewidth=10) # plot for whole US
# HPI_data.plot(ax = ax1,label="Monthly")


# Resample

# TX1yr = HPI_data['TX NSA'].resample('A').mean() # resample TX for 1 year
# HPI_data['TX NSA'].plot(ax = ax1,label="Monthly") # plot for monthly
# TX1yr.plot(ax=ax1,label='Annual') # plot for Yearly


# Handling missing data

# HPI_data['TX1yr']=HPI_data['TX NSA'].resample('A').mean() # add new column to create N/A data
# HPI_data.dropna(inplace=True) # drop N/A data
# HPI_data.fillna(method='bfill',inplace=True) # ffill/bfill/value forwrad/backward/value fill N/A data
# HPI_data[['TX NSA','TX1yr']].plot(ax=ax1) # plot for N/A


# Rolling data

# HPI_data['TX12MA'] = HPI_data['TX NSA'].rolling(12).mean() #12 data points/12 moving average
# HPI_data['TX12STD'] = HPI_data['TX NSA'].rolling(12).std() #12 data points/standard deviation
# # HPI_data[['TX NSA','TX12MA']].plot(ax=ax1)
# HPI_data['TX12STD'].plot(ax=ax2)
# TX_AK_12corr = HPI_data['TX NSA'].rolling(12).corr(HPI_data['AK NSA']) #12 data points/correlation between two states
# HPI_data['TX NSA'].plot(ax=ax1, label='TX HPI')
# HPI_data['AK NSA'].plot(ax=ax1, label='AK HPI')
# ax1.legend(loc=4)
# TX_AK_12corr.plot(ax=ax2,label='TX_AK_12corr')


# Mortgage vs HPI TX
#
# state_HPI_M30 = HPI_data.join(m30)
# HPI_M30_corr=state_HPI_M30.corr()['M30']
# print(HPI_M30_corr)
# HPI_M30_12corr = HPI_data['TX NSA'].rolling(12).corr(m30)
# HPI_M30_12corr.plot(ax=ax1,label='TX_AK_12corr')


# All correlation

# HPI= HPI_data.join([m30,sp500,unemployment,gdp,benchmark])
# HPI.dropna(inplace=True)
# HPI_US=HPI[['United States','M30','SP500','GDP','US_UNEMPLY']]
# HPI_corr=HPI[['United States','M30','SP500','GDP','US_UNEMPLY']].corr()
# HPI.to_pickle('HPI.pickle')
# HPI_corr.plot(ax=ax1,label='correlation')
# # HPI_US.plot(ax=ax2,label='US data')
#
# ax1.legend(loc=4)
# ax2.legend(loc=4)
# plt.show()



