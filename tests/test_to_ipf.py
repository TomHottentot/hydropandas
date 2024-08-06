#%%
import sys 
sys.path.append(r"C:\Users\925793\OneDrive - Royal HaskoningDHV\Python_Learning\hydropandas-1")
import hydropandasTemp as hydropandas

my_extent = (167000, 172500, 472000, 475000) # Define a boundingbox (XMIN, XMAX, YMIN, YMAX)

BRO_Import = hydropandas.read_bro(extent=my_extent)

#%%
Test = BRO_Import.to_IPF()
#%%
Test.insert(3, "screen_top", Test.pop('screen_top'))
