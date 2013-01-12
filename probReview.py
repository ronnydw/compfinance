# probReview.py
#
# Coursera "Introduction to Computational Finance and Financial Econometrics" - University of Washington, E. Zivot
# Translation from R to python of probReview.r (E. Zivot, June 26, 2012) 
# author: Ronny De Winter
# created: Januari 10, 2013
# revision history:
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### Univariate distributions ###

#
# discrete distribution for msft
#

r_msft = [-.3, 0, .1, .2, .5]
prob_vals = [.05, .2, .5, .2, .05]
data = pd.Series(prob_vals, index=r_msft)
# probablity bar plot 
data.plot(kind='bar')
plt.xlabel('Return')
plt.title('Annual Return on Microsoft')
plt.savefig('prob-bar-msft-annualReturn.png')
# alternatively create spike plot
plt.clf()
plt.scatter(r_msft, prob_vals)
plt.vlines(r_msft, 0, prob_vals)
plt.ylim(ymin=0)
plt.xticks(r_msft)
plt.xlabel('return')
plt.ylabel('probablity')
plt.savefig('prob-spike-plot.png')

# plot cumulative distributon function (cdf) of discrete dist
cdf = [0, .05, .25, .75, .95, 1]
x = [-.4, -.3, 0, .1, .2, .5]
plt.clf()
plt.step(x, cdf, linewidth=3.0)
plt.xticks(x)
plt.ylabel('cdf')
plt.savefig('cdf-discreteDistribution.png')

#
# Standard normal distributions
#
from scipy.stats import norm
x = np.linspace(-4,4,150)
# plot density
plt.clf()
plt.plot(x,norm.pdf(x))
plt.xlabel('x')
plt.ylabel('pdf')
plt.savefig('pdf-normalDistribution.png')
# plot cdf
plt.clf()
plt.plot(x,norm.cdf(x))
plt.xlabel('x')
plt.ylabel('cdf')
plt.savefig('cdf-normalDistribution.png')

# plot density with shaded area showing Pr(-2 <= x <= 1)
lb = -2
ub = 1
d=norm.pdf(x)
plt.clf()
plt.plot(x, d)
sx = np.linspace(lb,ub,100)
sd = norm.pdf(sx)
plt.fill_between(sx, sd, 0, color = 'b')
plt.savefig('pdf-normalDist-segmentFilled.png')

# compute quantiles
a_vals = [.01, .05, .1, .5]
q_vals = norm.ppf(a_vals)
q_vals

# area under normal curve
# Pr(X >= 2) = Pr(X <= -2)
norm.cdf(-2)
# Pr(-1 <= X <= 2)
norm.cdf(2) - norm.cdf(-1)
# Pr(-1 <= X <= 1)
norm.cdf(1) - norm.cdf(-1)
# Pr(-2 <= X <= 2)
norm.cdf(2) - norm.cdf(-2)
# Pr(-3 <= X <= 3)
norm.cdf(3) - norm.cdf(-3)

#
# General normal distribution
#

# Example: R ~ N(0.01, 0.10)
mu = .01
sd = .1
x = np.linspace(-4,4,150) * sd + mu
plt.clf()
plt.plot(x, norm.pdf(x, mu, sd), color='b')
plt.vlines(mu, 0, norm.pdf(mu, mu, sd), color='b')
plt.savefig('pdf-general-normalDist.png')

norm.cdf(-.5, .01, .1)
norm.cdf(0, .01, .1)
1 - norm.cdf(.5, .01, .1)
1 - norm.cdf(1, .01, .1)

a_vals = [.01, .05, .95, .99]
norm.ppf(a_vals, .01, .1)

# Example: risk-return tradeoff
mu_r = .02
sd_r = .1
x = np.linspace(-3,3,150) * sd_r + mu_r 
plt.clf()
plt.plot(x, norm.pdf(x, mu_r, sd_r), color='k', label='Amazon')
plt.vlines(mu_r, 0, norm.pdf(mu_r, mu_r, sd_r))
plt.plot(x, norm.pdf(x, .01, .05), 'b--', label='Boeing')
plt.vlines(.01, 0, norm.pdf(.01, .01, .05), color='b', linestyles='dashed')
plt.legend()
plt.xlabel('x')
plt.ylabel('pdf')
plt.savefig('pdf-risk-return-tradeoff.png')

#
#  log-normal distrbution
#

# example: r(t) = ln(1 + R(t)) ~ N(0.05, (0.5)^2))
#          1 + R(t) = exp(r(t)) ~ logNormal(0.05, (0.5)^2)
#          R(t) = e(r(t)) - 1 ~ logNormal(0.05, (0.5)^2) - 1
#

# plot normal and log normal density

from scipy.stats import lognorm
mu = .05
sd = .5
x = np.linspace(mu - 3 * sd, mu + 3 * sd, 100)
plt.clf()
plt.plot(x, norm.pdf(x, mu, sd), label="Normal") 
plt.plot(np.exp(x)-1, lognorm.pdf(np.exp(x), sd, mu), '--', label="Log-Normal")
plt.legend()
plt.savefig('pdf-normal-vs-lognormal.png')

# TODO: Student's t distribution (hint: scipy.stats.t)

#
# Value-at-Risk calculations
#

w0 = 10000
# plot return, wealth, and loss distributions
mu_R = .05
sd_R = .1
R = np.linspace(mu_R - 3 * sd_R, mu_R + 3 * sd_R, 100)
mu_w1 = 10500
sd_w1 = 1000
w1 = np.linspace(mu_w1 - 3 * sd_w1, mu_w1 + 3 * sd_w1, 100)
L = w0 * R
mu_L = w0 * mu_R
sd_L = w0 * sd_R
# compute 5% quantile for return, wealth, and loss distributions
q_R_05 = norm.ppf(.05, mu_R, sd_R)
q_w1_05 = norm.ppf(.05, mu_w1, sd_w1)
q_L_05 = norm.ppf(.05, mu_L, sd_L)  

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(3, 1, 1) # Return distribution 
ax2 = fig.add_subplot(3, 1, 2) # Wealth distribution
ax3 = fig.add_subplot(3, 1, 3) # Loss distribution
fig.subplots_adjust(hspace=0.4)
# plot return density
ax1.plot(R, norm.pdf(R, mu_R, sd_R))
ax1.axvline(q_R_05, color='r')
ax1.set_title("Return R(t) ~ N(0.05,(.10)^2)")
ax1.set_xlabel("R")
ax1.set_ylabel("pdf")
# plot wealth density
ax2.plot(w1, norm.pdf(w1, mu_w1, sd_w1))
ax2.axvline(q_w1_05, color='r')
ax2.set_title("Wealth W1 ~ N(10,500,(1,000)^2)")
ax2.set_xlabel("W1")
ax2.set_ylabel("pdf")
ax2.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
# plot loss density
ax3.plot(L, norm.pdf(L, mu_L, sd_L))
ax3.axvline(q_L_05, color='r')
ax3.set_title("Loss R*W0 ~ N(500,(1,000)^2)")
ax3.set_xlabel("W0*R")
ax3.set_ylabel("pdf")
ax3.ticklabel_format(style='sci', scilimits=(0,0), axis='y')
ax3.text(-2500, .0002, "5% VaR", color='r')
plt.savefig('VaR-normalDist-Return-Wealth-Loss.png')

#
# TODO: bivariate distributions
#

