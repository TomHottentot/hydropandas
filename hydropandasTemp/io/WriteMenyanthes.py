#%%
import sys 
import os
import pandas as pd
import hydropandas as hdp

sys.path.append(r"C:\Users\925793\OneDrive - Royal HaskoningDHV\Python_Learning\hydropandas-1")
import hydropandasTemp as hydropandas


#%%
my_extent = (167000, 172500, 472000, 475000) # Define a boundingbox (XMIN, XMAX, YMIN, YMAX)
utrecht_noord_extent = (133890, 137782, 456000, 457331)
#%%
BRO_Import = hydropandas.read_bro(extent=my_extent)

#%%
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
header2 = pd.DataFrame({'col1': col1, 'col2': col2, 'col3': col3, 'col4': col4})

#%%

def to_Menyanthes(self, dirpath):
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
        header2 = pd.DataFrame({'col1': col1, 'col2': col2, 'col3': col3, 'col4': col4})

        Obs_no = self.stats.get_no_of_observations()
        NonEmptyObs = Obs_no[Obs_no > 0]
        SelectedObs = self[self.index.isin(NonEmptyObs.index)]

        for i in range(SelectedObs.shape[0]):
                MonitoringWell_ID = SelectedObs.monitoring_well.iloc[i]
                TimeSeries = hdp.GroundwaterObs.from_bro(MonitoringWell_ID, int(SelectedObs.tube_nr.iloc[i]))
                LocatiePeilbuis = [TimeSeries.monitoring_well] * len(TimeSeries)
                FilternummerTimeSeries = [TimeSeries.tube_nr] * len(TimeSeries)
                PeilDatumTijd = [t.strftime("%d-%m-%Y %H:%M") for t in TimeSeries.index]
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
                        TimeSeriesModule = pd.concat([TimeSeriesModule,TimeSeriesObs])
        
        TimeSeriesModuleCols = TimeSeriesModule.columns.to_list()
        TimeSeriesModuleUnits = ['[String]',
                                 '[Integer]',
                                 '[ExcelDate]',
                                 '[m+ref]',
                                 '[m+ref]']
        TimeSeriesModuleHeader = pd.DataFrame([TimeSeriesModuleCols, TimeSeriesModuleUnits])

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
        StartDatum = [t.strftime("%d-%m-%Y %H:%M") for t in SelectedObs.stats.dates_first_obs.to_list()]
        EindeDatum = [t.strftime("%d-%m-%Y %H:%M") for t in SelectedObs.stats.dates_last_obs.to_list()]
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
                                  '[ExcelDate]',
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
        
        DescriptionModuleHeader = pd.DataFrame([DescriptionModuleCols, DescriptionModuleUnits])

        #### Write CSV file
        with open(f'{dirpath}\BRO2Menyanthes.csv', 'w',newline='') as file:
                file.write(header2.to_csv(index = False, header = False, sep = ';', decimal = ","))
                file.write(";\n")
                file.write(DescriptionModuleHeader.to_csv(index = False, header = False, sep = ';', decimal = ","))
                file.write(DescriptionModule.to_csv(index = False, header = False, sep = ';', decimal = ","))
                file.write(";\n")
                file.write(TimeSeriesModuleHeader.to_csv(index = False, header = False, sep = ';', decimal = ","))
                file.write(TimeSeriesModule.to_csv(index = False, header = False, sep = ';', decimal = ","))

#%%

BRO_Import.to_Menyanthes(dirpath = r"c:\Users\925793\Downloads")


#%% OLD VERSION
Obs_no = BRO_Import.stats.get_no_of_observations()
NonEmptyObs = Obs_no[Obs_no > 0]
SelectedObs = BRO_Import[BRO_Import.index.isin(NonEmptyObs.index)]

for i in range(SelectedObs.shape[0]):
    #Obs_no = SelectedObs.stats.get_no_of_observations()
    #NonEmptyObs = Obs_no[Obs_no > 0]
    #SelectedObs = SelectedObs[SelectedObs.index.isin(NonEmptyObs.index)]
    MonitoringWell_ID = SelectedObs.monitoring_well.iloc[i]
    TimeSeries = hdp.GroundwaterObs.from_bro(MonitoringWell_ID, int(SelectedObs.tube_nr.iloc[i]))
    #print(TimeSeries)
    LocatiePeilbuis = [TimeSeries.monitoring_well] * len(TimeSeries)
    FilternummerTimeSeries = [TimeSeries.tube_nr] * len(TimeSeries)
    PeilDatumTijd = [t.strftime("%d-%m-%Y %H:%M") for t in TimeSeries.index] 
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
        TimeSeriesModule = pd.concat([TimeSeriesModule,TimeSeriesObs])
#%%
TimeSeriesModuleCols = TimeSeriesModule.columns.to_list()
TimeSeriesModuleUnits = ['[String]',
                         '[Integer]',
                         '[ExcelDate]',
                         '[m+ref]',
                         '[m+ref]']
TimeSeriesModuleHeader = pd.DataFrame([TimeSeriesModuleCols, TimeSeriesModuleUnits])
#%% Series description
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
StartDatum = [t.strftime("%d-%m-%Y %H:%M") for t in SelectedObs.stats.dates_first_obs.to_list()]
EindeDatum = [t.strftime("%d-%m-%Y %H:%M") for t in SelectedObs.stats.dates_last_obs.to_list()]
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

DescriptionModule = pd.DataFrame(DescriptionZipped, columns=['Name',
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
                          '[ExcelDate]',
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
DescriptionModuleHeader = pd.DataFrame([DescriptionModuleCols, DescriptionModuleUnits])
#%%
with open(r'C:\Users\925793\Downloads\test.csv', 'w',newline='') as file:
        file.write(header2.to_csv(index = False, header = False, sep = ';', decimal = ","))
        file.write(";\n")
        file.write(DescriptionModuleHeader.to_csv(index = False, header = False, sep = ';', decimal = ","))
        file.write(DescriptionModule.to_csv(index = False, header = False, sep = ';', decimal = ","))
        file.write(";\n")
        file.write(TimeSeriesModuleHeader.to_csv(index = False, header = False, sep = ';', decimal = ","))
        file.write(TimeSeriesModule.to_csv(index = False, header = False, sep = ';', decimal = ","))

