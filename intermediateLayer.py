#fichier gérant les interactions entre l'interface et les fichiers fonctionnels
from fileOpening import *
from fileManagemt import *
from codeGen import CodeGeneration
from typing import *
from appattr import AppAttr
import traceback
from copy import deepcopy


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
        code = AnnexOperation.loadInfo(data = "prjtCodeList")
        AppAttr.config("code_list", code)
        CodeGeneration.mWinCode(old_data, dico["parameters"])
        ProjectOperation.wCode(AppAttr.get("code_list"))
        FileModification.modifyPrjtInfo(dico)


    @staticmethod
    def renameDirReq(newname : str) -> bool:
        var =  ProjectOperation.renameDir(newname)
        if type(var) == bool :
            return var
        else :
            try : 
                raise TypeError
            except Exception as error:
                error_level = AppAttr.getErrorlevel(error)
                with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                    log.write(f"\n An error Occured | level : {error_level}\n")
                    traceback.print_exc(file = log)
                return False 
            



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
        init2 = AnnexOperation.loadInfo(data = "initwidsetlist")
        init3 = AnnexOperation.loadInfo(data = "prjtCodeList")
        AppAttr.config("code_list", init3)
        init1 = AnnexOperation.loadInfo(data = "widNameList")
        AppAttr.config("widnamelist", init1)
        init4 = AnnexOperation.loadInfo("prjctInfo")["gen_indices"]
        print(init4)
        AppAttr.config("indices", init4)
        if init1 == False or init2 == False or init3 == False or init4 == False :
            try :
                raise FileNotFoundError
            except Exception as error:
                error_level = AppAttr.getErrorlevel(error)
                with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                    log.write(f"\n An error Occured | level : {error_level}\n")
                    traceback.print_exc(file = log)
                return False


    @staticmethod
    def saveModifReq():
        ProjectOperation.save()


class WidgetReq():
    """WidgetReq 
    Class which contains the requests about the widget 
    """


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
        cache = ("<add>", AppAttr.get("widget"))
        CacheReq.addToCache(cache)


    @staticmethod
    def modifyWidSetReq() -> None:
        """modifyWidSetReq 
        Envoie une requête de modification des paramètres d'un widget créé par l'utilisateur
        """
        cache = ("<modify>", AppAttr.get("widget")[0], AppAttr.get("widget")[1], AppAttr.get("widsetlist")[::], AppAttr.get("code_list")[::])
        CacheReq.addToCache(cache)
        CodeGeneration.mWidCode()


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
        code = AppAttr.get("code_list")[::]
        CodeGeneration.delWidCode(CodeGeneration)
        cache = ("<delete>", AppAttr.get("widget"), deepcopy(AppAttr.get("prjtwidsetslist")[AppAttr.get("widget")]),
                 AppAttr.get("widnamelist")[::], code)
        CacheReq.addToCache(cache)



class CodeReq():
    """CodeReq 
    Class which contains the requests about the code
    """


    @staticmethod
    def shutdownExe(path):
        FileOperation.rmFiles(path)



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


class CacheReq():


    @staticmethod
    def addToCache(cached):
        cache = AppAttr.get("cache")
        cache.append(cached)
        AppAttr.config("cache")


    @staticmethod
    def undo():
        try :
            cache = AppAttr.get("cache")
            aux_cache = AppAttr.get("redo_cache")
            last_element = cache[-1]
            match last_element[0] :
                case "<add>":
                    widnamelist = AppAttr.get("widnamelist")
                    widsetlist = AppAttr.get("prjtwidsetslist")
                    aux_cache.append(("<RedoAdd>", last_element[1], deepcopy(widnamelist), deepcopy(widsetlist)))
                    del widnamelist[widnamelist.index(last_element[1])]
                    widsetlist = AppAttr.get("prjtwidsetslist")
                    del widsetlist[last_element[1]]
                    del cache[-1]
                    AppAttr.config("cache")
                    AppAttr.config("redo_cache")
                    AppAttr.config("widget", None) if AppAttr.get("widget") == last_element[1] else None
                case "<delete>":
                    aux_cache.append(("<RedoDelete>", last_element[1], deepcopy(AppAttr.get("code_list"))))
                    AppAttr.config("widnamelist", last_element[3])
                    widsetlist = AppAttr.get("prjtwidsetslist") 
                    widsetlist[last_element[1]] = last_element[2]
                    AppAttr.config("code_list", last_element[4])
                    del cache[-1]
                    AppAttr.config("cache")
                    AppAttr.config("redo_cache")
                    AppAttr.config("widget", last_element[1]) if AppAttr.get("widget") == None else None
                case "<modify>":
                    aux_cache.append(("<RedoModify>",last_element[1], last_element[2], AppAttr.get("widsetlist")[::], AppAttr.get("code_list")[::]))
                    widnamelist = AppAttr.get("widnamelist")
                    widnamelist.insert(widnamelist.index(last_element[2]), last_element[1])
                    del widnamelist[widnamelist.index(last_element[2])]
                    widsetlist = AppAttr.get("prjtwidsetslist")
                    del widsetlist[last_element[2]]
                    widsetlist[last_element[1]] = last_element[3]
                    AppAttr.config("code_list", last_element[4])
                    AppAttr.config("widget", last_element[1]) if AppAttr.get("widget") == last_element[2] else None
                    del cache[-1]
                    AppAttr.config("cache")
                    AppAttr.config("redo_cache")
        except Exception as error:
                error_level = AppAttr.getErrorlevel(error)
                with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                    log.write(f"\n An error Occured | level : {error_level}\n")
                    traceback.print_exc(file = log)
                return False
        
    @staticmethod
    def redo():
        try:
            aux_cache = AppAttr.get("redo_cache")
            last_element = aux_cache[-1]
            match last_element[0]:
                case "<RedoAdd>":
                    CacheReq.addToCache(("<add>", last_element[1]))
                    AppAttr.config("widnamelist", last_element[2])
                    AppAttr.config("prjtwidsetslist", last_element[3])
                    AppAttr.config("widget", last_element[1]) if AppAttr.get("widget") == None else None
                    del aux_cache[-1]
                    AppAttr.config("cache")
                    AppAttr.config("redo_cache")
                case "<RedoDelete>":
                    CacheReq.addToCache(("<delete>", last_element[1], deepcopy(AppAttr.get("prjtwidsetslist")[last_element[1]]), 
                                         AppAttr.get("widnamelist")[::], deepcopy(AppAttr.get("code_list"))))
                    widnamelist = AppAttr.get("widnamelist")
                    del widnamelist[widnamelist.index(last_element[1])]
                    widsetlist = AppAttr.get("prjtwidsetslist")
                    del widsetlist[last_element[1]]
                    AppAttr.config("code_list", last_element[2])
                    AppAttr.config("widget", None) if AppAttr.get("widget") == last_element[1] else None
                    del aux_cache[-1]
                    AppAttr.config("cache")
                    AppAttr.config("redo_cache")
                case "<RedoModify>" :
                    CacheReq.addToCache(("<modify>", last_element[1],last_element[2] , deepcopy(AppAttr.get("prjtwidsetslist")[last_element[2]]), 
                                        deepcopy(AppAttr.get("code_list"))))
                    widnamelist = AppAttr.get("widnamelist")
                    widnamelist.insert(widnamelist.index(last_element[1]), last_element[2])
                    del widnamelist[widnamelist.index(last_element[1])]
                    widsetlist = AppAttr.get("prjtwidsetslist")
                    del widsetlist[last_element[1]]
                    widsetlist[last_element[2]] = last_element[3]
                    AppAttr.config("code_list", last_element[4])
                    AppAttr.config("widget", last_element[2]) if AppAttr.get("widget") != last_element[2] else None
                    del aux_cache[-1]
                    AppAttr.config("cache")
                    AppAttr.config("redo_cache")

        except Exception as error:
                error_level = AppAttr.getErrorlevel(error)
                with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                    log.write(f"\n An error Occured | level : {error_level}\n")
                    traceback.print_exc(file = log)
                return False

    @staticmethod
    def resetCache():
        AppAttr.config("cache", [])



#possibilité de lancer le programme seul, à des fins de débogage
if __name__ == "__main__" :
    list = ['import customtkinter\n', '\n', 'window = customtkinter.CTk()\n', '\n', '\n', '\n', '\n', '#variables\n', '\n', '\n', '\n', '#functions\n', '\n', '\n', '\n', '#frames\n', '\n', '\n', '\n', '#widgets\n', '\n']