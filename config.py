# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 17:03:28 2020

@author: Simon

Configuration file for Profixio scraper
"""
from teamclass import Team

update  = True          # scrape data (True) or read old data from file
readmID = True          # read match IDs from file (True) or scrape from Profixio
season  = 2021          # First year of the season of interest

# dictionary keys for the match data
mkeys = [ 'Date','Division','Name','Series ID','Team Name','SolnaTeamID',
             'Arranger','Location','Home','Guest',
             'Result','Sets','Referee 1','Referee 2','Week #' ]
# url specifiers
base = "https://www.profixio.com/fx/"
spec = "serieoppsett.php?"
t = "SVBF_SERIE_AVD"
p = "1"

# path to match ID list
mIDfname = 'mIDlist.txt'

""" 
Dictionary of all the teams registered in SolnaVBK for a given season including their unique identifiers on Profixio.
This must be filled out manually based on the data from Profixio.
!!! Data for teams not listed here will not be downloaded !!!
"""

# Nomenclature
# SVBK[#name] = (#division,#divisionName,#SVBF_ID,#Series_ID,#Team_ID,#Type)
# sample url: https://www.profixio.com/fx/serieoppsett.php?t=SVBF_SERIE_AVD13033_X&k=LS13033&p=1
#             https://www.profixio.com/fx/serieoppsett.php?t=SVBF_SERIE_AVD #SVBF_ID &k=LS #Series_ID &p=1
SVBK = {}
# Season 2021/2022: 
SVBK['Damer A']  = Team(season, "Div 1","Norra Damer",          "12979",  "12979","15488352","0") # Division 1 - Norra Damer           - Damer A
SVBK['Herrar A'] = Team(season, "Div 1","Norra Herrar",         "12975",  "12975","15487976","0") # Division 1 - Norra Herrar          - Herrar A
SVBK['Damer B']  = Team(season, "Div 2","Östra Damer",          "13033_X","13033","15488532","1") # Division 2 - Östra Damer           - Damer B
SVBK['Damer C']  = Team(season, "Div 2","Mellersta Östra Damer","13034",  "13034","15487731","1") # Division 2 - Mellersta Östra Damer - Damer C
SVBK['Herrar B'] = Team(season, "Div 2","Östra Herrar",         "13039",  "13039","15487565","1") # Division 2 - Östra Herrar          - Herrar B
SVBK['Damer D']  = Team(season, "Div 3","Östra Damer",          "13052",  "13052","15488754","1") # Division 3 - Östra Damer           - Damer D
SVBK['Herrar C'] = Team(season, "Div 3","Östra Herrar",         "13058",  "13058","15501201","1") # Division 3 - Östra Herrar
SVBK['Herrar D'] = Team(season, "Div 3","Östra Herrar",         "13058",  "13058","15489432","1") # Division 3 - Östra Herrar         - Herrar C

# SVBK 2020/2021:
# SVBK['Damer A']  = Team(2020, "Div 1","Norra Damer",          "11952","11952","15461634","0")
# SVBK['Herrar A'] = Team(2020, "Div 1","Norra Herrar",         "11961","11961","15461610","0")
# SVBK['Damer B']  = Team(2020, "Div 2","Mellersta Östra Damer","11969","11969","15461662","1")
# SVBK['Herrar B'] = Team(2020, "Div 2","Östra Herrar",         "11971","11971","15461653","0")
# SVBK['Damer C']  = Team(2020, "Div 3","Östra Damer",          "12016","12016","15461759","1")
# SVBK['Damer D']  = Team(2020, "Div 3","Östra Damer",          "12016","12016","15461760","1")
# SVBK['Herrar C'] = Team(2020, "Div 3","Östra Herrar",         "12035","12035","15462818","1")
