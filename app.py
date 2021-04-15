"""app.py: web interface based on the flask framework that allows to synchronize 2 folders."""
__author__      = "Corine RAKOTOBE"
__copyright__   = "Projet formation Devops"
__date__ = " Avril 2021"

from flask import *
from function import *
import pandas as pd

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


# synchronization without extension
@app.route('/enterFolder/')
def enterFolder():
    return render_template("activate.html")

@app.route('/enterFolder/activate/', methods=['POST'])
def activateFolder():
    msg_error=''
    # variables globales
    global dossierSrc
    global dossierDest
    global dataFrammeSrc
    global dataFrammeDest
    global dataframmeMod
    global historyActivate
    # initialisation des variables globales
    dossierSrc=""
    dossierDest=""
    dataFrammeSrc=""
    dataFrammeDest=""
    dataframmeMod=""
    historyActivate=[]
    try :       
        dossierSrc=request.form['dossierSrc']
        dossierDest=request.form['dossierDest']
        dataFrammeSrc, dataFrammeDest, dataframmeMod,historyActivate = activate(dossierSrc,dossierDest)
    except (FileNotFoundError):
        msg_error="Les dossiers saisis sont introuvables, veuillez resaisir vos chemins de dossiers valides"
    finally :
        return render_template("activate_details.html",msg_error=msg_error,dossierSrc=dossierSrc,dossierDest=dossierDest,dataFrammeSrc=dataFrammeSrc,dataFrammeDest=dataFrammeDest,dataframmeMod=dataframmeMod,historyActivate=historyActivate)

@app.route('/enterFolder/activate/activate_details/')
def activateDetails():
    return render_template("activate_details.html",dossierSrc=dossierSrc,dossierDest=dossierDest)


@app.route('/enterFolder/activate/detailsSrc/')
def detailsSrc():
    dataFrammeSrc.index.name = None
    return render_template("details_src.html",data=dataFrammeSrc.to_html(),historyActivate=historyActivate)

@app.route('/enterFolder/activate/detailsToDo/')
def detailsToDo():
    dataframmeMod.index.name = None
    return render_template("details_ToDo.html",data=dataframmeMod.to_html(),dataframmeMod=dataframmeMod)


@app.route('/enterFolder/activate/synchronizeFolder/')
def synchronizeFolder():
    dataFrammeDest, historyUpdateDest = synchronize(dossierSrc,dossierDest,dataframmeMod)
    dataFrammeDest.index.name = None
    return render_template("synchronize.html",dataSrc=dataFrammeSrc.to_html(),dataDest=dataFrammeDest.to_html(),historyUpdateDest=historyUpdateDest)



# synchronization with extension
@app.route('/enterFolderExt/')
def enterFolderExt():
    return render_template("activate_ext.html")

@app.route('/enterFolder/activateExt/', methods=['POST'])
def activateFolderExt():
    msg_error=''
    msg_warning=''
    # variables globales
    global dossierSrcExt
    global dossierDestExt
    global extension
    global dataFrammeSrcExt
    global dataFrammeDestExt
    global dataframmeModExt
    global historyActivateExt
    # initialisation des variables globales
    dossierSrcExt=""
    dossierDestExt=""
    extension=""
    dataFrammeSrcExt=""
    dataFrammeDestExt=""
    dataframmeModExt=""
    historyActivateExt=[]
    try :
        dossierSrcExt=request.form['dossierSrc']
        dossierDestExt=request.form['dossierDest']
        extension=request.form['extension']
        if not existFileWithExtInDir(dossierSrcExt,extension):
            msg_warning ="Aucun fichier de type {} n'a été trouvé dans le dossier source --> Synchronisation impossible".format(extension)
        else :
            dataFrammeSrcExt, dataFrammeDestExt, dataframmeModExt,historyActivateExt = activateExt(dossierSrcExt,dossierDestExt,extension)
    except (FileNotFoundError):
        msg_error="Les dossiers saisis sont introuvables, veuiller resaisir vos chemins de dossiers valides"
    finally:
        return render_template("activate_details_ext.html",msg_error=msg_error,msg_warning=msg_warning,dossierSrcExt=dossierSrcExt,dossierDestExt=dossierDestExt,dataFrammeSrcExt=dataFrammeSrcExt,dataFrammeDestExt=dataFrammeDestExt,dataframmeModExt=dataframmeModExt,historyActivateExt=historyActivateExt,extension=extension)

@app.route('/enterFolder/activate/activate_detailsExt/')
def activateDetailsExt():
    return render_template("activate_details_ext.html",dossierSrcExt=dossierSrcExt,dossierDestExt=dossierDestExt,extension=extension)


@app.route('/enterFolder/activate/detailsSrcExt/')
def detailsSrcExt():
    dataFrammeSrcExt.index.name = None
    return render_template("details_src_ext.html",dataExt=dataFrammeSrcExt.to_html(),historyActivateExt=historyActivateExt)

@app.route('/enterFolder/activate/detailsToDoExt/')
def detailsToDoExt():
    dataframmeModExt.index.name = None
    return render_template("details_ToDo_ext.html",dataExt=dataframmeModExt.to_html(),dataframmeModExt=dataframmeModExt)


@app.route('/enterFolder/activate/synchronizeFolderExt/')
def synchronizeFolderExt():
    dataFrammeDestExt, historyUpdateDestExt = synchronize(dossierSrcExt,dossierDestExt,dataframmeModExt)
    dataFrammeDestExt.index.name = None
    return render_template("synchronize_ext.html",dataSrcExt=dataFrammeSrcExt.to_html(),dataDestExt=dataFrammeDestExt.to_html(),historyUpdateDestExt=historyUpdateDestExt,extension=extension)


if __name__=="__main__":
    app.run(port='5000',debug=True)