import json
from logsFile import Logs
from typing import *
import traceback


class AppAttr():
    """AppAttr 
    Class containing all the global variable in the application

    contains the methods : 
    -get
    -config
    -getErrorlevel
    """

    _win_settings = {}
    _widsetlist = []
    _widget_name_list = []
    _project_wid_sets_list = {}
    _cache = []
    _redo_cache = []
    _widsets = None
    _widinfo = None
    _lang_dict = {}
    _saved = True
    _code_list = []
    _code = None
    _lang_choice = None
    _project = None
    _widget = None
    _widget_id = None
    _logs = None

    print("AppAttr loaded")


    @classmethod
    def _initConstAttr(cls):
        """_initConstAttr 
        funtion that initialize the constants of the application

        Returns
        -------
        str, True
            return True if the initialisation is good, else "Error" 
        """
        cls._logs = Logs()
        try : 
            with open("rssDir"+ "\\" +"widgetInfo.json", "r", encoding= 'utf8') as file:
                cls._widinfo = json.load(file)
        except Exception as error:
            error_level = cls._logs.getErrorLevel(type(error).__name__)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)
            return False
        try : 
            with open('rssDir'+ "\\" +'widParaInfo.json', "r", encoding= 'utf8') as file:
                cls._widsets = json.load(file)
        except Exception as error:
            error_level = cls._logs.getErrorLevel(type(error).__name__)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)
            return False
        try :
            with open("rssDir" + "\\" + "languageDict.json", 'r', encoding= 'utf8') as file :
                cls._lang_dict = json.load(file)
        except Exception as error:
            error_level = cls._logs.getErrorLevel(type(error).__name__)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)
            return False
        try :
            with open("rssDir" + "\\" + "wdSettings.json", "r", encoding= 'utf8') as file :
                cls._win_settings = json.load(file)
        except Exception as error:
            error_level = cls._logs.getErrorLevel(type(error).__name__)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)
            return False
        return True


    @classmethod
    def get(cls, attr):
        """get 
        fonction that gives the values of the defined attributes

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
            -language        : language chose
            -langdict        : dictionnary of the different languages
            -code_list       : list containing each line of the code
            -code            : code as it is in it's file
            -cache           : gives the current cache
            -redo_cache      : gives the current redo cache

        Returns
        -------
        _type_
            the data that contains the precised attribute
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
            case "saved" :
                return cls._saved
            case "language" :
                return cls._lang_choice
            case "langdict" :
                return cls._lang_dict
            case "code_list" :
                return cls._code_list
            case "code" :
                return cls._code
            case "cache" :
                return cls._cache
            case "redo_cache" :
                return cls._redo_cache


    @classmethod
    def config(cls, attr : str, val : enumerate[int, str, list, dict, bool] = None):
        """config 
        fucntion that modifies the values of a given attribute

        Parameters
        ----------
        attr : str
            attribute to modify
            -project         : opened project name
            -widget          : opened widget name
            -widget_id       : opened widget's ID
            -widsets         : widget's parameters list
            -widinfo         : widget main info
            -settings        : window settings
            -widsetlist      : settings of the opened widget
            -widnamelist     : list of the existing widgets in the project
            -prjtwidsetslist : list of the widsets
            -language        : language chose
            -langdict        : dictionnary of the different languages
            -code_list       : list containing each line of the code
            -code            : code as it is in it's file
            -cache           : cache of the programm
            -cache           : redo cache of the programm
            
        val : enumerate[int, str, list, dict, bool], optional
            new value of the attribute, by default None
        """
        match attr :
            case "project":
                cls._project = val
                cls._logs.addToLogs("new project", val)
            case "widget" :
                cls._widget = val
                cls._logs.addToLogs("actual widget opened", val)
            case "widget_id" :
                cls._widget_id = val
                cls._logs.addToLogs("actual widget's ID", val)
            case "settings" :
                cls._win_settings = val
                cls._logs.addToLogs("window settings", val)
            case "widsetlist" :
                cls._widsetlist = val
                cls._logs.addToLogs("widget settings list", val)
            case "widnamelist" :
                cls._widget_name_list = val
                cls._logs.addToLogs("widget name list", val)
            case "prjtwidsetslist" :
                cls._project_wid_sets_list = val
            case "saved" :
                if cls._saved != val and val == True :
                    cls._logs.addToLogs("modification saved", val)
                    cls._logs.addToLogs("widget settings list's dictionnary saved", cls._project_wid_sets_list)
                    cls._logs.addToLogs("code list saved", cls._code, True)
                cls._saved = val
            case "language" :
                cls._lang_choice = val
                cls._logs.addToLogs("language used", val)
            case "code_list" :
                cls._code_list = val
                cls._code = "".join(cls._code_list)
            case "cache" :
                cls._logs.addToLogs("actual cache", cls._cache)
            case "closelogs" :
                cls._logs.save()
            case "const" :
                return cls._initConstAttr()
            case "redo_cache" :
                cls._logs.addToLogs("actual redo cache", cls._redo_cache)

    @classmethod
    def getErrorlevel(cls, err):
        return cls._logs.getErrorLevel(type(err).__name__)