#fichier gérant les interactions entre l'interface et les fichiers fonctionnels
import fileOpening as fileop
import fileManagemt as flmngt
from codeGen import CodeGeneration
from typing import *


def newPrjctRqst(name : str) -> None: 
    """newPrjctRequest 
    fonction de transition entre le programme de l'interface et le programme de gestions des fichiers
    envoie une requête de création d'un dossier pour un nouveau projet

    Parameters
    ----------
    name : str
        nom du dossier à créer
    """
    fileop.dirCreation(name)


def rmproject() -> None:
    """rmproject 
    Envoie une requête de suppression d'un dossier

    Parameters
    ----------
    name : str
        nom du fichier
    """
    fileop.rmDirectory()


def modidyPrjctRqst(name : str, dico : dict) -> None:
    """modidyPrjctRqst 
    Envoie une requête de modification des paramètres d'un projet

    Parameters
    ----------
    name : str
        nom du projet
    dico : dict
        dictionnaire des paramètres du projet
    """
    path = fileop.createPath(name)
    old_data = fileop.loadInfo(path)
    path = fileop.createPath(name + "\\" + "code.py")
    code = CodeGeneration.mWinCode(CodeGeneration, old_data, dico, path)
    fileop.wCode(name, code)
    flmngt.modifyPrjtInfo(name, dico)


def renameDirReq(oldname : str, newname : str) -> bool:
    return fileop.renameDir(oldname, newname)


def getPrjtSetRqst(name : str) -> dict:
    """getPrjtSetRqst 
    Envoie une requête d'obtention des paramètres d'un projet

    Parameters
    ----------
    name : str
        nom du projet

    Returns
    -------
    dict
        paramètres du projet ciblé
    """
    path = fileop.createPath(name)
    return fileop.loadInfo(path = path)


def getMainWidSetsRqst() -> dict:
    """getMainWidSetsRqst 
    Envoie une requête d'obtention des données par défaut d'un widget

    Returns
    -------
    dict
        paramètres du widget ciblé
    """
    return fileop.loadInfo(data = "widsets")


def getSetsInfoRqst() -> dict:
    """getSetsInfoRqst 
    Envoie une requête d'obtention des données des paramètres présent dans tkinter

    Returns
    -------
    dict
        dictionnaire des données de chaque paramètre dans tkinter
    """
    return fileop.loadInfo(data = 'setsinfo')


def verifyFilesRqst()-> list:
    """verifyFilesRqst 
    Envoie une requête de vérification de l'intégrité de l'application

    Returns
    -------
    list
        renvoie le nom du fichier ou du projet altéré, et son type (file ou project)
        si il n'y a pas d'erreur, l'élément 0 de la liste est True
    """
    path = fileop.createPath("rssDir")
    with open(path + "\\" + "prjctNameSave.txt", 'r') as file :
        prjts = file.read()
        prjts.split(",")
    file.close()
    for projects in prjts :
        print(projects)
        if not  fileop.verifyDir(fileop.createPath(projects)) :
            return [projects, 'project']
    return [fileop.verifyApp(), 'file']


def getWidNameListReq(project : str) -> list:
    """getWidNameListReq 
    Envoie une requête d'obtention de la liste des widgets d'un projet

    Parameters
    ----------
    project : str
        nom du projet ciblé

    Returns
    -------
    list
        liste contenant le nom de chaque widget du projet
    """
    path = fileop.createPath(project)
    print(path)
    return fileop.loadInfo(path, data = "widNameList")


def getWidSetReq(widname : str, project : str) -> dict:
    """getWidSetReq 
    Envoie une requête d'obtention des paramètres d'un widget créé par l'utilisateur

    Parameters
    ----------
    widname : str
        nom du widget
    project : str
        nom du projet parent du widget

    Returns
    -------
    dict
        dictionnaire composé des paramètres du widget
    """
    path = fileop.createPath(project + "\\" + widname + ".json")
    return fileop.loadInfo(path, "actualwidSet")


def createWidSetFileReq(newwidget : str) -> str:
    """createWidSetFileReq 
    Envoie une requête de création d'un fichier pour un widget

    Parameters
    ----------
    newwidget : str
        nom du nouveau widget
    project : str
        nom du projet parent du widget

    Returns
    -------
    str
        retourne le nouveau nom du widget
    """
    flmngt.cNWSF(newwidget)


def modifyWidSetReq(widget : str, widname : str, dico : list, project : str) -> None:
    """modifyWidSetReq 
    Envoie une requête de modification des paramètres d'un widget créé par l'utilisateur

    Parameters
    ----------
    widget : str
        identifiant du widget ( label, button etc)
    widname : str
        nom du widget ( donné par l'utilisateur/ par le programme)
    dico : list
        dictionnaire des paramètres du widget
    project : str
        nom du projet parent du widget
    """
    path = fileop.createPath(project+ "\\" + widname + ".json")
    old_data = fileop.loadInfo(path, data = "actualwidSet")
    path = fileop.createPath(project + "\\" + "code.py")
    code = CodeGeneration.mWidCode(CodeGeneration, old_data, dico, path)
    fileop.wCode(project, code)
    flmngt.uWS(widget,widname, dico, project)


def delWidReq(widget : str, wid_id,  project : str) -> None:
    """delWidReq 
    Envoie une requête de suppression des données d'un widget

    Parameters
    ----------
    widget : str
        nom du widget
    project : str
        nom du projet parent du widget
    """
    path = fileop.createPath(project+ "\\" + widget + ".json")
    old_data = fileop.loadInfo(path, data = "actualwidSet")
    path = fileop.createPath(project + "\\" + "code.py")
    code = CodeGeneration.delWidCode(CodeGeneration, widget, wid_id, path)
    fileop.wCode(project, code)
    fileop.rmWid(widget, project)


def getCodeReq(project):
    path = fileop.createPath(project + "\\" + "code.py")
    return fileop.loadInfo(path, data = "prjtCode")


def tryWN(name : str) -> bool:
    """tryWN 
    Fonction de vérification de la validité d'un nom de widget entré,
    étant donné que ce nom est aussi utilisé comme nom de variable il doit :
    - ne pas contenir de caractères interdits
    - ne par commencer par une majuscule
    Parameters
    ----------
    name : str
        nom de widget à tester

    Returns
    -------
    bool
        renvoie True si le nom est valide, False sinon
    """
    allowedchar = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'
    ]
    for letters in name :
        if letters not in allowedchar :
            return False
    if name[0] in allowedchar[26:-2]:
        return False
    return True


def tryFont(family :str, family_list : str ) -> str :
    #on récupère le
    family = family.capitalize().strip()
    if family + '\n' in family_list :
        return family
    else :
        return False


def getRssPath(rss):
    return fileop.createPath("rssDir" + "\\" + rss)


def getProjectPath(project):
    return fileop.createPath(project)


def prepareExe(project):
    code = fileop.loadInfo(fileop.createPath(project + "\\" + "code.py"), "prjtCodeList")
    code = flmngt.prepForExe(code)
    fileop.wCode(project, code)


def shutdownExe(project):
    code = fileop.loadInfo(fileop.createPath(project + "\\" + "code.py"), "prjtCodeList")
    code = flmngt.sDAE(code)
    fileop.wCode(project, code)


#possibilité de lancer le programme seul, à des fins de débogage
if __name__ == "__main__" :
    name = input("nom : ")
    print(tryWN(name))