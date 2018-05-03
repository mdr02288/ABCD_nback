import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.xkcd()

fname = '/Users/tariqcannonier/Desktop/ABCD PsychoPy/ABCD NBACK/data/NDAR_INVABCD1234/NDAR_INVABCD1234_WM_12.csv'
data = pd.read_csv(fname)

accuracy = data['Stim.ACC']
accuracy = accuracy.dropna(axis=0, how='any')
rt = data['Stim.RT']
rt = rt.dropna(axis=0,how='any')

fig, ax = plt.subplots(1,2)
ax[0].bar(1,np.mean(accuracy),align='center')
ax[0].set_xlim([0.5,1.5])
ax[0].set_xticks([])

ax[1].bar(1,np.mean(rt[rt>0]),align='center')
ax[1].bar(np.arange(len(accuracy[0:7])),accuracy[0:7],align='center')

#plt.bar(1,np.mean(accuracy),align='center')

plt.show()