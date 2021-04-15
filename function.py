""" Script includes several functions that allow to synchronize 2 folders."""
__author__      = "Corine RAKOTOBE"
__copyright__   = "Projet formation Devops"
__date__ = " Avril 2021"
import os
import time
import glob
import shutil
import pandas as pd


#----- directory functions -----#
def detailsFileDir(pathfileName):
    """ Returns the details(fileName, extension, modificationDate, size) of a 
    file in a folder from the absolute path of the file (pathfileName : str) """
    fileName = os.path.basename(pathfileName)
    extension = os.path.splitext(fileName)[1]
    modificationDate = time.ctime(os.path.getmtime(pathfileName))
    size = os.path.getsize(pathfileName)
    return fileName, extension, modificationDate, size

def getAllFilesInDir(pathDir):
    """ Returns a list of all files in a folder from the absolute path of the 
    folder (pathDir : str) """
    return os.listdir(pathDir) 

def getFilesInDirExt(pathDir,extension):
    """ Returns a list of all files with the extention 'extension' in a folder 
    from the absolute path of the folder """
    listOfAllFilesExt = []
    listOfAllFiles = getAllFilesInDir(pathDir)
    for file in listOfAllFiles:
        if file.endswith(extension):
            listOfAllFilesExt.append(file)
    return listOfAllFilesExt

def existFileInDir(fileToSearch,pathDir):
    """ Tests if a file exists in a folder by using the name of the file 
    to search (fileToSearch : str) and the absolute path of the folder 
    (pathDir : str) as parameters """
    listOfAllFiles = getAllFilesInDir(pathDir)
    result=False
    for file in listOfAllFiles:
        if file == fileToSearch:
            result = True
            break
    return result 

def existFileWithExtInDir(pathDir,extension):
    """ Tests if at least one file with the extension 'extension' exists in a 
    folder by taking as parameters the absolute path (pathDir :str) of the 
    folder and the extension (extension : str) """
    listOfAllFilesExt = getFilesInDirExt(pathDir,extension)
    if not listOfAllFilesExt:
        result = False
    else:
        result = True
    return result 

def existFileInList(fileToSearch,listFiles):
    """ Tests if a file exists in a list of files by taking as parameters the 
    file to search (fileToSearch : str) and a list of files (listFiles : list) """
    result=False
    for file in listFiles:
        if file == fileToSearch:
            result = True
            break
    return result 

def copyFileInDir(pathFileToCopy,pathDir):
    """ Copies a file to a folder by taking as parameters the path of the file
    to copy (pathFileToCopy : str) and the absolute path (pathDir :str) of the
    folder """
    filePath = shutil.copy(pathFileToCopy, pathDir)
    return filePath

def deleteFileInDir(fileToDelete,pathDir):
    """ Detetes a file in a folder by taking as parameters the name of the file
    to delete (fileToDelete : str) and the absolute path (pathDir :str) of the
    folder """
    if existFileInDir(fileToDelete,pathDir):
        os.remove(pathDir + "/" + fileToDelete)
    else: 
        pass
    return 0



#----- dataframme functions -----#
def existFileInPd(fileToSearch,dataFrammePd):
    """ Tests if a file exists in a dataFramme by using the name of the file to
    search(fileToSearch : str) and the dataFramme (dataFrammePd : pd.dataFramme)
    as parameters """
    listOfAllFilesPd = dataFrammePd.index.tolist()
    result = False
    for file in listOfAllFilesPd:
        if file == fileToSearch:
            result =True
            break
        else :
            result =False
    return result

def addFileInPd(pathfileName,dataFrammePd,history):
    """ Adds a line (fileName, extension, modificationDate,size) in a dataFramme
    by using the absolute path of the file (pathfileName : str) and the 
    dataFramme (dataFrammePd : pd.dataFramme) as parameters """
    msg=""
    fileName, extension, modificationDate,size =  detailsFileDir(pathfileName)
    dataFrammePd.loc[fileName]=[extension, modificationDate,size]
    msg = "Le fichier {} est ajouté au Fichier de Controle".format(fileName)
    history.append(msg)
    return dataFrammePd,history

def deleteFileInPd(fileToDelete,dataFrammePd,history):
    """ Deletes a line (fileName, extension, modificationDate,size) in a dataFramme
    by using the name of the file to delete (fileToDelete : str) and the dataFramme
    (dataFrammePd : pd.dataFramme) as parameters """
    msg=""
    if existFileInPd(fileToDelete,dataFrammePd):
        dataFrammePd.drop(fileToDelete,inplace=True)
        msg = "Le fichier {} est supprimé du Fichier de Controle".format(fileToDelete)
        history.append(msg)
    else :
        pass
    return dataFrammePd, history

def detailsFilePd(fileName,dataFrammePd):
    """ Returns a line (fileName, extension, modificationDate,size) in a dataFramme
    by using the name of the file (fileName : str) and the dataFramme 
    (dataFrammePd : pd.dataFramme) as parameters """
    data = dataFrammePd.loc[fileName]
    extension = data.extension
    modificationDate = data.modificationDate
    size = data['size']
    return fileName, extension, modificationDate, size

def isDiferentDateSizeCF(fileName,dataFrammeSrc,dataFrammeDest):
    """ Tests if the same file present in dataFrammeSrc and in dataFrammeDest 
    are different (i.e. either the modification date or the size is different) 
    by using the name of the file (fileName : str), the dataFramme source 
    (dataFrammeSrc : pd.dataFramme) and the dataFramme destination
    (dataFrammeDest : pd.dataFramme)as parameters """
    fileNameSrc, extensionSrc, modificationDateSrc, sizeSrc = detailsFilePd(fileName,dataFrammeSrc) 
    fileNameDest, extensionDest, modificationDateDest, sizeDest = detailsFilePd(fileName,dataFrammeDest) 
    if ((modificationDateSrc != modificationDateDest) or (sizeSrc != sizeDest)):
        return True
    else :
        return False  



#----- Create Controle File functions -----#
def createCFSrc(pathDirSrc,history): #Source
    """ Creates a control file source in the source folder(i.e. a csv file that 
    lists all the files with its details present in the folder) if it doesn't 
    exist by using the absolute path of the folder source (pathDirSrc : str) 
    as parameters """
    msg =""
    dataFrammePd = pd.DataFrame(columns = ['fileName','extension','modificationDate','size'])
    listOfAllFiles = getAllFilesInDir(pathDirSrc)
    if existFileInDir("ControlFS.csv",pathDirSrc):
            pass
    else :
        msg = "Première synchronisation Source: Le fichier 'ControlFS' (Fichier de Controle Source) a été crée"
        history.append(msg)
        dataFrammePd = dataFrammePd.set_index('fileName')   
        for file in listOfAllFiles:
            dataFrammePd, history = addFileInPd(pathDirSrc+"/"+file,dataFrammePd,history)
        dataFrammePd.to_csv(pathDirSrc+"/ControlFS.csv")  
    return dataFrammePd, history

def createCFDest(pathDirDst,history): #destination
    """ Creates a control file destination in the destination folder (i.e. a csv 
    file that lists all the files with its details present in the folder) if it 
    doesn't exist by using the absolute path of the folder destination 
    (pathDirDst : str) as parameters """
    msg=""
    dataFrammeDest = pd.DataFrame(columns = ['fileName','extension','modificationDate','size'])
    dataFrammeDest = dataFrammeDest.set_index('fileName') 
    if existFileInDir("ControlFD.csv",pathDirDst) :
        dataFrammeDest = pd.read_csv(pathDirDst+"/ControlFD.csv") 
        dataFrammeDest = dataFrammeDest.set_index('fileName')
    else : 
        msg = "Première synchronisation Destination: Le fichier 'ControlFD' (Fichier de Controle Destination) a été crée"
        history.append(msg)
        dataFrammeDest.to_csv(pathDirDst+"/ControlFD.csv")      
    return dataFrammeDest, history


#----- Source functions -----#
def isModidfiedFile(fileToTest,pathDir,dataFrammePd,history):
    """ Tests if a file has been modified by comparing the file details with the
    dataframme by using the name of file (fileToTest : str ), the absolute path
    of the folder containing the file (pathDir : str) and the dataFramme 
    (dataFrammePd : pd.dataFramme)as parameters """
    msg=""
    result = False
    data = dataFrammePd.loc[fileToTest]
    modificationDateFile = time.ctime(os.path.getmtime(pathDir+"/"+fileToTest))
    sizeFile = os.path.getsize(pathDir+"/"+fileToTest)
    modificationDatePd = data.modificationDate
    sizePd = data['size']
    if ((modificationDateFile != modificationDatePd) or (sizeFile != sizePd)):
        msg = "Le fichier {} à été modifié dans le dossier Source --> Modification du Fichier de Controle Source (Modification)".format(fileToTest)
        history.append(msg)
        result =  True
    else :
        result =  False  
    return result, history


#--------Update functions Source---#
def dataframmeModification(pathDirSrc,pathDirDest,dataframmeMod):

    """ Returns a dataFramme that lists the changes to be made to the 
    destination folder to perform the synchronization by using the absolute path
    of the folder source (pathDirSrc : str), the absolute path of the folder 
    destination (pathDirDest : str) and the dataFramme 
    (dataframmeMod : pd.dataFramme)as parameters """

    dataFrammeSrc = pd.read_csv(pathDirSrc+"/ControlFS.csv") 
    dataFrammeSrc = dataFrammeSrc.set_index('fileName')
    dataFrammeDest = pd.read_csv(pathDirDest+"/ControlFD.csv") 
    dataFrammeDest = dataFrammeDest.set_index('fileName')
    dataframmeModOut = pd.DataFrame(columns = ['fileName','actions'])
    dataframmeModOut = dataframmeModOut.set_index('fileName')
    listOfAllFiles = getAllFilesInDir(pathDirSrc)
    listOfAllFiles.remove("ControlFS.csv")
    listOfAllFilesMod = dataframmeMod.index.tolist()      
    if dataFrammeDest.empty:
        for file in listOfAllFiles:
            dataframmeModOut.loc[file]=['add']
    else :       
        for file in listOfAllFiles:
            if existFileInList(file,listOfAllFilesMod):
                listOfAllFiles.remove(file)
            else :
                pass
        for file in listOfAllFiles:
            if existFileInPd(file,dataFrammeDest):
                if  isDiferentDateSizeCF(file,dataFrammeSrc,dataFrammeDest):
                    dataframmeMod.loc[file]=['mod']
                else :
                    pass
            else :
                dataframmeMod.loc[file]=['add']
        dataframmeModOut = dataframmeMod
    return dataframmeModOut

def dataframmeModificationExt(pathDirSrc,pathDirDest,extension,dataframmeMod):
    """ Returns a dataFramme that lists the changes to be made to the 
    destination folder to perform the synchronization with extension by using
    the absolute path of the folder source (pathDirSrc : str), the absolute path
    of the folder destination (pathDirDest : str), extension (extension :str ) 
    and the dataFramme (dataframmeMod : pd.dataFramme)as parameters """
    dataFrammeSrc = pd.read_csv(pathDirSrc+"/ControlFS.csv") 
    dataFrammeSrc = dataFrammeSrc.set_index('fileName')
    dataFrammeDest = pd.read_csv(pathDirDest+"/ControlFD.csv") 
    dataFrammeDest = dataFrammeDest.set_index('fileName')
    dataframmeModOut = pd.DataFrame(columns = ['fileName','actions'])
    dataframmeModOut = dataframmeModOut.set_index('fileName')
    if dataFrammeDest.empty:
        listOfAllFilesExt = getFilesInDirExt(pathDirSrc,extension)
        if extension == '.csv':
            listOfAllFilesExt.remove("ControlFS.csv")
        else :
            pass
        for file in listOfAllFilesExt:
            dataframmeModOut.loc[file]=['add']
    else :
        listOfAllFilesMod = dataframmeMod.index.tolist()
        for file in listOfAllFilesMod:
            if not file.endswith(extension):
                dataframmeMod.drop(file,inplace=True)
            else :
                pass
        listOfAllFilesExt = getFilesInDirExt(pathDirSrc,extension)
        
        for file in listOfAllFilesExt:
            if existFileInList(file,listOfAllFilesMod):
                listOfAllFilesExt.remove(file)
            else :
                pass

        for file in listOfAllFilesExt:
            if existFileInPd(file,dataFrammeDest):
                if  isDiferentDateSizeCF(file,dataFrammeSrc,dataFrammeDest):
                    dataframmeMod.loc[file]=['mod']
                else :
                    pass
            else :
                dataframmeMod.loc[file]=['add']
        dataframmeModOut = dataframmeMod
    return dataframmeModOut

def updateDelFileSrc(pathDir,dataFrammePd,history,dataframmeMod):
    """ Updates the source dataframme by deleting the files that have been 
    removed from the source folder by using the absolute path of the folder 
    (pathDir : str) and the dataframme source (dataFrammePd : pd.dataFramme)
    as parameters """
    listOfAllFilesPd = dataFrammePd.index.tolist()
    for file in listOfAllFilesPd:
        if existFileInDir(file,pathDir):
            pass
        else :
            dataframmeMod.loc[file]=['del']
            dataFrammePd, history = deleteFileInPd(file,dataFrammePd,history)
    return dataFrammePd,dataframmeMod, history

def updateAddFileSrc(pathDir,dataFrammePd,history,dataframmeMod): 
    """ Updates the source dataframme by adding the files that have been 
    added from the source folder by using the absolute path of the folder 
    (pathDir : str) and the dataframme source (dataFrammePd : pd.dataFramme) 
    as parameters """
    listOfAllFiles = getAllFilesInDir(pathDir)
    listOfAllFiles.remove("ControlFS.csv")
    for file in listOfAllFiles:
        if existFileInPd(file,dataFrammePd) :
            pass
        else :
            dataframmeMod.loc[file]=['add']
            dataFrammePd ,history = addFileInPd(pathDir+"/"+file,dataFrammePd,history)
    return dataFrammePd, dataframmeMod, history

def updateModFileSrc(pathDir,dataFrammePd,history,dataframmeMod): 
    """ Updates the source dataframme by modifying the files that have been
    modified from the source folder by using the absolute path of the folder 
    (pathDir : str) and the dataframme source (dataFrammePd : pd.dataFramme) 
    as parameters """
    listOfAllFiles = getAllFilesInDir(pathDir)
    listOfAllFiles.remove("ControlFS.csv")
    for file in listOfAllFiles:
        modified, history = isModidfiedFile(file,pathDir,dataFrammePd,history)
        if modified:
            dataframmeMod.loc[file]=['mod']
            dataFrammePd.loc[file, "modificationDate"] = time.ctime(os.path.getmtime(pathDir+"/"+file))
            dataFrammePd.loc[file, "size"] = os.path.getsize(pathDir+"/"+file)
        else :
            pass
    return dataFrammePd,dataframmeMod,history

def updateCFSrc(pathDirSrc,historyUpdateSrc): 
    """ Updates the source dataframme taking into account all the modifications
    of the source file by using the absolute path of the folder source 
    (pathDirSrc : str) as parameters """
    dataframmeMod =  pd.DataFrame(columns = ['fileName','actions'])
    dataframmeMod = dataframmeMod.set_index('fileName')
    dataFrammePd = pd.read_csv(pathDirSrc+"/ControlFS.csv") 
    dataFrammePd = dataFrammePd.set_index('fileName')
    dataFrammePd ,dataframmeMod, historyUpdateSrc = updateDelFileSrc(pathDirSrc,dataFrammePd,historyUpdateSrc,dataframmeMod)
    dataFrammePd ,dataframmeMod, historyUpdateSrc = updateAddFileSrc(pathDirSrc,dataFrammePd,historyUpdateSrc,dataframmeMod)
    dataFrammePd ,dataframmeMod, historyUpdateSrc = updateModFileSrc(pathDirSrc,dataFrammePd,historyUpdateSrc,dataframmeMod)
    dataFrammePd.to_csv(pathDirSrc+"/ControlFS.csv")
    return dataFrammePd, historyUpdateSrc, dataframmeMod



#--------Update functions Destination---#
def updateDelFileDest(pathDest,dataFrammeDest,history,dataframmeMod): 
    """ Updates the destination dataframme and destination folder by deleting the
    files that have been removed from the source folder by using the absolute path
    of the folder destination (pathDest : str),the dataframme destination 
    (dataFrammeDest : pd.dataFramme) and the dataframmeMod 
    (dataframmeMod : pd.dataFramme) as parameters """
    msg=""
    data = dataframmeMod[dataframmeMod['actions'] == 'del']
    print("data :",data)
    listOfFiles = data.index.tolist()
    for file in listOfFiles:
        deleteFileInDir(file,pathDest)
        dataFrammeDest, history = deleteFileInPd(file,dataFrammeDest,history)
        msg = "Le fichier {} à été supprimé dans le dossier Source --> Modification du Dossier Destination et Fichier de Controle Destination (Suppression)".format(file)
        history.append(msg)
    return dataFrammeDest, history

def updateAddFileDest(pathDirSrc,pathDirDst,dataFrammeSrc,dataFrammeDest,history,dataframmeMod):
    """ Updates the destination dataframme and destination folder by adding the 
    files that have been added from the source folder by using the absolute path
    of the folder source (pathDirSrc : str),the absolute path of the folder 
    destination (pathDirDst : str), the dataframme source 
    (dataFrammeSrc : pd.dataFramme), the dataframme destination (dataFrammeDest : pd.dataFramme)  
    and the dataframmeMod (dataframmeMod : pd.dataFramme) as parameters """
    msg=""
    data = dataframmeMod[dataframmeMod['actions'] == 'add']
    listOfFiles = data.index.tolist()
    for file in listOfFiles:
        copyFileInDir(pathDirSrc+"/"+file,pathDirDst)
        dataFrammeDest, history = addFileInPd(pathDirDst+"/"+file,dataFrammeDest,history)
        fileName, extension, modificationDate,size =  detailsFilePd(file,dataFrammeSrc)
        dataFrammeDest.loc[file]=[extension, modificationDate,size]
        msg = "Le fichier {} à été ajouté dans le dossier Destination --> Modification du Fichier de Controle Destination (Ajout)".format(file)
        history.append(msg)
    return dataFrammeDest, history
            
def updateModFileDest(pathDirSrc,pathDirDst,dataFrammeSrc,dataFrammeDest,history,dataframmeMod): 
    """ Updates the destination dataframme and destination folder by modifying
    the files that have been modified from the source folder by using the 
    absolute path of the folder source (pathDirSrc : str),the absolute path of
    the folder destination (pathDirDst : str),the dataframme source 
    (dataFrammeSrc : pd.dataFramme), the dataframme destination (dataFrammeDest : pd.dataFramme)  
    and the dataframmeMod (dataframmeMod : pd.dataFramme) as parameters """
    msg=""
    data = dataframmeMod[dataframmeMod['actions'] == 'mod']
    listOfFiles = data.index.tolist()
    for file in listOfFiles:
        deleteFileInDir(file,pathDirDst)
        copyFileInDir(pathDirSrc+"/"+file,pathDirDst)
        dataSrc = dataFrammeSrc.loc[file]
        dataFrammeDest.loc[file, "modificationDate"] = dataSrc.modificationDate
        dataFrammeDest.loc[file, "size"] = dataSrc["size"]
        msg = "Le fichier {} à été modifié dans le dossier Source --> Modification du Fichier de Controle Destination (Modification)".format(file)
        history.append(msg)
    return dataFrammeDest,history

def updateCFDest(pathDirSrc,pathDirDst,dataframmeMod): 
    """Updates the destination dataframme taking into account all the modifications
    of the source file by using the absolute path of the folder source 
    (pathDirSrc : str), the absolute path of the folder detination 
    (pathDirDst : str) and the dataframmeMod 
    (dataframmeMod : pd.dataFramme) as parameters """
    historyUpdateDest=[]
    dataFrammeSrc = pd.read_csv(pathDirSrc+"/ControlFS.csv") 
    dataFrammeSrc = dataFrammeSrc.set_index('fileName')
    dataFrammeDest = pd.read_csv(pathDirDst+"/ControlFD.csv") 
    dataFrammeDest = dataFrammeDest.set_index('fileName')
    dataFrammeDest,historyUpdateDest = updateDelFileDest(pathDirDst,dataFrammeDest,historyUpdateDest,dataframmeMod)
    dataFrammeDest,historyUpdateDest = updateAddFileDest(pathDirSrc,pathDirDst,dataFrammeSrc,dataFrammeDest,historyUpdateDest,dataframmeMod)
    dataFrammeDest,historyUpdateDest = updateModFileDest(pathDirSrc,pathDirDst,dataFrammeSrc,dataFrammeDest,historyUpdateDest,dataframmeMod)
    dataFrammeDest.to_csv(pathDirDst+"/ControlFD.csv")
    return dataFrammeDest, historyUpdateDest


#----- Sync sans extension ----#
def activate(pathDirSrc,pathDirDest):
    """ Creates the control files (source and destination) if they do not exist
    and prepares the dataframme that lists all the changes to be made to the 
    destination folder for synchronization by using the absolute path of the 
    folder source (pathDirSrc : str)and the absolute path of the folder detination
    (pathDirDest : str) as parameters """
    historyActivate=[]
    dataFrammeSrc , historyActivate = createCFSrc(pathDirSrc,historyActivate)
    dataFrammeDest , historyActivate = createCFDest(pathDirDest,historyActivate)
    dataFrammeSrc, historyActivate, dataframmeMod = updateCFSrc(pathDirSrc,historyActivate)
    dataframmeMod = dataframmeModification(pathDirSrc,pathDirDest,dataframmeMod)    
    return dataFrammeSrc, dataFrammeDest, dataframmeMod,historyActivate

def synchronize(pathDirSrc,pathDirDst,dataframmeMod):
    """Synchronizes the destination folder by updating the destination dataframme
    and the destination folder by using the absolute path of the folder source 
    (pathDirSrc : str) and the absolute path of the folder detination 
    (pathDirDest : str) and the dataframmeMod  (dataframmeMod : pd.dataFramme) 
    as parameters """
    dataFrammeDest, historyUpdateDest = updateCFDest(pathDirSrc,pathDirDst,dataframmeMod)
    return dataFrammeDest, historyUpdateDest


#----- Sync avec extension ----#
def activateExt(pathDirSrc,pathDirDest,extension):
    """ Creates the control files (source and destination) if they do not exist 
    and prepares the dataframme that lists all the changes to be made to the 
    destination folder for synchronization with extension by using the absolute 
    path of the folder source (pathDirSrc : str), the absolute path of the folder
    detination (pathDirDest : str) and the extension (extension : str)
    as parameters """
    historyActivateExt=[]
    dataFrammeSrc , historyActivateExt = createCFSrc(pathDirSrc,historyActivateExt)
    dataFrammeDest , historyActivateExt = createCFDest(pathDirDest,historyActivateExt)
    dataFrammeSrc, historyActivateExt, dataframmeMod = updateCFSrc(pathDirSrc,historyActivateExt)
    dataframmeMod = dataframmeModificationExt(pathDirSrc,pathDirDest,extension,dataframmeMod)
    return dataFrammeSrc, dataFrammeDest, dataframmeMod,historyActivateExt



