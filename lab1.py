# lab1.py
#
# Translation from R to python of econ424lab1.r (E. Zivot, June 27, 2011) 
# author: Ronny De Winter
# created: Januari 4, 2013
# revision history:
#   

import pandas as pd
import matplotlib.pyplot as plt
from numpy import log

# read the sbux prices into a DataFrame object
sbux_df = pd.read_csv('sbuxPrices.csv')

# sbux_df is a DataFrame object. DataFrames are rectangular data objects typically with
# observations in rows and variables in columns
type(sbux_df) # pandas.core.frame.DataFrame
sbux_df
sbux_df.head()
sbux_df.tail()
sbux_df.columns.values
type(sbux_df['Date'])        # pandas.core.series.Series
type(sbux_df['Adj Close'])   # pandas.core.series.Series

#
# subsetting operations
#

# extract the first 5 rows of the price data. 
sbux_df[:5]["Adj Close"]
sbux_df[sbux_df.Date == "1994-03-01"]
sbux_df[sbux_df.Date == "1995-03-01"]
sbux_df[12:25]

# create a new data.frame containing the price data with the dates as the row names
sbux_df = pd.read_csv('sbuxPrices.csv', index_col=0, parse_dates=True)
sbux_df.head()

# with Dates as rownames (ix), you can subset directly on the dates
# find indices associated with the dates 1994-03-01 and 1995-03-01
sbux_df.ix["1994-03-01"]
sbux_df.ix["1995-03-01"]

#
# plot the data
#

# note: the default plot is a "line" plot
plt.plot(sbux_df, label='SBUX')
plt.title('Monthly closing price of SBUX')
plt.ylabel('Adjusted Close')
plt.legend(loc = 'upper left')  # optimize with 'best'
# save the figure
plt.savefig('SBUX-MonthlyClosingPrice.png')

#
# compute returns
#

# simple 1-month returns
sbux_df['rets'] = sbux_df['Adj Close'].pct_change()
sbux_df.rets.head()

# continuously compounded 1-month returns
sbux_df['ccret'] = log(1 + sbux_df.rets)
sbux_df.ccret.head()

# compare the simple and cc returns
sbux_df.head()

# plot the simple and cc returns in separate graphs
# split screen into 2 rows and 1 column
fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
# plot simple returns first
ax1.plot(sbux_df.rets)
ax1.set_title('Monthly Simple Returns on SBUX')
ax1.set_ylabel('Return')
ax1.axhline(0)
# next plot the cc returns
ax2.plot(sbux_df.ccret)
ax2.set_title('Monthly Continuously Compounded Returns on SBUX')
ax2.set_ylabel('Return')
ax2.axhline(0)
# save the figure
plt.savefig('SBUX-Returns-Simple-CC-2fig.png')

# reset the screen to 1 row and 1 column    
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# plot the returns on the same graph
ax.plot(sbux_df.rets, color="blue", label="Simple")
ax.set_ylabel("Return")
ax.set_title("Monthly Returns on SBUX")
# add horizontal line at zero
ax.axhline(0, color='black')     
# add the cc returns
ax.plot(sbux_df.ccret, color="red", label="CC")
# add a legend
ax.legend(loc="lower right")
# save the figure
plt.savefig('SBUX-Returns-Simple-CC-1fig.png')

#
# calculate growth of $1 invested in SBUX
#

# compute gross returns
sbux_df['gret'] = 1 + sbux_df.rets
# compute future values
sbux_df['fv'] = sbux_df.gret.cumprod()
plt.clf()
plt.plot(sbux_df.fv)
plt.title("FV of $1 invested in SBUX")
plt.ylabel("Dollars")
# save the figure
plt.savefig('SBUX-FV.png')

