#programme d'ouvertures des dossiers
from typing import *
import os
import json
from appattr import AppAttr


class FileOperation():
    """FileOperation 
    Class wich incorporate the functions dedicated to operations on the files of the app
    """

    @staticmethod
    def _addFiletoDir(cls, path : str) -> None:
        """addFiletoDir 
        fonction d'ajout des fichiers de base à un dossier si ils sont manquant

        Parameters
        ----------
        path : str
            chemin d'accès au dossier
        """
        files = os.listdir(path)
        if "code.py" not in files :
            with open(path +"\\"+  'code.py', "w") as file :
                pass
        if "prjtset.json" not in files :
            with open(path +"\\"+ 'prjtset.json', "w") as file :
                pass
        if "widNmeList.txt" not in files :
            with open(path +"\\"+ 'widNmeList.txt', "w") as file :
                pass

    @staticmethod
    def verifyDir(path : str) -> bool:
        """verifyDir 
        surcharge du la fonction précédente du même nom,
        ici, le paramètre est remplacé par path, dans le cas, ou l'appelant possède le chemin d'accès, et non le nom
        """
        if os.path.exists(path) :
            files = os.listdir(path)
            if "code.py" in files and "prjtset.json" in files and "widNmeList.txt" in files :
                return True
            else :
                FileOperation._addFiletoDir(path)
                return True

    @staticmethod
    def rmFiles(path : str) -> None:
        """rmFiles 
        Fonction de suppression des fichiers présent dans le dossier pointé

        Parameters
        ----------
        path : str
            chemin d'accès à un dossier
        """
        files_list = os.listdir(path)
        for files in files_list :
            try: 
                os.remove(path + "\\" + files)
            except : 
                os.rmdir()

    @staticmethod
    def rmFile(path : str) -> None:
        """rmFile 
        Fonction de suppression d'un fichier

        Parameters
        ----------
        path : str
            chemin d'accès du fichier à supprimer
        """
        os.remove(path)

    @staticmethod
    def createPath(target : str) -> str:
        """createPath 
        crée un chemin d'accès à partir du chemin absolu du programme et du nom du fichier ou du dossier cible

        Parameters
        ----------
        target : str
            fichier ou dossier ciblé

        Returns
        -------
        str
            retourne le chemin d'accès de la cible
        """
        return os.path.join(os.getcwd(), target)


class ProjectOperation():
    """ProjectOperation 
    class which contain the function dedicated to operations on projects files and directories
    """

    @staticmethod
    def dirCreation() -> None:
        """dirCreation 
        fonction de création du dossier associé à un projet, et des fichiers enfants

        Parameters
        ----------
        name : str
            nom du projet, servant de nom au dossier
        """
        path = os.getcwd() +"\\"+ AppAttr.get( "project")
        try :
            os.mkdir(path)
            with open(path +"\\"+ 'prjtset.json', "w") as file :
                pass
            with open(path +"\\"+ 'code.py', "w") as file :
                file.write("import customtkinter\n\nwindow = customtkinter.CTk()\n\n")
            with open(path +"\\"+ 'widNmeList.txt', "w") as file :
                pass
        except OSError as error :
            print("error raised : ", error)

    @staticmethod
    def renameDir(newname : str ) -> bool :
        """renameDir 
        change le nom d'un dossier de projet

        Parameters
        ----------
        oldname : str
            ancien nom du projet
        newname : str
            nouveau nom du projet

        Returns
        -------
        bool
            renvoie True si le renommage est réussi, false sinon
        """
        try :
            os.rename(os.path.join(os.getcwd(), AppAttr.get("project")), os.path.join(os.getcwd(), newname))
            return True
        except any as error :
            print(error)
            return False

    @staticmethod
    def rmDirectory() -> None:
        """rmDirectory 
        fonction de suppression d'un dossier
        supprime d'abord tous les fichiers enfants

        Parameters
        ----------
        name : str
            nom du dossier à supprimer
        """
        path =  os.getcwd() +"\\"+ AppAttr.get( "project")
        FileOperation.rmFiles( path)
        os.rmdir(path)

    @staticmethod
    def mPS(path : str, info : dict) -> None:
        """mPS : modify Project Settings 
        écrase les précédents paramètres du projet ciblé par les nouveaux

        Parameters
        ----------
        path : str
            fichier ciblé
        info : dict
            dictionnaire des paramètres
        """
        with open(path, "w", encoding= 'utf8') as file :
            json.dump(info, file)

    @staticmethod
    def wCode(code):
        """wCode 
        écrase le code d'un projet par le nouveau

        Parameters
        ----------
        project : _type_
            _description_
        code : _type_
            _description_
        """
        path = FileOperation.createPath( AppAttr.get("project") + "\\" + "code.py")
        with open(path, "w", encoding= 'utf8') as file :
            file.writelines(code)
        file.close()


class WidgetFileOperation(): 
    """WidgetFileOperation 
    class which contains the functions dedicated to widgets files operations.
    """


    @staticmethod
    def rmWid() -> None : 
        """rmWid : remove Widget
        Fonction de suppression d'un widget

        Parameters
        ----------
        widget : str
            widget à supprimer
        project : str
            projet parent du widget
        """
        path = FileOperation.createPath( AppAttr.get("project"))
        os.remove(path + "\\" + AppAttr.get("widget") + ".json")
        
        data = AppAttr.get("widnamelist")
        del data[data.index(AppAttr.get("widget"))]
        AppAttr.config("widnamelist", data)
        data = ",".join(data)
        with open(path + "\widNmeList.txt", 'w', encoding= 'utf8') as file :
            file.write(data)     


    @staticmethod
    def cWSF(path : str, name : str, settings : dict) -> None:
        """cWSF : create Widget Settings File
        crée le fichier correspondant au widget créé par l'utilisateur
        modifie la liste des widgets dans le fichier "widNmeList.txt"

        Parameters
        ----------
        path : str
            chemin d'accès au fichier du widget
        name : str
            nom du widget
        settings : dict
            dictionnaire des paramètres du widget
        """
        with open(path + "\\" + name + ".json", "w", encoding= 'utf8') as file :
            json.dump(settings, file)
        with open(path + "\widNmeList.txt", 'a', encoding= 'utf8') as file :
            file.write("," + name)
        

    @staticmethod
    def mWS(path : str) -> None :
        """mWS : modify Widget Settings
        à la manière de la fonction "cWSF", crée un fichier contenant les nouvelles données du widget
        si le nom du widget a été changé, la fonction modifie aussi le nom dans le fichier "widNmeList.txt"

        Parameters
        ----------
        path : str
            chemin d'accès du dossier du projet parent
        newname : str
            nouveau nom du widget
        oldname : str
            ancien nom du widget 
        note : newname et oldname peut être identiques
        settings : dict
            dictionnaires contenant les paramètres du widget
        """
        with open(path + "\\" + AppAttr.get( "widsetlist")[0]["name"] + ".json", "w", encoding= 'utf8') as file :
            json.dump(AppAttr.get( "widsetlist"), file)
        
        if AppAttr.get( "widsetlist")[0]["name"] != AppAttr.get("widget") :
            data = AppAttr.get("widnamelist")
            data.insert(data.index(AppAttr.get("widget")), AppAttr.get( "widsetlist")[0]["name"])
            del data[data.index(AppAttr.get("widget"))]
            AppAttr.config("widnamelist", data)
            data = ','.join(data)
            with open(path + "\widNmeList.txt", 'w', encoding= 'utf8') as file :
                file.write(data)
            

class AnnexOperation():
    """AnnexOperation 
    class which contains the methods of this module that not refer to any of the 3 others classes
    """


    @staticmethod
    def verifyApp() -> Union[str, bool]:
        """verifyApp 
        fonction de vérification que tous les fichiers de l'applications sont présents

        Returns
        -------
        Union[str, bool]
            renvoie True si tous les fichiers sont présents, renvoie le nom du fichier manquant sinon
        """
        path = os.getcwd()
        cfiles = os.listdir(path)
        if 'addWidgetTool.py' not in cfiles :
            return 'addWidgetTool.py'
        if "fileManagemt.py" not in cfiles :
            return "fileManagemt.py"
        if "projectApp.py" not in cfiles :
            return "projectApp.py"
        if "settingsApp.py" not in cfiles :
            return "settingsApp.py"
        if "widgetApp.py" not in cfiles :
            return "widgetApp.py"
        if "tool_tip.py" not in cfiles :
            return "tool_tip.py"
        cfiles =os.listdir(path + "\\" + "rssDir")
        if 'prjctNameSave.txt' not in cfiles :
            return "prjctNameSave.txt"
        if "wdSettings.json" not in cfiles :
            return "wdSettings.json"
        if "widgetInfo.json" not in cfiles :
            return "widgetInfo.json"
        if "widgetRss.json" not in cfiles :
            return "widgetRss.json"
        if "widParaInfo.json" not in cfiles :
            return "widParaInfo.json"
        return True


    def loadInfo(data : str = 'prjctInfo') -> Union[dict, list, None]:
        """loadInfo _summary_
        Fonction de chargement des données des fichiers

        Parameters
        ----------
        path : str, optional
            chemin d'accès au fichier, by default None
        data : str, optional
            précise les données à charger :
            -widsets      : chargement des données relative à un widget précis (widgetInfo.json)
            -setsinfo     : chargement des données relatives aux paramètres des widgets 
            -prjctInfo    : chargement des paramètres du projet selectionné
            -widNameList  : chargement de la liste des widget du projet selectionné
            -actualwidSet : chargement des données d'un widget créé par l'utilisateur
            -prjtCode     : chargement du code du projet 
            -prjtCodeList : chargement du code du projet sous forme de liste

        Returns
        -------
        Union[dict, list, None]
            retourne :
            -widsets      : retourne un dictionnaire si le chargement a réussi, None sinon
            -setsinfo     : retourne un dictionnaire si le chargement a réussi, None sinon
            -prjctInfo    : retourne un dictionnaire si le chargement a réussi, None sinon
            -widNameList  : retourne la liste des widget si le chargement a réussi, une liste vide sinon
            -actualwidSet : retourne un dictionnaire si le chargement a réussi, False sinon
        """
        if data == 'prjctInfo' : 
            path = FileOperation.createPath(AppAttr.get("project"))
            if FileOperation.verifyDir(path = path) :
                try : 
                    with open(path + '\\prjtset.json', "r", encoding= 'utf8' ) as file:
                        return json.load(file)
                except :
                    return None
        if data == "widNameList" :
            try :
                path = FileOperation.createPath(AppAttr.get("project"))
                with open(path + "\\" +"widNmeList.txt", 'r', encoding= 'utf8') as file :
                    widsaved = file.read().split(",")
                file.close()
                return widsaved
            except :
                return []
        if data == "actualwidSet" :
            try :
                path = FileOperation.createPath(AppAttr.get( "project") + "\\" + AppAttr.get("widget") + ".json")
                with open(path, 'r', encoding= 'utf8') as file :
                    return json.load(file)
            except :
                return None
        if data == "prjtCode" :
            try :
                path = FileOperation.createPath(AppAttr.get("project") + "\\" + "code.py")
                with open(path, "r", encoding= 'utf8') as file :
                    return file.read()
            except any as error :
                print(error)
                return None
        if data == "prjtCodeList" :
            try :
                path = FileOperation.createPath(AppAttr.get("project") + "\\" + "code.py")
                with open(path, "r", encoding= 'utf8') as file :
                    return file.readlines()
            except any as error :
                print(error)
                return None
        if data == "initwidsetlist":
            try:
                for element in AppAttr.get("widnamelist"):
                    print(element)
                    if element != "": 
                        path = FileOperation.createPath(AppAttr.get("project")) + "\\" + element + ".json"
                        with open(path, "r", encoding="utf8") as file :
                            data = json.load(file)
                            liste = AppAttr.get("prjtwidsetslist")
                            liste.append(data)
                            AppAttr.config("prjtwidsetslist", liste)
            except any as error :
                print(error)
                return None
           

if __name__ == "__main__" :
    print(AnnexOperation.verifyApp())