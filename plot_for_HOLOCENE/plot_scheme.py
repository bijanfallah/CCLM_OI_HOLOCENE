'''
Program to plot da scheme for HOLOCENE


'''
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy import stats


random.seed(777)
fig, ax = plt.subplots(1)
fig.set_size_inches(16,8)
s = np.array(np.ones(30))
d1=np.random.random(30)*.3
random.seed(777)
d2=np.random.random(30)*.3
target = s+d1-d2
plt.plot(target,'o-', c= 'green')
ax.set_xlabel('$time$',size= 35)
ax.set_ylabel('$X^{Model}$',size= 35)


ax.set_xlim([-1,36])
sig = np.std(target)
mea = np.mean(target)
x = np.linspace(mea - 2*sig, mea + 2*sig, 1000)
iq = stats.norm(mea, sig)
#plt.plot(iq.pdf(x)+32, x, 'g-',lw=3)

ann1 = ax.annotate("Proxy",
                   xy=(15,1.06),xycoords='data',
                   xytext=(20,1.27), textcoords='data',
                   size=30, va="center", ha="center",
                   arrowprops=dict(arrowstyle="-|>",
                                   connectionstyle="arc3,rad=-0.2",
                                   fc="w", lw=3),
                   )

ann2 = ax.annotate('',xy=(33,(1+sig)),xycoords='data',
                   xytext=(33,(1-sig)), textcoords='data',
                   arrowprops=dict(arrowstyle="<->", lw=3, fc='g', ec='g'),
                   )
plt.text(31.5,1,"$1\sigma$",rotation='vertical', size=30, color='g')
plt.scatter(33.5,1,marker='.', s=300, c='g')
plt.text(34,1,"$\mu$",rotation='horizontal', size=30, color='g')
plt.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
plt.tick_params(axis='y',which='both',right='off',left='off',labelleft='off')
plt.errorbar(15,1.06, yerr=.07,lw=1,c='red')
plt.scatter(15,1.06,marker='o', s=300, c='red')

plt.savefig("bij01.pdf")

plt.close()