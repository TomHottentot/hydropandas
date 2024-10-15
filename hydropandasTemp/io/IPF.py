import numpy as np
import pandas as pd
import os

from .. import observation
from ..observation import Obs, GroundwaterObs, WaterlvlObs

def to_IPF(self, dirpath):
    """Write an ObsCollection to an iMOD IPF file including a folder with timeseries data..
    
    Parameters
    ----------
    dirpath : str
    full directory path of the folder where the IPF-file and timeseries folder should be stored.

    Returns
    -------
    SelectedObs : pastastore.PastaStore
        the ObsColelction with the non-empty observations from the ObsCollection
    """
    Obs_no = self.stats.get_no_of_observations()
    NonEmptyObs = Obs_no[Obs_no > 0]
    print(f'{len(NonEmptyObs)} of {len(self)} obs have timeseries data')
    if(len(NonEmptyObs == 0)):
        e =3
    else:
        e = 4 #

    SelectedObs = self[self.index.isin(NonEmptyObs.index)]
    MeanList = list(SelectedObs.stats.get_seasonal_stat(winter_months=(1,2,3,4,5,6,7,8,9,10,11,12)).iloc[:, 0])
    file_location = os.getcwd()
    IPFpath = rf'{dirpath}\IPF'
    timeseries_path = rf'{dirpath}\IPF\TimeSeries'

    if not os.path.exists(IPFpath):
        os.makedirs(IPFpath)
    if not os.path.exists(timeseries_path):
        os.makedirs(timeseries_path)

    SelectedObs = SelectedObs.drop(columns=['obs',
                                            'filename',
                                            'unit',
                                            'metadata_available']
                                            )
    SelectedObs['id'] = ("TimeSeries\\" 
                         + SelectedObs["monitoring_well"].astype(str)
                         + "_"
                         + SelectedObs["tube_nr"].astype(str)
                         )
    SelectedObs['Mean'] = MeanList
    SelectedObs.insert(3,
                       "screen_top",
                       SelectedObs.pop('screen_top')
                       )
    SelectedObs.insert(4,
                       "screen_bottom",
                       SelectedObs.pop('screen_bottom')
                       )
    col_num_timeseries_id = SelectedObs.columns.get_loc("id") + 1

    HeaderString = f"{len(SelectedObs)}\n{len(SelectedObs.columns)}\n"
    PostString = f"\n{col_num_timeseries_id},txt\n"
    header = HeaderString + '\n'.join(SelectedObs.columns) + PostString
    SelectedObsText = SelectedObs.to_string(header = False, index = False)

    with open(rf"{IPFpath}\GroundwaterObs.ipf", 'w') as file:
        file.write(header)
        file.write(SelectedObsText)
    
    for i in range(SelectedObs.shape[0]):
        print(SelectedObs.iloc[i]['monitoring_well'])
        MonitoringWell_ID = SelectedObs.monitoring_well.iloc[i]
        filename = SelectedObs.index.astype(str)
        tubenumber = SelectedObs.tube_nr.iloc[i]
        tube_number = int(SelectedObs.tube_nr.iloc[i])
        TimeSeries = GroundwaterObs.from_bro(MonitoringWell_ID,
                                              int(SelectedObs.tube_nr.iloc[i]))
        TimeSeries['timestamp'] = TimeSeries.index
        TimeSeriesDaily = TimeSeries.groupby(TimeSeries.timestamp.dt.date)['values'].mean()
        TimeSeriesSimplified = pd.DataFrame({'date':TimeSeriesDaily.index,
                                             'HEAD':TimeSeriesDaily.values})
        TimeSeriesSimplified['DOB'] = pd.to_datetime(TimeSeriesSimplified['date'])
        TimeSeriesSimplified['Date'] = TimeSeriesSimplified['DOB'].dt.strftime('%Y%m%d')
        output = TimeSeriesSimplified.drop(columns=['date', 'DOB'])
        output = output.reindex(columns=["Date","HEAD"])
        save_filepath = rf'{timeseries_path}/{MonitoringWell_ID}_{SelectedObs.tube_nr.iloc[i]}.txt'
        pre_string = f"""
        {len(output)}
        2
        Date -999
        HEAD -999
        """
        output_string = output.to_string(header = False, index = False)
        with open(save_filepath, 'w') as file:
            file.write(pre_string)
            file.write(output.to_string(header = False, index = False))
    print(f"Time series for ({len(SelectedObs)}) GroundwaterObs have been writen to the folder TimeSeries")
    return SelectedObs