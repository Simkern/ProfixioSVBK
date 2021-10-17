# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 12:05:41 2021

@author: Simon

Data structure to save and summarise match data for Tournaments in the Swedish League (Profixio)
"""

class Team(object):
    def __init__(self,season,div,name,svbfID,sID,tID,v):
        self.season  = season
        self.data    = {}
        klist = ['Division','Name','SVBF ID',
                 'Series ID','SolnaTeamID','Tournament Type']
        for k,val in zip(klist,[div,name,svbfID,sID,tID,v]):
            self.data[k] = val
        self.mIDlist = []
        
    def addMatch(self,mID):
        if mID in self.mIDlist:
            print('mID',mID,'has already been added!')
        else:
            self.mIDlist.append(mID)
            
    def getSummary(self,vrb):
        if vrb:
            print('  General:')
        print('\tDivision: ',self.data['Division'])
        print('\tGroup:    ',self.data['Name'])
        print('\tSeason:   ',self.season,'/',self.season+1)
        print('\tMatches:  ',len(self.mIDlist))
        if len(self.mIDlist) > 0 and vrb:
            print(*self.mIDlist)
            print('  Internals:')
            print('\tSVBFID:   ',self.data['SVBF ID'])
            print('\tseriesID: ',self.data['Series ID'])
            print('\tteamID:   ',self.data['SolnaTeamID'])
            print('\ttournament type:',self.data['Tournament Type'])
        print(' ')