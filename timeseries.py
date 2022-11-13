# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 19:27:37 2022

@author: saira
"""

import pathlib

import matplotlib.pyplot as plt
import pandas as pd

import pandapower as pp
import pandapower.networks as nw
from pandapower import pp_dir
from pandapower.control.controller.const_control import ConstControl
from pandapower.timeseries.data_sources.frame_data import DFData
from pandapower.timeseries.output_writer import OutputWriter
from pandapower.timeseries.run_time_series import run_timeseries


def create_distribution_network():
    """
    Returns the simple example network from the pandapower tutorials.

    OUTPUT:
        net - simple example network

    EXAMPLE:

    >>> import pandapower.networks
    >>> net = pandapower.networks.example_simple()

    """
    net = pp.create_empty_network()

    # create buses
    bus1 = pp.create_bus(net, name="HV Busbar", vn_kv=110., type="b")
    bus2 = pp.create_bus(net, name="HV Busbar 2", vn_kv=110., type="b")
    bus3 = pp.create_bus(net, name="HV Transformer Bus", vn_kv=110., type="n")
    bus4 = pp.create_bus(net, name="MV Transformer Bus", vn_kv=20., type="n")
    bus5 = pp.create_bus(net, name="MV Main Bus", vn_kv=20., type="b")
    bus6 = pp.create_bus(net, name="MV Bus 6", vn_kv=20., type="b")
    bus7 = pp.create_bus(net, name="MV Bus 7", vn_kv=20., type="b")
    
    bus6_1 = pp.create_bus(net, name="MV Bus 6_1", vn_kv=20., type="b")
    
    
    bus7_1 = pp.create_bus(net, name="MV Bus 7_1", vn_kv=20., type="b")
    
    bus8 = pp.create_bus(net, name="MV Bus 8", vn_kv=20., type="b")
    bus8_1 = pp.create_bus(net, name="LV Bus 8_1", vn_kv=0.4, type="b")
    bus8_2 = pp.create_bus(net, name="LV Bus 8_2", vn_kv=0.4, type="b")
    

    # create ex#ternal grid
    pp.create_ext_grid(net, bus1, vm_pu=1.02, va_degree=50)

    # create transformer
    pp.create_transformer(net, bus3, bus4, name="110kV/20kV transformer",
                                   std_type="25 MVA 110/20 kV")
    
    pp.create_transformer_from_parameters(net, bus8, bus8_1,
                                          sn_mva=10, vn_hv_kv=20, vn_lv_kv=0.4,
                                          vkr_percent=1.325, vk_percent=4,
                                          pfe_kw=0.95, i0_percent=0.2375, tap_side="hv",
                                          tap_neutral=0, tap_min=-2, tap_max=2,
                                          tap_step_percent=2.5, tap_pos=0,
                                          shift_degree=150, name='MV-LV-Trafo')
    # create lines
    pp.create_line(net, bus1, bus2, length_km=10,
                           std_type="N2XS(FL)2Y 1x300 RM/35 64/110 kV", name="Line 1")
    line2 = pp.create_line(net, bus5, bus6, length_km=2.0,
                           std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 2")
    line3 = pp.create_line(net, bus6, bus6_1, length_km=3.5,
                           std_type="48-AL1/8-ST1A 20.0", name="Line 3")
    line4 = pp.create_line(net, bus7, bus5, length_km=2.5,
                           std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 4")
    line5 = pp.create_line(net, bus7, bus7_1, length_km=1,
                           std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 5")
    line6 = pp.create_line(net, bus5, bus8, length_km=0.5,
                           std_type="NA2XS2Y 1x240 RM/25 12/20 kV", name="Line 6")
    
    line7 = pp.create_line(net, bus8_1, bus8_2, length_km=0.1,
                           std_type="94-AL1/15-ST1A 0.4", name="Line 7")

    # create bus-bus switches
    pp.create_switch(net, bus2, bus3, et="b", type="CB")
    pp.create_switch(net, bus4, bus5, et="b", type="CB")

    # create bus-line switches
    pp.create_switch(net, bus5, line2, et="l", type="LBS", closed=True)
    pp.create_switch(net, bus6, line2, et="l", type="LBS", closed=True)
    pp.create_switch(net, bus6, line3, et="l", type="LBS", closed=True)
    #pp.create_switch(net, bus7, line3, et="l", type="LBS", closed=False)
    pp.create_switch(net, bus7, line4, et="l", type="LBS", closed=True)
    pp.create_switch(net, bus5, line4, et="l", type="LBS", closed=True)
    

    # create load
    pp.create_load(net, bus7, p_mw=1, q_mvar=2, scaling=0.6, name="load bus 7")
    pp.create_load(net, bus6, p_mw=1, q_mvar=2, scaling=0.6, name="load bus 6")
    
    pp.create_load(net, bus7_1, p_mw=1, q_mvar=2, scaling=0.6, name="load bus 7_1")
    pp.create_load(net, bus6_1, p_mw=1, q_mvar=2, scaling=0.6, name="load bus 6_1")
    pp.create_load(net, bus8_1, p_mw=1, q_mvar=2, scaling=0.6, name="load bus 8_1")
    pp.create_load(net, bus8_2, p_mw=0.12, q_mvar=0.24, scaling=0.6, name="load bus 8_2")

    # create generator
    pp.create_gen(net, bus6, p_mw=6, max_q_mvar=3, min_q_mvar=-3, vm_pu=1.03,
                  name="generator")

    # create static generator
    

    # create shunt
    pp.create_shunt(net, bus3, q_mvar=-0.96, p_mw=0, name='Shunt')

    return net

# open the grid and modify it
net = create_distribution_network()
net.gen.drop(net.gen.index, inplace=True)
pp.create_sgen(net, 5, p_mw=1, name="Wind Bus 6")
pp.create_sgen(net, 7, p_mw=2, q_mvar=-0.5, name="PV bus 6_1")
pp.create_sgen(net, 6, p_mw=2, q_mvar=-0.5, name="PV bus 7")
pp.create_sgen(net, 10, p_mw=1, q_mvar=-0.5, name="PV bus 8_1")
#pp.create_sgen(net, 11, p_mw=0.5, q_mvar=-0.5, name="PV bus 8_2")


pp.create_storage(net, 5, p_mw=0.5, max_e_mwh=.2, soc_percent=50., q_mvar=0., controllable=True)
pp.create_storage(net, 8, p_mw=0.5, max_e_mwh=.2, soc_percent=50., q_mvar=0., controllable=True)
pp.create_storage(net, 6, p_mw=0.5, max_e_mwh=.2, soc_percent=50., q_mvar=0., controllable=True)
pp.create_storage(net, 10, p_mw=0.5, max_e_mwh=.2, soc_percent=50., q_mvar=0., controllable=True)

# create the data source for the controller

df = pd.read_excel(r"C:\Users\SairamSampath\Desktop\New folder\Timeseriesmodel\Model 1\data.xlsx")
df.loc[:,["PV","Wind","Residential1","EV"]].plot()
plt.xlabel("time steps")
plt.ylabel("Power in MW")
print(df.head())
ds = DFData(df)

# add controller for sgens and loads
ConstControl(net, "sgen", "p_mw", element_index=net.sgen.index, profile_name=["Wind", "PV", "PV", "PV_LV1"], data_source=ds)
ConstControl(net, "load", "p_mw", element_index=net.load.index, profile_name=["Residential1","Residential2","Residential3","Residential4", "Residential_LV", "Residential_LV2"], data_source=ds)
ConstControl(net, "storage", "p_mw", element_index=net.storage.index, profile_name=["EV3","EV3","EV3","EV_LV2"], data_source=ds)
#ConstControl(net, "storage", "p_mw", element_index=net.storage.index, profile_name=["EV2","EV2","EV2","EV_LV1"], data_source=ds)
#ConstControl(net, "load", "q_mvar", element_index=1, profile_name=["Residential"], data_source=ds)

# add the output writer to store results
ow = OutputWriter(net, time_steps=(0, 95), output_path="./results/", output_file_type=".xlsx")
# these values are logged by default anyway and must not be explicitly set
# ow.log_variable("res_bus", "vm_pu")
# ow.log_variable("res_line", "loading_percent")

# run the time series
run_timeseries(net, time_steps=range(0, 95))

# optional: plot the result
fig, axes = plt.subplots(2, 1, sharex=True)
df = pd.read_excel("./results/res_bus/vm_pu.xlsx", index_col=0)
df.plot(ax=axes[0])
axes[0].set_ylabel("bus voltage magnitude [p.u.]")

df = pd.read_excel("./results/res_line/loading_percent.xlsx", index_col=0)
df.plot(ax=axes[1])
axes[1].set_ylabel("line loading [%]")


[ax.grid() for ax in axes]
plt.xlabel("time steps")
plt.show()



