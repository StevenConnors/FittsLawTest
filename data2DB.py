import sqlite3 as sql
import os
import numpy as np
import matplotlib.pylab as plt
import Tkinter, tkFileDialog
import dataReader as dR
import dataOps as dO

def tableCheck(database,outputTable):
    tables=listTables(database)
    if outputTable in tables:
        print('%s tables exists, do you want to drop it? yes/no'%(outputTable))
        input=raw_input()
        if 'y' in input.lower():
            dropTable(database,outputTable)
            return True
        else:
            print('change the name of the %s table'%(outputTable))
            return False

def errorRateTable(databaseName,dataTable,outputTable):
    conn=sql.connect(databaseName)
    c=conn.cursor()
    
    if not(tableCheck(databaseName,outputTable)):
        return False
        
    
    query='''
    create table %s as select 1.0*sum(clicked)/count(clicked),
    participant,device,condition,trial from %s 
    where target!=0 
    group by participant,condition,trial,device
    '''%(outputTable,dataTable)
    c.execute(query)
    conn.commit()
    conn.close()

    


def meansTable(databaseName,outliersTable,dataTable,outputTable):
    conn=sql.connect(databaseName)
    c=conn.cursor()
    
    if not(tableCheck(databaseName,outputTable)):
        return -1
    
    query='''
    create table %s as select avg(elapsedTime) as avg_elapsed,
    participant,condition,trial,device from %s 
    where rowid not in(select * from %s) and target!= 0 and clicked!=1 
    group by participant,condition,trial,device
    '''%(outputTable,dataTable,outliersTable)
    c.execute(query)
    conn.commit()
    conn.close()


def writeOutliersTable(database,outputTable,data):
    conn=sql.connect(database)
    c=conn.cursor()
    tables=listTables(database)
    if outputTable in tables:
        print('outliers tables exists, do you want to drop it? yes/no')
        input=raw_input()
        if 'y' in input.lower():
            dropTable(database,outputTable)
        else:
            print('change the name of the outlier table')
            return -1
        
    c.execute('create table %s (rows integer)'%(outputTable))
    conn.commit()
    c=conn.cursor()
    for rowId in data:
        c.execute('insert into %s values(%d)'%(outputTable,rowId))
    conn.commit()
    conn.close()
    
    
def outlierDetection(database,inputTable,columns2pick,observations,outputTable,excludeQuery=None):
    '''
    This function finds from the specified database and table the outliers
    In order to do that it creates blocks from the specified columns in 
    columns2pick. The observations are a numerical column from which the outliers
    will be calculated.
    columns2pick : list of strings with the names of the columns to be used
    to build the blocks
    observations : column from which the outliers will be calculated
    outputTable : Table in which the results will be stored
    excludeQuery : If some of the data should be excluded from the query
                    simply add it to this variable. It will be appended at the end of any query
                    done by the code to the database ideally it should be of the form
                    "variable!=something"
    '''
    
    
    outlierRows=[]
    temp=''
    for column in columns2pick:
        temp+=column+','
    columns=temp
    columns=columns[:-1]
    
    
    conn=sql.connect(database)
    c=conn.cursor()
    
    #First I need to extract the information
    #to build the different blocks
    blocks=[]
    blocksSize=[]
    for col in columns2pick:
        c.execute('select distinct %s from %s'%(col,inputTable))
        temp=[]
        for i in c:
            temp.append(i[0])
        blocks.append(temp)
        blocksSize.append(len(temp))
        
    
        
    indxs=np.indices(tuple(blocksSize)).reshape(len(blocksSize),-1).T
    
    for i in range(len(indxs)):
        
        #Section where the data from a single trial is selected
        rowsIdxs=''
        for i2 in range(len(indxs[i])):
            if isinstance(blocks[i2][indxs[i][i2]],str) or isinstance(blocks[i2][indxs[i][i2]],unicode):
                rowsIdxs+=str(columns2pick[i2])+'='+'"'+str(blocks[i2][indxs[i][i2]])+'"'
            else:
                rowsIdxs+=str(columns2pick[i2])+'='+str(blocks[i2][indxs[i][i2]])
            if not(i2==len(indxs[i])-1):
                rowsIdxs+=' and '
    
        query="select rowid,%s from %s where %s;"%(observations,inputTable,rowsIdxs)
        
        if excludeQuery!=None:
            query=query[:-1]
            if 'where' in excludeQuery:
                ind=excludeQuery.find('where')
                excludeQuery=excludeQuery[ind+5:]
            query+=' and '+excludeQuery+';'
        c.execute(query)
        
        empty=False
        
        try:
            tempData=[[tempInd[0],tempInd[1]] for tempInd in c]
        except:
            empty=True
            print('error')
        else:
            if tempData==[]:
                empty=True
                
            
            
        if not(empty):            
            data=[tempInd[1] for tempInd in tempData]
            rowid=[tempInd[0] for tempInd in tempData]
            q1=np.percentile(data,25)
            q3=np.percentile(data,75)
            iqr=q3-q1
            lb=q1-iqr*1.5
            ub=q3+iqr*1.5
            std=np.std(data)
            mu=np.mean(data)
            
            for tempInd in range(len(data)):
#                 if data[tempInd]<=lb or data[tempInd]>=ub:
#                 if data[tempInd]>=ub:
                if data[tempInd]>=std*3+mu:
                    outlierRows.append(rowid[tempInd])
        else:
            print('warning : empty result for query')
            print(query)
    conn.close()
    writeOutliersTable(database,outputTable,outlierRows)
    

def dropTable(filename,tablename):
    conn=sql.connect(filename)
    c=conn.cursor()
    c.execute("drop table %s"%(tablename))
    conn.commit()
    conn.close()
    
def queryExecute(filename,tablename,query):
    conn=sql.connect(filename)
    c=conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    

def listTables(filename):
    conn=sql.connect(filename)
    c=conn.cursor()
    c.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
    tablesList=[]
    for i in c:
        tablesList.append(str(i[0]))
    conn.commit()
    conn.close()
    return tablesList
    

def createDatabase(filename,tablename):
    conn=sql.connect(filename)
    c=conn.cursor()
    c.execute('''create table %s (
                participant integer,
                trial integer,
                condition text,
                device text,
                target integer,
                absTime real,
                elapsedTime real,
                targetX real,
                targetY real,
                clickX integer,
                clickY integer,
                clicked integer,
                keyPressed text,
                width integer,
                distance integer,
                errorMargin real,
                homingTime real,
                keybHomingTime real,
                typingTime real,
                word text,
                path text
                 ) '''%(tablename))
#     c.execute("insert into stocks values('2006-01-05','buy','rhat',100,35.14)")
    conn.commit()
    conn.close()
    
    

def insertDirectory(filename,tablename):
    '''
    openDirectory(filename,tablename)
    This function reads all the files on a folder and put them in a database
    the database will be created if it does not exist
    filename : The name of the database
    tablename : The name of the table to be created     
    '''
    if os.path.isfile(filename):
        print('database exists')
        tables=listTables(filename)
        if tablename in tables:
            print('table exists, do you want to overwrite it?')
            inp=raw_input()
            if 'y' in inp.lower():
                dropTable(filename,tablename)
                print('table erased')
                createDatabase(filename,tablename)
                print('table created')
            else:
                print('change the name of the table to be created')
                return False
        else:
            print('table does not exist, creating')
            createDatabase(filename,tablename)
            
    else:
        print('database does not exist, creating')
        createDatabase(filename,tablename)
        
        
    conn=sql.connect(filename)
    c=conn.cursor()
        
    root = Tkinter.Tk()
    allFiles=[]
    
    filesPath=tkFileDialog.askdirectory()

    
    
    if filesPath:
        for root, dirs, files in os.walk(filesPath):
            for file in files:
                if file.endswith(".dat"):
                    tempFilename=os.path.join(root, file)
                    allFiles.append(tempFilename)
                    temp=dO.alphaNumExtract(file)
                    
                    userT=temp[1]
                    deviceT=temp[2]
                    trialT=temp[3]
                    difficultyT=temp[4].split('.')[0][-1]
                    
                    inFile=dR.csvReader(tempFilename, delimiter=',', headerLines=3)
                    
                    temp=inFile['header']
                    header=temp[2]
                    userF=dO.alphaNumExtract(temp[0][0])[1]
                    deviceF=dO.alphaNumExtract(temp[0][0])[2]
                    trialF=dO.alphaNumExtract(temp[0][0])[3]
                    difficultyF=temp[0][1]
                    
                    #Error check
                    error=0
                    if not(userF==userT):
                        print('users do not correspond for file')
                        print(tempFilename)
                    if not(deviceF==deviceT):
                        print('devices do not correspond for file')
                        print(tempFilename)
                    if not(trialF==trialT):
                        print('trial number does not correspond for file')
                        print(tempFilename)
                    if not(difficultyF==difficultyT):
                        print('difficulties does not match for file')
                        print(tempFilename)
                        
                        
                    previousTime=-1
                    tempData={}
                    for row in inFile['data']:
                        
                        for ind in range(len(row)):
                            tempData[header[ind].strip()]=row[ind]
                        
                        absTime=float(tempData['time'])
                        if previousTime!=-1:
                            elapsedTime=absTime-previousTime
                        else:
                            elapsedTime=absTime

                        
                        
                        previousTime=absTime

                        #After all the data has been confirmed we can now write to the database
                        query='''insert into %s values (
                        %s,%s,"%s","%s",%s,%s,
                        %s,%s,%s,%s,%s,
                        %s,"%s",%s,%s,%s,
                        %s,%s,%s,"%s","%s"
                        );
                        '''%(tablename,
                             userF,
                             trialF,
                             difficultyF,
                             deviceF,
                             tempData['Target#'],
                             str(absTime),
                             str(elapsedTime),
                             tempData['targetX'],
                             tempData['targetY'],
                             tempData['clickX'],
                             tempData['clickY'],
                             tempData['clicked'],
                             tempData['keyPressed'],
                             tempData['width'],
                             tempData['distance'],
                             tempData['errorMargin'],
                             tempData['Homing Time1'],
                             tempData['Keyboard Homingtime'],
                             tempData['Typingtime'],
                             tempData['Word'],
                             tempFilename                             
                             )
                        c.execute(query)
                        conn.commit()
                    print(tempFilename)
                     
                     #Now here add the part where I take the file and
                     #input it to the database 
                     #Remember to feed to the database the elapsed time
                     #as opposed to the current absolute time or maybe both
    conn.close()
    
    
    
if __name__=='__main__':
    databaseName='/Users/julian/Dropbox/fingers/fingers.db'

    excludeQuery='where target!= 0 and clicked!=1'
    
    
    
    #The next function reads all of the data 
    #from a directory and puts it into a database
    datatable='relative_vs_absolute' 
#     insertDirectory(databaseName,datatable)
    
    
    outputTable='outliers_sd'
    columns2pick=['participant','trial','condition','device']
    observations='elapsedTime'
    
    outlierDetection(databaseName,datatable,columns2pick,observations,outputTable,excludeQuery)
    
    
    outliersTable='outliers_sd'
    dataTable='relative_vs_absolute'
    outputTable='meansTableSD'
    
    
    meansTable(databaseName,outliersTable,dataTable,outputTable)
    
    #The next table does not take into account outliers only missclicks
    outputTable='errorRate'
    errorRateTable(databaseName,dataTable,outputTable)
    
    
    
    
    print('done')
    

    
    #Currently the code creates tables, and database if necessary, also asks
    #if the table already exists, the only part left then is to actually insert
    #the data into the database
    #This code should work as well for the next pilot studies
    #in addition the outlier detection code also filters out using a custom query
    
#     
    

    