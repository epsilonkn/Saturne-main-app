#fichier gérant les interactions avec les fichiers de sauvegarde
from fileOpening import *
from appattr import AppAttr
from codeGen import CodeGeneration


class FileModification():


    @staticmethod
    def modifyPrjtInfo(newinfo : dict):
        get_path = FileOperation.createPath(AppAttr.get("project")) +"\\"+ 'prjtset.json'
        ProjectOperation.mPS(get_path, newinfo)


    @staticmethod
    def cNWSF():
        """cNWSF : Create New Widget Settings File

        Parameters
        ----------
        widget : _type_
            _description_
        project : _type_
            _description_

        Returns
        -------
        _type_
            _description_
        """
        sets = AppAttr.get( "widinfo")
        sets = sets[AppAttr.get( "widget_id")]
        flag = False
        incr = 1
        while flag == False :
            if AppAttr.get( "widget_id") + str(incr) not in AppAttr.get("widnamelist") :
                flag = True
                newname = AppAttr.get( "widget_id") + str(incr)
            else : incr += 1
        id_card_dict = {}
        id_card_dict["name"] = newname
        id_card_dict["ID"] = AppAttr.get( "widget_id")
        id_card_dict["master"] = "window"
        id_card_dict["slaves"] = 0
        id_card_dict["layout"] = id_card_dict["initcode"] = id_card_dict["layoutcode"] = None
        
        code = CodeGeneration.createWidCode([{}, {}, {}, id_card_dict])
        id_card_dict["initcode"] = code[0]
        id_card_dict["layoutcode"] = code[1]
        
        AppAttr.config( "widget", newname)
        AppAttr.config(AppAttr.get( "widget_id"), [{}, {}, {}, id_card_dict])
        data = AppAttr.get("prjtwidsetslist")
        data[newname] = [{}, {}, {}, id_card_dict]
        AppAttr.config("prjtwidsetslist", data)