#fichier gérant les interactions entre l'interface et les fichiers fonctionnels
from fileOpening import *
from fileManagemt import *
from codeGen import CodeGeneration
from typing import *
from appattr import AppAttr

class ProjectReq():
    """ProjectReq 
    Class which contains the Requests about the projects
    """
    

    @staticmethod
    def newPrjctRqst() -> None: 
        """newPrjctRequest 
        fonction de transition entre le programme de l'interface et le programme de gestions des fichiers
        envoie une requête de création d'un dossier pour un nouveau projet

        Parameters
        ----------
        name : str
            nom du dossier à créer
        """
        ProjectOperation.dirCreation()


    @staticmethod
    def rmproject() -> None:
        """rmproject 
        Envoie une requête de suppression d'un dossier

        Parameters
        ----------
        name : str
            nom du fichier
        """
        ProjectOperation.rmDirectory()


    @staticmethod
    def modidyPrjctRqst(dico : dict) -> None:
        """modidyPrjctRqst 
        Envoie une requête de modification des paramètres d'un projet

        Parameters
        ----------
        name : str
            nom du projet
        dico : dict
            dictionnaire des paramètres du projet
        """
        old_data = AnnexOperation.loadInfo(data = "prjctInfo")
        code = CodeGeneration.mWinCode(old_data, dico)
        ProjectOperation.wCode(code)
        FileModification.modifyPrjtInfo(dico)


    @staticmethod
    def renameDirReq(newname : str) -> bool:
        return ProjectOperation.renameDir(newname)


    @staticmethod
    def getPrjtSetRqst() -> dict:
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
        return AnnexOperation.loadInfo(data = "prjctInfo")


    @staticmethod
    def initProjectAttrReq():
        AppAttr.config("widnamelist", AnnexOperation.loadInfo(data = "widNameList"))
        AnnexOperation.loadInfo(data = "initwidsetlist")


    @staticmethod
    def saveModifReq():
        ProjectOperation.save()


class WidgetReq():
    """WidgetReq 
    Class which contains the requests about the widget 
    """


    @staticmethod
    def getMainWidSetsRqst() -> dict:
        """getMainWidSetsRqst 
        Envoie une requête d'obtention des données par défaut d'un widget

        Returns
        -------
        dict
            paramètres du widget ciblé
        """
        return AnnexOperation.loadInfo(data = "widsets")


    @staticmethod
    def getSetsInfoRqst() -> dict:
        """getSetsInfoRqst 
        Envoie une requête d'obtention des données des paramètres présent dans tkinter

        Returns
        -------
        dict
            dictionnaire des données de chaque paramètre dans tkinter
        """
        return AnnexOperation.loadInfo(data = 'setsinfo')


    @staticmethod
    def getWidSetReq() -> dict:
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
        return AnnexOperation.loadInfo(data = "actualwidSet")


    @staticmethod
    def createWidSetFileReq() -> str:
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
        FileModification.cNWSF()


    @staticmethod
    def modifyWidSetReq() -> None:
        """modifyWidSetReq 
        Envoie une requête de modification des paramètres d'un widget créé par l'utilisateur
        """
        code = CodeGeneration.mWidCode()
        ProjectOperation.wCode(code)


    @staticmethod
    def delWidReq() -> None:
        """delWidReq 
        Envoie une requête de suppression des données d'un widget

        Parameters
        ----------
        widget : str
            nom du widget
        project : str
            nom du projet parent du widget
        """
        code = CodeGeneration.delWidCode(CodeGeneration)
        ProjectOperation.wCode(code)


class CodeReq():
    """CodeReq 
    Class which contains the requests about the code
    """


    @staticmethod
    def prepareExe():
        code = AnnexOperation.loadInfo(data = "prjtCodeList")
        code = FileModification.prepForExe(code)
        ProjectOperation.wCode(code)


    @staticmethod
    def shutdownExe():
        code = AnnexOperation.loadInfo("prjtCodeList")
        code = FileModification.sDAE(code)
        ProjectOperation.wCode(code)


    @staticmethod
    def getCodeReq():
        return AnnexOperation.loadInfo(data = "prjtCode")
    

    @staticmethod
    def getProjectPath():
        return FileOperation.createPath(AppAttr.get("project"))


class ControlReq():
    """ControlReq 
    Class which contains the others requests
    """
    
    _family_path  = FileOperation.createPath("rssDir" + "\\" + "tk_family.txt")
    with open(_family_path, "r", encoding="utf8") as file :
        _tk_family_font = file.readlines()
        for element in _tk_family_font :
                element.replace("\n", "")
        file.close()
    file.close()
    _allowedchar = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_']


    @classmethod
    def tryWN(cls, name : str) -> bool:
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
        for letters in name :
            if letters not in cls._allowedchar :
                return False
        if name[0] in cls._allowedchar[26:-2]:
            return False
        return True


    @classmethod
    def tryFont(cls, family :str) -> str :
        #on récupère le
        family = family.capitalize().strip()
        if family + '\n' in cls._tk_family_font :
            return family
        else :
            return False


    @staticmethod
    def verifyFilesRqst()-> list:
        """verifyFilesRqst 
        Envoie une requête de vérification de l'intégrité de l'application

        Returns
        -------
        list
            renvoie le nom du fichier ou du projet altéré, et son type (file ou project)
            si il n'y a pas d'erreur, l'élément 0 de la liste est True
        """
        path = FileOperation.createPath("rssDir")
        with open(path + "\\" + "prjctNameSave.txt", 'r') as file :
            prjts = file.read()
            prjts.split(",")
        file.close()
        for projects in prjts :
            print(projects)
            if not  FileOperation.verifyDir( path = FileOperation.createPath(projects)) :
                return [projects, 'project']
        return [AnnexOperation.verifyApp(), 'file']

#possibilité de lancer le programme seul, à des fins de débogage
if __name__ == "__main__" :
    name = input("nom : ")
    #print(tryWN(name))