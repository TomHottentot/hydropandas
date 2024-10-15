#%%
import sys 
import os
import pandas as pd
import hydropandas as hdp

sys.path.append(r"C:\Users\925793\OneDrive - Royal HaskoningDHV\Python_Learning\hydropandas-1")
import hydropandasTemp as hydropandas

#%%
def to_Menyanthes(self, dirpath):
        """Write an ObsCollection to an HydroHonitor formatted .csv file.  
        
        Parameters
        ----------
        dirpath : str
        full directory path of the folder where a folder with an IPF-file and timeseries folder should be stored.

        Returns
        -------
        SelectedObs: GroundwaterObs
                     hydropandas observation object.
        the ObsColelction with the non-empty observations from the ObsCollection
        """
        col1 = ['Format Name',
                'Format Version',
                'Format Definition',
                'File Type',
                'File Contents',
                'Object Type',
                'Object Identification'] 
        col2 = ['HydroMonitor - open data exchange format',
                '1.0',
                'http://hydromonitor.nl/downloads/hydromonitor_data_exchange_format.pdf',
                'CSV',
                'Header',
                'ObservationWell',
                'Name']
        col3 = ['', 
                '',
                '',
                '',
                'Metadata',
                '',
                'FilterNo'] 
        col4 = ['', 
                '',
                '',
                '',
                'Data',
                '',
                ''] 
        header2 = pd.DataFrame({'col1': col1, 
                                'col2': col2, 
                                'col3': col3, 
                                'col4': col4})

        Obs_no = self.stats.get_no_of_observations()
        NonEmptyObs = Obs_no[Obs_no > 0]
        SelectedObs = self[self.index.isin(NonEmptyObs.index)]

        for i in range(SelectedObs.shape[0]):
                MonitoringWell_ID = SelectedObs.monitoring_well.iloc[i]
                TimeSeries = hdp.GroundwaterObs.from_bro(
                        MonitoringWell_ID, 
                        int(SelectedObs.tube_nr.iloc[i]))
                LocatiePeilbuis = [TimeSeries.monitoring_well] * len(TimeSeries)
                FilternummerTimeSeries = [TimeSeries.tube_nr] * len(TimeSeries)
                PeilDatumTijd = [t.strftime("%d-%m-%Y %H:%M") 
                                 for t in TimeSeries.index]
                StandNAP = TimeSeries['values']
                ManualHead = TimeSeries['values']

                TimeSeriesZipped = list(zip(LocatiePeilbuis, 
                                FilternummerTimeSeries, 
                                PeilDatumTijd, 
                                StandNAP, 
                                ManualHead))
                TimeSeriesObs = pd.DataFrame(TimeSeriesZipped, 
                                             columns=['Name',
                                                      'FilterNo',
                                                      'DateTime',
                                                      'LoggerHead',
                                                      'ManualHead'])

                if(i == 0):
                        TimeSeriesModule = TimeSeriesObs
                else:
                        TimeSeriesModule = pd.concat([TimeSeriesModule,
                                                      TimeSeriesObs])
        
        TimeSeriesModuleCols = TimeSeriesModule.columns.to_list()
        TimeSeriesModuleUnits = ['[String]',
                                 '[Integer]',
                                 '[dd-mm-yyyy HH:MM]',
                                 '[m+ref]',
                                 '[m+ref]']
        TimeSeriesModuleHeader = pd.DataFrame([TimeSeriesModuleCols, 
                                               TimeSeriesModuleUnits])

        #### Description Module
        Locatie = SelectedObs['monitoring_well']
        FilterNummer = SelectedObs['tube_nr']
        ExterneAanduiding = [""] * len(SelectedObs)
        X_Coordinaat = SelectedObs['x']
        Y_Coordinaat = SelectedObs['y']
        Maaiveld = SelectedObs['ground_level']
        Geschat = [""]* len(SelectedObs)
        PeilbuisTop = SelectedObs['tube_top']
        BovenkantFilter = SelectedObs['screen_top']
        OnderkantFilter = SelectedObs['screen_bottom']
        StartDatum = [t.strftime("%d-%m-%Y %H:%M") 
                      for t in SelectedObs.stats.dates_first_obs.to_list()]
        EindeDatum = [t.strftime("%d-%m-%Y %H:%M") 
                      for t in SelectedObs.stats.dates_last_obs.to_list()]
        EmptyDummy = [""]* len(SelectedObs)
        
        DescriptionZipped = list(zip(Locatie,
                                     ExterneAanduiding,
                                     ExterneAanduiding,
                                     FilterNummer, 
                                     StartDatum, #Dummy for StartDateTime
                                     X_Coordinaat, 
                                     Y_Coordinaat,
                                     Maaiveld,
                                     PeilbuisTop,
                                     BovenkantFilter,
                                     OnderkantFilter,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy,
                                     EmptyDummy))

        DescriptionModule = pd.DataFrame(DescriptionZipped, 
                                         columns=['Name',
                                                  'NITGCode',
                                                  'OLGACode',
                                                  'FilterNo', 
                                                  'StartDateTime',
                                                  'XCoordinate',
                                                  'YCoordinate',
                                                  'SurfaceLevel',
                                                  'WellTopLevel',
                                                  'FilterTopLevel',
                                                  'FilterBottomLevel',
                                                  'WellBottomLevel',
                                                  'LoggerSerial',
                                                  'LoggerDepth',
                                                  'LoggerBrand',
                                                  'LoggerType',
                                                  'Comment',
                                                  'CommentBy',
                                                  'Organization',
                                                  'Status'])

        DescriptionModuleCols = DescriptionModule.columns.to_list()

        DescriptionModuleUnits = ['[String]',
                                  '[String]',
                                  '[String]',
                                  '[Integer]',
                                  '[dd-mm-yyyy HH:MM]',
                                  '[m]',
                                  '[m]',
                                  '[m+ref]',
                                  '[m+ref]',
                                  '[m+ref]',
                                  '[m+ref]',
                                  '[m+ref]',
                                  '[String]',
                                  '[m]',
                                  '[Categorical]',
                                  '[Categorical]',
                                  '[String]',
                                  '[String]',
                                  '[String]',
                                  '[Categorical]']
        
        DescriptionModuleHeader = pd.DataFrame([DescriptionModuleCols, 
                                                DescriptionModuleUnits])

        #### Write CSV file
        with open(f'{dirpath}\BRO2Menyanthes.csv', 'w',newline='') as file:
                file.write(header2.to_csv(index = False, 
                                          header = False, 
                                          sep = ';', 
                                          decimal = ","))
                file.write(";\n")
                file.write(DescriptionModuleHeader.to_csv(index = False, 
                                                          header = False, 
                                                          sep = ';', 
                                                          decimal = ","))
                file.write(DescriptionModule.to_csv(index = False, 
                                                    header = False, 
                                                    sep = ';', 
                                                    decimal = ","))
                file.write(";\n")
                file.write(TimeSeriesModuleHeader.to_csv(index = False, 
                                                         header = False, 
                                                         sep = ';', 
                                                         decimal = ","))
                file.write(TimeSeriesModule.to_csv(index = False, 
                                                   header = False, 
                                                   sep = ';', 
                                                   decimal = ","))
