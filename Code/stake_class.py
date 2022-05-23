#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:49:02 2021

@author: cmarkovsky
"""

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#%% Stake Class

class Stake:

    
    def __init__(self, directory, stake_folder, filename):
        row_names = ['lat', 'long', 'elevation', 'date', 'length_exposed', 'length_in_ice', 'surface_lowering', 'stake_length', \
                    'status', 'surface_type', 'debris_depth', 'debris_property', 'snow_depth', 'snow_density', \
                     'snow_dens_source', 'ice_density', 'ice_dens_source', 'mass_balance', 'comments', 'investigator']
        file_path = directory + stake_folder + '/' + filename
        stake_df_full = pd.read_csv(file_path, skiprows=3, names = row_names)
        self.df_full = stake_df_full
        self.build_stake_df(stake_df_full)
        
#         stake_dict = self.build_stake_dicts(stake_file)
#         self.dict = stake_dict
    
    def build_stake_df(self, full_df):
        index = 'date'
        parameters = ['date','surface_lowering', 'debris_depth', 'elevation', 'surface_type']
        df = pd.DataFrame()
        
        for param in parameters:
            df[param] = full_df[param]
        dates = df['date']
        new_dates = []
        for m in range(len(dates)):
            cur_date = dates[m]
            new_date = self.datechange(cur_date)
            new_dates.append(new_date)
        df['date'] = new_dates
        self.df = df
        try:
            avg_lat = np.nanmean(full_df['lat'])
            avg_long = np.nanmean(full_df['long'])
        except:
            next
        self.coords = (avg_lat, avg_long)

#     def build_stake_dict(self, stake):
#         stake_dict={}
#         stake_dict['dates']=stake['date']
#         stake_dict['surface_melt']=stake['surface_lowering']
#         stake_dict['debris_depth']=stake['debris_depth']
#         stake_dict['elevation']=stake['elevation']
#         stake_dict['surface_type']=stake['surface_type'][0]
#         dates=stake_dict['dates']
# #         print(stake_dict['elevation'])
#         new_dates=[]
#         for m in range(len(dates)):
#             cur_date = dates[m]
# #             cur_date = dates[m].split(' ')[0]
# #             cur_date = cur_date.replace('-','/')
#             new_date = self.datechange(cur_date)
#             new_dates.append(new_date)
#         df['date']=new_dates
        

    def datechange(self, date_str):
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return(dt)

    def days_between(self, date1, date2):
        delta=abs(date2-date1)
        return(delta.days)

    def get_melt(self):
        melt = self.df['surface_lowering']
        dates = self.df['date']
        debris = self.df['debris_depth']
        elevation = self.df['elevation']
        
        day_melt_list = [0] #(#Days, Melt)
        total_melt_list = [0]
        melt_dates = [dates[0]]
        debris_list = [debris[0]]
        elevation_list = [elevation[0]]
        for m in (range(dates.size-1)):
            day1 = dates.iloc[m]
            day2 = dates.iloc[m+1]
            num_days = self.days_between(day1, day2)
            if (not num_days < 9):
                cur_melt = melt.iloc[m+1]
                try:
                    melt.iloc[m+1] = float(melt.iloc[m+1])
                except:
                    melt.iloc[m+1] = float(melt.iloc[m+1].replace('>',''))

                melt_per_day = melt.iloc[m+1] / num_days
                
                melt_dates.append(dates.iloc[m+1])
                day_melt_list.append(melt_per_day)
                total_melt_list.append(melt.iloc[m+1]) 
                debris_list.append(float(debris.iloc[m+1]))
                elevation_list.append(elevation.iloc[m+1])
        melt_df = pd.DataFrame({'melt_dates': melt_dates, 'melt_per_day': day_melt_list, 'total_melt_list': \
                                total_melt_list, 'debris_depth': debris_list, 'elevation': elevation_list})
        return melt_df
    


#     def elevation(self):
#         ele_list=self.stake_dict['Ele']
#         ele=0
#         # print(ele_list)
#         for item in ele_list:
#             if item > 0:
#                 ele=item
#                 return(ele)
#             else:
#                 ele=-1
#         self.ele=ele 
        
#         return(ele)

#     def temp_adj(self, AWS_year):
#         ele=self.elevation()
        
#         if AWS_year == 2021:
#             standard = 541
#         else:
#             standard = 585.8

#         fact=-6.5*(ele-standard)/1000
#         return fact
    
#     def dates(self):
#         info=self.csv()
#         return info['Date']

#     def plotmvd(self, dates, melts):
#         fig=plt.figure()
#         ax=fig.gca()
#         ax.grid()
#         plt.plot(dates, melts)
#         ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
#         plt.ylabel('Melt Rate (cm/day)')
        
#     def melt_sum(self):
#         total_melt=sum(self.totalmelt)
#         return total_melt
    
#     def getname(self):
#         filename=self.filename
#         name=filename[filename.index("/")+1:filename.index(".")]
#         self.name=name
#         return name
    
#     def if_ice(self):
#         if self.stake_dict['Surface'] == 'Ice':
#             return True
#         else:
#             return False
        
    
    
        
    
