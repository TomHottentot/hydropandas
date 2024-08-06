import hydropandas as hdp

#%%
my_extent = (167000, 172500, 472000, 476000) # Define a boundingbox (XMIN, XMAX, YMIN, YMAX)

#%%
BRO_Import = hdp.read_bro(extent=my_extent)

#%%
BRO_Import.to_IPF()