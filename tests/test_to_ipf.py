#%%
import sys 
import os
sys.path.append(r"C:\Users\925793\OneDrive - Royal HaskoningDHV\Python_Learning\hydropandas-1")
import hydropandasTemp
from IPython.display import HTML
#%%
Dennenkamp = (230000, 241000, 480000, 488000)
grave_extent = (177500, 183500, 417000, 422500)
my_extent = (167000, 172500, 472000, 475000) # Define a boundingbox (XMIN, XMAX, YMIN, YMAX)
utrecht_noord_extent = (133890, 137782, 456000, 457331)
lommerbroek = (207500,217500,380000,390000)
#%%
BRO_Import = hydropandasTemp.read_bro(extent=(230000, 241000, 480000, 481000), tmin="2011-01-01")
#%%
BRO_Import_1 = hydropandasTemp.read_bro(extent=(230000, 241000, 481000, 482000), tmin="2011-01-01")

#%%
BRO_Import_2 = hydropandasTemp.read_bro(extent=(230000, 241000, 482000, 483000), tmin="2011-01-01")

#%%
BRO_Import_3 = hydropandasTemp.read_bro(extent=(230000, 241000, 483000, 484000), tmin="2011-01-01")

#%%
BRO_Import_4 = hydropandasTemp.read_bro(extent=(230000, 241000, 484000, 485000), tmin="2011-01-01")

#%%
BRO_Import_5 = hydropandasTemp.read_bro(extent=(230000, 241000, 485000, 486000), tmin="2011-01-01")

#%%
BRO_Import_6 = hydropandasTemp.read_bro(extent=(230000, 241000, 486000, 487000), tmin="2011-01-01") # dit stuk zit een kapotte peilbuis

#%%
BRO_MERGE = BRO_Import.add_obs_collection(BRO_Import_1, inplace=False, overlap = "use_left")
BRO_MERGE_1 = BRO_MERGE.add_obs_collection(BRO_Import_2, inplace=False, overlap = "use_left")
BRO_MERGE_2 = BRO_MERGE_1.add_obs_collection(BRO_Import_3, inplace=False, overlap = "use_left")
BRO_MERGE_3 = BRO_MERGE_2.add_obs_collection(BRO_Import_4, inplace=False, overlap = "use_left")
BRO_MERGE_4 = BRO_MERGE_3.add_obs_collection(BRO_Import_5, inplace=False, overlap = "use_left")
BRO_MERGE_5 = BRO_MERGE_3.add_obs_collection(BRO_Import_6, inplace=False, overlap = "use_left")

#%%
BRO_Import = hydropandasTemp.read_bro(grave_extent)
BRO_Import = hydropandasTemp.read_bro(Dennenkamp, tmin="2011-01-01")
#%%

BRO_MERGE_3.geo.set_lat_lon()
BRO_MERGE_3.plots.interactive_plots()

#%%
Obs_no = BRO_Import.stats.get_no_of_observations()
NonEmptyObs = Obs_no[Obs_no > 0]
SelectedObs = BRO_Import[BRO_Import.index.isin(NonEmptyObs.index)]

temp = SelectedObs.drop([9])
#%%
BRO_Import_3.plots.section_plot()
BRO_MERGE_4.to_IPF(dirpath = r"c:\Users\925793\Downloads")

#%%
BRO_Import = hydropandasTemp.read_bro(my_extent)
#%%
test = BRO_Import.to_Menyanthes(dirpath = r"c:\Users\925793\Downloads")

#%%

DennenkampPickle = hydropandasTemp.read_pickle("c:/Users/925793/Downloads/Dennenkamp.pkl")

#%%
DennenkampPickle.to_Menyanthes(dirpath = r"c:\Users\925793\Downloads")
