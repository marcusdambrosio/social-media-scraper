import pandas as pd
import os 
import sys
import datetime as dt

def combine_data(fi):
    master = pd.DataFrame()
    for file in os.listdir('DATA'):
        if type(fi) != str:
            for name in fi:
                if name in file:
                    currData = pd.read_csv(os.path.join('DATA', file))
                    master = pd.concat([master, currData], join='outer')
            fi = fi[-1]
        else:
            if fi in file:
                currData = pd.read_csv(os.path.join('DATA', file))
                master = pd.concat([master, currData], join = 'outer')

    master.to_csv(f'DATA\{fi}_master.csv', index = False)

def date_col(specFile = None, ret = False):
    '''CREATE A READABLE DATE COLUMN FROM TIMESTAMP'''
    if specFile == None:
        for file in os.listdir('DATA'):
            try:
                tempData = pd.read_csv(os.path.join('DATA', file))
            except:
                continue
            tempData['date'] = [dt.datetime.utcfromtimestamp(c).strftime('%m-%d') for c in tempData['time']]
            tempData.to_csv(f'DATA\{file}', index = False)
    else:
        tempData = pd.read_csv(os.path.join('DATA', specFile[0]))
        tempData['date'] = [dt.datetime.utcfromtimestamp(c).strftime('%m-%d') for c in tempData['time']]
        if ret:
            return tempData
        else:
            tempData.to_csv(f'DATA\{file}', index = False)

def update_post_data(fi, subreddit):
    '''UPDATE REDDIT POST DATA GIVEN A 'NEW' POST CSV FILE IN DIRECTORY'''
    newFile = [c for c in os.listdir('DATA') if fi in c and subreddit in c and 'NEW' in c]
    oldFile = [c for c in os.listdir('DATA') if fi in c and subreddit in c and 'NEW' not in c]

    oldData = pd.read_csv(os.path.join('DATA', oldFile[0]))
    newData = pd.read_csv(os.path.join('DATA', newFile[0]))
    newData = date_col(specFile=newFile, ret = True)

    updated = pd.concat([oldData, newData], join='inner')
    updated.to_csv(f'DATA\{fi}_{subreddit}.csv')
# update_post_data('dogecoin', 'posts')

def organize_graphs(fi):
    '''ORGANIZE ALL GRAPHS INTO RESPECTIVE FOLDERS ;; REALLY ONLY MADE FOR ONE TIME USE BECAUSE I DIDNT WANT TO MOVE MANUALLY'''
    graphFiles = [f for f in os.listdir('GRAPHS') if 'png' in f]
    
    for file in graphFiles:
        if 'language' in file:
            if 'withvol' in file:
                os.rename(os.path.join('GRAPHS', file), os.path.join('GRAPHS\LANGUAGE\WITHVOLUME', file))
            else:
                os.rename(os.path.join('GRAPHS', file), os.path.join('GRAPHS\LANGUAGE', file))
        else:
            if 'withvol' in file:
                os.rename(os.path.join('GRAPHS', file), os.path.join('GRAPHS\FREQUENCY\WITHVOLUME', file))
            else:
                os.rename(os.path.join('GRAPHS', file), os.path.join('GRAPHS\FREQUENCY', file))
    print('Graph organization completed')
# organize_graphs('dogecoin')
