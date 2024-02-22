import json

class AppAttr():

    _win_settings = {}
    _widsetlist = []
    _widget_name_list = []
    _project_wid_sets_list = []
    _widsets = None
    _widinfo = None
    _lang_dict = None
    
    _project = None
    _widget = None
    _widget_id = None

    print("AppAttr loaded")


    @classmethod
    def _initConstAttr(cls):
        try : 
            with open("rssDir"+ "\\" +"widgetInfo.json", "r", encoding= 'utf8') as file:
                cls._widinfo = json.load(file)
        except :
            return "Error"
        try : 
            with open('rssDir'+ "\\" +'widParaInfo.json', "r", encoding= 'utf8') as file:
                cls._widsets = json.load(file)
        except :
            return "Error"
        try :
            with open("rssDir" + "\\" + "languageDict.json", 'r', encoding= 'utf8') as file :
                cls._lang_dict = json.load(file)
        except :
            return "Error"
        try :
            with open("rssDir" + "\\" + "wdSettings.json", "r", encoding= 'utf8') as file :
                cls._win_settings = json.load(file)
        except :
            return "Error"


    @classmethod
    def get(cls, attr):
        """get _summary_

        Parameters
        ----------
        attr : _type_
            -project         : opened project name
            -widget          : opened widget name
            -widget_id       : opened widget's ID
            -widsets         : widget's parameters list
            -widinfo         : widget main info
            -settings        : window settings
            -widsetlist      : settings of the opened widget
            -widnamelist     : list of the existing widgets in the project
            -prjtwidsetslist : list of the widsets

        Returns
        -------
        _type_
            _description_
        """
        match attr :
            case "project":
                return cls._project
            case "widget" :
                return cls._widget
            case "widget_id" :
                return cls._widget_id
            case "widsets" :
                return cls._widsets
            case "widinfo":
                return cls._widinfo
            case "settings" :
                return cls._win_settings
            case "widsetlist" :
                return cls._widsetlist
            case "widnamelist" :
                return cls._widget_name_list
            case "prjtwidsetslist" :
                return cls._project_wid_sets_list


    @classmethod
    def config(cls, attr, val = None):
        match attr :
            case "project":
                cls._project = val
            case "widget" :
                cls._widget = val
            case "widget_id" :
                cls._widget_id = val
            case "settings" :
                cls._win_settings = val
            case "widsetlist" :
                cls._widsetlist = val
            case "widnamelist" :
                cls._widget_name_list = val
            case "prjtwidsetslist" :
                cls._project_wid_sets_list = val
            case "const" :
                cls._initConstAttr()
            