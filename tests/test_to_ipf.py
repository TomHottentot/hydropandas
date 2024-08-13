#%%
import sys 
import os
sys.path.append(r"C:\Users\925793\OneDrive - Royal HaskoningDHV\Python_Learning\hydropandas-1")
import hydropandasTemp as hydropandas

my_extent = (167000, 172500, 472000, 475000) # Define a boundingbox (XMIN, XMAX, YMIN, YMAX)
utrecht_noord_extent = (133890, 137782, 456000, 457331)
#%%
BRO_Import = hydropandas.read_bro(extent=my_extent, keep_all_obs=False)

#%%
Test = BRO_Import.to_IPF(dirpath = r"c:\Users\925793\Downloads")

#%%
BRO_Import.plots.section_plot(section_colname_x="x", section_label_x="x coordinate [m]")
