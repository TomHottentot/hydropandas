import numpy as np
import pandas as pd
import os

from .. import observation
from ..observation import Obs, GroundwaterObs, WaterlvlObs

def to_IPF(self):
        Obs_no = self.stats.get_no_of_observations()
        NonEmptyObs = Obs_no[Obs_no > 0]
        SelectedObs = self[self.index.isin(NonEmptyObs.index)]
        file_location = os.getcwd()
        IPFpath = rf'{file_location}/IPF'
        timeseries_path = rf'{IPFpath}/TimeSeries'

        if not os.path.exists(rf'{file_location}/IPF'):
            os.makedirs(rf"{file_location}/IPF")
        if not os.path.exists(rf'{file_location}/IPF/TimeSeries'):
            os.makedirs(rf'{file_location}/IPF/TimeSeries')

        SelectedObs = SelectedObs.drop(columns=['obs', 'filename', 'unit','metadata_available'])
        SelectedObs['id'] = "TimeSeries\\" + SelectedObs["monitoring_well"].astype(str) + "_" +  SelectedObs["tube_nr"].astype(str)
        
        SelectedObs.insert(3, "screen_top", SelectedObs.pop('screen_top'))
        SelectedObs.insert(4, "screen_bottom", SelectedObs.pop('screen_bottom'))
        
        col_num_timeseries_id = SelectedObs.columns.get_loc("id") + 1

        HeaderString = f"{len(SelectedObs)}\n{len(SelectedObs.columns)}\n"
        poststring = f"\n{col_num_timeseries_id},txt\n"
        header = HeaderString + '\n'.join(SelectedObs.columns) + poststring
        SelectedObsText = SelectedObs.to_string(header = False, index = False)

        with open(rf"{IPFpath}\GroundwaterObs.ipf", 'w') as file:
            file.write(header)
            file.write(SelectedObsText)
        print(f"All groundwater observations containing data ({len(SelectedObs)}) have been writen to GroundwaterObs.ipf")
        
        for i in range(SelectedObs.shape[0]):
            print(SelectedObs.iloc[i]['monitoring_well'])
            monitoring_well_id = SelectedObs.monitoring_well.iloc[i]
            filename = SelectedObs.index.astype(str)
            tubenumber = SelectedObs.tube_nr.iloc[i]
            tube_number = int(SelectedObs.tube_nr.iloc[i])
            time_series = GroundwaterObs.from_bro(monitoring_well_id, tube_number)
            time_series['timestamp'] = time_series.index
            time_series_daily = time_series.groupby(time_series.timestamp.dt.date)['values'].mean()
            time_series_simplified = pd.DataFrame({'date':time_series_daily.index, 'HEAD':time_series_daily.values})
            time_series_simplified['DOB'] = pd.to_datetime(time_series_simplified['date'])
            time_series_simplified['Date'] = time_series_simplified['DOB'].dt.strftime('%Y%m%d')
            output = time_series_simplified.drop(columns=['date', 'DOB'])
            output=output.reindex(columns=["Date","HEAD"])
            save_filepath = rf'{timeseries_path}/{monitoring_well_id}_{tubenumber}.txt'
            pre_string = f""" 
            {len(output)}
            2
            Date -999
            HEAD -999
            """
            output_string = output.to_string(header = False, index = False)
            with open(save_filepath, 'w') as file:
                file.write(pre_string)
                file.write(output_string)
        print(f"Time series for ({len(SelectedObs)}) GroundwaterObs have been writen to the folder TimeSeries")
        return SelectedObs 