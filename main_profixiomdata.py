# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 10:17:15 2021

@author: Simon

Main interface for Profixio scraper
"""
import pandas as pd
from datetime import datetime as dt
# read local modules
from matchdataget import get_mdata, get_mIDdict, print_summary, print_mdata
# read configuration file
from config import SVBK, update, readmID, mkeys

print('Update: '+str(update)+'\n')
if not update:
    print('Loading matchdata from file.')
    df_all = pd.read_csv("matchdata_all.csv",index_col=0,parse_dates=True)
else:
    # get or load match IDs
    mIDdict = get_mIDdict(SVBK,readmID)
    # generate matchdata dictionary
    matchdata = {}
    for team in SVBK:
        print('\n',team)
        SVBK[team].getSummary(False)
        for mID in SVBK[team].mIDlist:
            if mID not in matchdata.keys():
                matchdata[mID] = { key: '' for key in mkeys }
                matchdata[mID]['Team Name'] = team
                for key in set.intersection(set(list(SVBK[team].data)),set(mkeys)):
                    matchdata[mID][key] = SVBK[team].data[key]
    # print summary
    print_summary(mIDdict)
                
    print('Fetch data:')
    for team in SVBK:
        print('  %-10s' % team)
        for i, mID in enumerate(SVBK[team].mIDlist):
            status = get_mdata(mID,matchdata)
            if status:
                print_mdata(i,mID,matchdata)
            else:
                print('\t%3i: Could not fetch data.' % (i+1) )

    print('Create dataframes ... ')
    # Create dataframe
    df_all = pd.DataFrame.from_dict(matchdata,orient="index")
    # Add prefix to results to keep Excel from converting to string
    df_all['Result'] = '(' + df_all['Result'].str.replace(" ","") + ')'
    df_home = df_all[df_all['Arranger'].str.contains('Solna')]
    df_away = df_all[ (~df_all['Arranger'].str.contains('Solna')) & (df_all['Guest'].str.contains('Solna'))]
    df_SVBK = df_all[ (     df_all['Home'].str.contains('Solna')) | (df_all['Guest'].str.contains('Solna'))]
    
    print('Slice data and save ... ')
    # Slice dataframe and output
    descr = 'matchdata_'
    today = dt.today().strftime("%Y%m%d_")
    ext = '.csv'
    df_all.to_csv(today+descr+'all'+ext,index = True, header = True, date_format='%Y-%m-%d %a %H:%M',encoding='utf-8-sig')
    df_home.to_csv(today+descr+'home'+ext,index = True, header = True, date_format='%Y-%m-%d %a %H:%M',encoding='utf-8-sig')
    df_away.to_csv(today+descr+'away'+ext,index = True, header = True, date_format='%Y-%m-%d %a %H:%M',encoding='utf-8-sig')
    df_SVBK.to_csv(today+descr+'SVBK'+ext,index = True, header = True, date_format='%Y-%m-%d %a %H:%M',encoding='utf-8-sig')