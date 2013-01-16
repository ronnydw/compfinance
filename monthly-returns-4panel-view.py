# monthly-returns-4panel-view.py
#
# plot 4 panels on monthly Continuosly Compounded returns:
#   - histogram
#   - smoothed histogram
#   - boxplot
#   - QQ plot
#
# author: Ronny De Winter
# created: Januari 16, 2013
# revision history:
#   

import pandas as pd
import matplotlib.pyplot as plt
from numpy import log
import pandas.io.data as web

# read the MSFT prices into a DataFrame object
msft = web.get_data_yahoo(name='MSFT', start='1998-01-01', end='2012-05-31')['Adj Close']
# resample to monthly 
msft = pd.DataFrame(msft.resample('1M', how='last'), columns=[msft.name])

# simple 1-month returns
msft['rets'] = msft['Adj Close'].pct_change()

# continuously compounded 1-month returns
msft['ccret'] = log(1 + msft.rets)

# split screen into 2 rows and 2 columns
fig = plt.figure(figsize=(9, 6))
ax1 = fig.add_subplot(221) # hist
ax2 = fig.add_subplot(222) # box
ax3 = fig.add_subplot(223) # kde
ax4 = fig.add_subplot(224) # QQ

# sort the CC Returns and create DataFrame (boxplot needs DataFrame)
ccr = pd.DataFrame(msft['ccret'].order().dropna())

# plot histogram
ccr['ccret'].hist(ax=ax1)
ax1.set_xlim(ccr['ccret'][0], ccr['ccret'][-1])
ax1.set_title('MSFT Monthly CC Returns')
ax1.set_xticklabels([''])

# boxplot
ccr.boxplot(ax=ax2)
ax2.set_xticklabels([''])
ax2.yaxis.tick_right()

# smoothed histogram - kde
ccr['ccret'].plot(kind='kde', ax=ax3)
ax3.set_xlim(ccr['ccret'][0], ccr['ccret'][-1])
ax3.set_title('Smoothed density')
ax3.set_ylabel('density estmate')

# qq plot 
import scipy.stats as stats
res = stats.probplot(ccr['ccret'].values, sparams=(ccr.mean(), ccr.std()), plot=plt)
ax4.set_title('Normal Q-Q Plot')
ax4.set_xlabel('Theoretical Quantiles')
ax4.set_ylabel('Sample Quantiles')
ax4.yaxis.tick_right()

plt.show()
plt.savefig('CCmonthlyReturn-4panel-MSFT.png')
