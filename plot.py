# -*- coding: utf-8 -*-
"""
Created on Sat Mar  5 01:53:34 2022

@author: SairamSampath
"""
import pandas as pd
import matplotlib.pyplot as plt

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 14}

plt.rc('font', **font)

# optional: plot the result
# fig, axes = plt.subplots(2, 1, sharex=True)
# df = pd.read_excel("./results1/res_bus/vm_pu.xlsx", index_col=0)
# df.plot(ax=axes[0])
# axes[0].set_ylabel("bus voltage magnitude [p.u.]")

# df = pd.read_excel("./results1/res_line/loading_percent.xlsx", index_col=0)
# df.plot(ax=axes[1])
# axes[1].set_ylabel("line loading [%]")


# [ax.grid() for ax in axes]
# plt.xlabel("Time in Hours ")
# plt.show()

fig, axes = plt.subplots(2, 1, sharex=True)
df = pd.read_excel("./results2_short/res_bus/vm_pu.xlsx", index_col=0)
df.plot(ax=axes[0])
axes[0].set_ylabel("bus voltage magnitude [p.u.]")

df = pd.read_excel("./results2_short/res_line/loading_percent.xlsx", index_col=0)
df.plot(ax=axes[1])
axes[1].set_ylabel("line loading [%]")


[ax.grid() for ax in axes]
plt.xlabel("Time in Hours ")

plt.show()


fig, axes = plt.subplots(2, 1, sharex=True)
df = pd.read_excel("./results1_short/res_bus/vm_pu.xlsx", index_col=0)
df.plot(ax=axes[0])
axes[0].set_ylabel("bus voltage magnitude [p.u.]")

df = pd.read_excel("./results1_short/res_line/loading_percent.xlsx", index_col=0)
df.plot(ax=axes[1])
axes[1].set_ylabel("line loading [%]")



[ax.grid() for ax in axes]
plt.xlabel("Time in Hours ")

plt.show()