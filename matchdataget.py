# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 14:57:57 2020

@author: Simon

Set of routines for the Profixio scraper.
"""
import re
import ast
import os
import datetime as dt
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# load configuration data
from config import season, base, spec, SVBK, t, p, mIDfname

def bs_preprocess(html):
     """remove distracting whitespaces and newline characters"""
     pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
     html = re.sub(pat, '', html)       # remove leading and trailing whitespaces
     html = re.sub('\n', ' ', html)     # convert newlines to spaces
                                        # this preserves newline delimiters
     html = re.sub('[\s]+<', '<', html) # remove whitespaces before opening tags
     html = re.sub('>[\s]+', '>', html) # remove whitespaces after closing tags
     return html 
 
def get_mID(match):
    data = match.get('onclick').strip('matchdetails')
    data = re.sub("[()'\s']","",data)
    return data.split(',')[-1]

def get_url(svbfID, sID, mID=None):
    """generate specific url"""
    loc = spec+'t='+t+svbfID+'&k=LS'+sID+'&p='+p
    if mID:
        loc = loc+'&m='+mID    
    return urljoin(base,loc)

def get_mlist_profixio(svbfID, sID, mID=None):
    """download and preprocess url data"""
    # build url
    url = get_url(svbfID,sID,mID)
    # get data from web page
    f = requests.get(url)
    html = bs_preprocess(f.text)
    soup = BeautifulSoup(html, 'html.parser')
    # get all matches
    return soup.find_all("tr", class_=["odd", "even"], onclick=True)
    
def get_mIDdict(SVBK,readmID):    
    """
    generate dictionary of match IDs 
    either by reading from file or by scraping
    the overview pages on profixio for each team
    """
    if readmID:
        if not os.path.isfile(mIDfname):
            raise(OSError('Cannot find file '+mIDfname))
        print('Reading mIDs from file.')
        with open(mIDfname, 'r') as f:
            contents = f.read()
            mIDdict = ast.literal_eval(contents)
    else:        
        mIDdict = {}
        for team in SVBK:
            mIDdict[team] = find_match(team)
        with open(mIDfname,'w') as f:
            f.write(str(mIDdict))
            
    for team in SVBK:
        for mID in mIDdict[team]:
            SVBK[team].addMatch(mID)
    return mIDdict

def find_match(team):
    """
    scrape overview page on Profixio 
    to get list of all match IDs for a 
    given team
    """
    mIDlist = []
    svbfID = SVBK[team].data['SVBF ID']
    sID    = SVBK[team].data['Series ID']
    mlist = get_mlist_profixio(svbfID, sID)
    
    for match in mlist:
        mID = get_mID(match)
        mIDlist.append(mID)
    return mIDlist

def get_mdata(mID,matchdata):
    """
    scrape full data for a specific match 
    specified by a unique mID
    """
    svbfID = SVBK[matchdata[mID]['Team Name']].data['SVBF ID']
    sID    = SVBK[matchdata[mID]['Team Name']].data['Series ID']
    v      = SVBK[matchdata[mID]['Team Name']].data['Tournament Type']
    # get data
    mlist = get_mlist_profixio(svbfID,sID,mID)
    # find correct match and get data
    match = None
    for m in mlist:
        # clean "onclick" data
        if get_mID(m) == '0':
            match = m
            break
    if match:
        # extract info
        return mparser(match,v,matchdata[mID])
    else:
        print(matchdata[mID])
        return False

def mparser(match,v,mdata):
    """
    parse raw html data
    """
    data = [ tag.string for tag in match.children ]
    # get date
    if v == '0': # standard setup
        date = data.pop(0)
        # translate date format
        wd,dm = date.split(' ',1)
        dd,mm = [ int(x) for x in dm.split('/',1) ]
        if mm>6:
            yy = season
        else:
            yy = season+1
            
    elif v == '1':    
        date_pattern = '\w{3} \d{2}/\d{2}'
        p = re.compile(date_pattern)
        datedata = None
        for sib in match.previous_siblings:
            string = sib.get_text()
            if p.match(string):
                datedata = string.split()
                wd,dm,yy = datedata
                dd,mm = [ int(x) for x in dm.split('/',1) ]
                yy = int(yy)
                break
        if not datedata:
            print(*data)
            print(*[ mdata[key] for key in mdata.keys() ], sep='\n')
            raise(RuntimeError,'Cannot find match date.')
    else:
        raise(ValueError,'Unknown setup type.')
    
    # get rest of data
    if len(data) == 7 or len(data) == 8:
        time, mdata['Home'], mdata['Guest'] = [ data[i] for i in [0,1,3] ]
        mdata['Result'], mdata['Sets'] = [ None, None ]
    elif len(data) == 9 or len(data) == 10:
        time, mdata['Home'], mdata['Guest'], mdata['Result'], mdata['Sets'] = [ data[i] for i in [0,1,3,7,8] ]
    else:
        print('\nError when parsing time:\n\tdata: ', ' ,'.join(data))
        return None
    # parse time and date and get timestamp
    if time:
        H,M = [ int(x) for x in time.split(':',1) ]
    else:
        H,M = [ 0, 0 ]
    if dd == 0:
        print('Illegal date format: ',date,' - setting illegal value to 1.')
        dd = 1
    if mm == 0:
        print('Illegal date format: ',date,' - setting day to 1.')
        mm = 1
    timestamp = dt.datetime(yy,mm,dd,H,M)
    mdata['Date'] = timestamp;
    mdata['Week #'] = timestamp.isocalendar()[1]
    
    # Matchdata
    nsib = list(match.next_sibling.children)
    data = nsib[1].get_text('|').split('|')
    
    for (i,fld) in enumerate(data):
        if i!=len(data):
            if fld=='Arrangör':
                mdata['Arranger'] = data[i+1]
            elif fld=='Spelplats':
                mdata['Location'] = data[i+1]
            elif fld=='1Domare':
                mdata['Referee 1'] = data[i+1]
            elif fld=='2Domare':
                mdata['Referee 2'] = data[i+1]
    
    return True

def print_summary(mIDlist):
    """
    visualisation of match summary data
    """
    print('Season %i/%i:' % (season,season+1))
    count = 0
    for team in SVBK.keys():
        nmatch = len(mIDlist[team])
        print("  %-10s: %3i" % (team,nmatch))
        count += nmatch
    print('------------------')
    print('  %-10s: %3i\n' % ('Total',count))
        
def print_mdata(i,mID,matchdata):
    """
    visualisation of specific match data
    """
    mdata = matchdata[mID]
    if mdata['Result']:
        print('\t%3i: %s | %s | %15s - %-15s | Arr: %-15s Loc: %-15s | %s' 
          % (i+1,mID,mdata['Date'].strftime('%y/%m/%d %H:%M'),
             mdata['Home'],mdata['Guest'],mdata['Arranger'],mdata['Location'][0:14],mdata['Result']))
    else:
        print('\t%3i: %s | %s | %15s - %-15s | Arr: %-15s Loc: %-15s' 
          % (i+1,mID,mdata['Date'].strftime('%y/%m/%d %H:%M'),
             mdata['Home'],mdata['Guest'],mdata['Arranger'],mdata['Location'][0:14]))