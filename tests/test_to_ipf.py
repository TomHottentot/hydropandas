#%%
import hydropandas

#%%
my_extent = (167000, 172500, 472000, 476000) # Define a boundingbox (XMIN, XMAX, YMIN, YMAX)

#%%
BRO_Import = hydropandas.read_bro(extent=my_extent)

#%%
BRO_Import.to_IPF()
#%%
BRO_Import.drop(columns=['obs', 'filename', 'unit','metadata_available'])