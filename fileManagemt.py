#fichier gérant les interactions avec les fichiers de sauvegarde
from fileOpening import *
from appattr import AppAttr


class FileModification():


    @staticmethod
    def modifyPrjtInfo(newinfo : dict):
        get_path = FileOperation.createPath(AppAttr.get("project")) +"\\"+ 'prjtset.json'
        ProjectOperation.mPS(get_path, newinfo)


    @staticmethod
    def cNWSF(widget):
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
        sets = sets[widget]
        path = FileOperation.createPath(AppAttr.get( "project"))
        flag = False
        incr = 1
        while flag == False :
            if widget + str(incr) not in AppAttr.get("widnamelist") :
                flag = True
                newname = widget + str(incr)
            else : incr += 1
        dico = {}
        dico["name"] = newname
        dico["ID"] = widget
        dico["layout"] = None
        for values in sets["parameters"]:
            dico [values] = AppAttr.get( "widsets")[values][0]
        WidgetFileOperation.cWSF(path, newname, [dico, {}, {}])
        AppAttr.config( "widget", newname)


    @staticmethod
    def uWS() -> None:
        """uWS : Update Widget Settings

        Parameters
        ----------
        wid : str
            _description_
        dico : dict
            _description_
        """
        datasets = {}
        datasets["name"] = AppAttr.get( "widsetlist")[0]["name"]
        datasets["ID"] = AppAttr.get( "widsetlist")[0]["ID"]
        datasets["layout"] = AppAttr.get( "widsetlist")[0]["layout"]
        sets = AppAttr.get( "widinfo")
        sets = sets[AppAttr.get("widget_id")]
        setvalues = AppAttr.get( "widsets")
        for settings in sets["parameters"] :
            if settings in AppAttr.get( "widsetlist")[0] :
                datasets[settings] = AppAttr.get( "widsetlist")[0][settings]
            else :
                datasets[settings] = setvalues[settings][0]
        AppAttr.config("widsetlist", [datasets, AppAttr.get( "widsetlist")[1], AppAttr.get( "widsetlist")[2]])
        path = FileOperation.createPath(AppAttr.get("project"))
        FileOperation.rmFile(path + "\\" + AppAttr.get("widget") + '.json')
        WidgetFileOperation.mWS(path)


    @staticmethod
    def prepForExe(code):
        code.append("\nwindow.mainloop()")
        return code


    @staticmethod
    def sDAE(code):
        del code[-1]
        del code[-1]
        return code