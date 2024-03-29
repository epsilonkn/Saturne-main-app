#file version 0.2.0
import tkinter as tk
from tkinter import messagebox
import customtkinter as ct
from intermediateLayer import *
from settingsApp import AppEditing
from widgetApp import WidgetApp
from projectApp import ProjectApp
import subprocess
from appattr import AppAttr
from topLevelWin import *
from helpBox import createHelpBox


class interface(ct.CTk):


    def __init__(self) -> None:
        super().__init__()
        
        self.actual_sets = [] #liste des paramètres utilisés dans l'application
        self.layout_list = [] #liste contenant des paramètres de layout, comprenant pour chacun : leur nom, entrée associée, et valeur par défaut
        self.settings = None # défini si la fenêtre de paramètre est ouverte ou non
        self.widgetapp = None # défini si la fenêtre de widgets est ouverte ou non
        self.project_app = None # défini si la fenêtre des projets est ouverte ou non
        self.app = None
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.getSettings()
        self.createInterface()
        if AppAttr.get("widget") != None :
            self.widgetParametersFrame(AppAttr.get("widget"))
        self.openProjectApp(reason = "new")

        self.bind("<Escape>", self.winState)
        self.bind("<Alt-p>", self.openParameters)
        self.bind("<Control-s>", self.savefile)
        self.bind("<Control-c>", self.copyCode)
        self.bind("<Control-p>", self.openPreview)
        self.bind("<Control-o>", self.openProjectApp)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-a>", self.widgetAdding)
        self.bind("<Control-m>", self.modifyWid)
        self.bind("<Control-w>", self.delWid)


    #-------------------- fonctions de création de la fenêtres --------------------
        

    def createInterface(self) -> None:
        """createInterface
        Fonction de création du corps de l'interface
        """
        try :
            #-------------------- création des frames --------------------
            
            
            self.code_frame = ct.CTkFrame(self, width=self.width*(40/100), height=self.height, border_color = "#000000", border_width= 2)
            self.edit_frame = ct.CTkScrollableFrame(self, width=self.width*(40/100), height=self.height*(90/100))
            self.actionbtframe = ct.CTkFrame(self, height = self.height*(10/100), width = self.width*(60/100))
            self.main_item_frame = ct.CTkScrollableFrame(self, height = self.height*(85/100), width = self.width*(18/100), label_text = AppAttr.get("langdict")["menuwid"][self.language])

            self.code_frame.grid(row =0, rowspan =2, column = 0, ipadx = 15, sticky = "N")
            self.edit_frame.grid(row = 0, column = 1, sticky = "e")
            
            self.main_item_frame.grid(row = 0, column = 2, sticky = "e")
            self.actionbtframe.grid(row = 1,column =1, columnspan = 2 )
            

            #-------------------- création du menu --------------------


            self.menubar = tk.Menu(self)
            self.config(menu=self.menubar)

            self.fichier = tk.Menu(self.menubar, tearoff = False)
            self.application = tk.Menu(self.menubar, tearoff = False)
            self.widget_menu = tk.Menu(self.menubar, tearoff = False)
            self.code_menu = tk.Menu(self.menubar, tearoff = False)
            
            self.fichier.add_command(label = AppAttr.get("langdict")["menufile1"][self.language], command = lambda x = AppAttr.get("project") : self.openProjectApp(reason = x))
            self.fichier.add_command(label = AppAttr.get("langdict")["menufile2"][self.language], command = lambda x = "new" : self.openProjectApp(reason = x))
            self.fichier.add_command(label = AppAttr.get("langdict")["menufile3"][self.language], command= lambda : self.savefile())

            self.application.add_command(label = AppAttr.get("langdict")["menuapp4"][self.language], command = lambda : self.undo())
            self.application.add_command(label = AppAttr.get("langdict")["menuapp5"][self.language], command = lambda : self.redo())
            self.application.add_command(label = AppAttr.get("langdict")["menuapp1"][self.language], command = lambda x = "all" : self.clear(x))
            self.application.add_command(label = AppAttr.get("langdict")["menuapp2"][self.language], command = lambda : self.openParameters())
            self.application.add_command(label = AppAttr.get("langdict")["menuapp3"][self.language], command = lambda : self.on_quit())


            self.widget_menu.add_command(label=AppAttr.get("langdict")["menuwid1"][self.language], command = lambda : self.widgetAdding())
            self.widget_menu.add_command(label=AppAttr.get("langdict")["menuwid2"][self.language], command = lambda : self.delWid())
            self.widget_menu.add_command(label=AppAttr.get("langdict")["menuwid3"][self.language], command = lambda : self.modifyWid())

            self.code_menu.add_command(label=AppAttr.get("langdict")["menucode1"][self.language], command = lambda : self.copyCode())
            self.code_menu.add_command(label=AppAttr.get("langdict")["menucode2"][self.language], command = lambda : self.openPreview())

            self.menubar.add_cascade(label = AppAttr.get("langdict")["menufile"][self.language], menu = self.fichier)
            self.menubar.add_cascade(label = AppAttr.get("langdict")["menuapp"][self.language], menu = self.application)
            self.menubar.add_cascade(label = AppAttr.get("langdict")["menuwid"][self.language], menu = self.widget_menu)
            self.menubar.add_cascade(label = AppAttr.get("langdict")["menucode"][self.language], menu = self.code_menu)
            

            #-------------------- création des widgets et des boutons d'actions --------------------


            self.code_output = ct.CTkTextbox(self.code_frame, width=self.width*(35/100), height=self.height*(96/100)-20, activate_scrollbars=False)
            self.code_scrollbar = ct.CTkScrollbar(self.code_frame, command=self.code_output.yview, height=self.height*(96/100)-20)
            self.code_scrollbar.grid()
            self.code_output.configure(yscrollcommand=self.code_scrollbar.set)

            self.copy_bt = ct.CTkButton(self.code_frame, width= self.width*(10/100), height= self.height*(4/100),
                                        text = AppAttr.get("langdict")["menucode1"][self.language], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, 
                                        command = lambda : self.copyCode())
            self.preview_bt = ct.CTkButton(self.code_frame, width= self.width*(10/100), height= self.height*(4/100),
                                        text = AppAttr.get("langdict")["menucode2"][self.language], font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, 
                                        command = lambda : self.openPreview())


            self.parameter_button = ct.CTkButton(self.actionbtframe, width= self.width*(10/100), height= self.height*(6/100),
                                                text = AppAttr.get("langdict")["menuapp2"][self.language], 
                                                font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.openParameters())

            self.modify_button = ct.CTkButton(self.actionbtframe,  width= self.width*(10/100), height= self.height*(6/100),
                                                text = AppAttr.get("langdict")["menuwid3"][self.language], 
                                                font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.modifyWid())
            self.modify_button.configure(state = "disabled") if AppAttr.get("widget") == None else None

            self.delete_button = ct.CTkButton(self.actionbtframe,  width= self.width*(10/100), height= self.height*(6/100),
                                                text = AppAttr.get("langdict")["menuwid2"][self.language], 
                                                font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.delWid())
            self.delete_button.configure(state = "disabled") if AppAttr.get("widget") == None else None


            self.code_output.grid(column =0, row = 0, pady = 5, padx = 10, columnspan = 2)
            self.code_scrollbar.grid(column = 2, row = 0, padx = 10)

            self.copy_bt.grid(row = 1, column = 1, padx = 10, pady = 5)
            self.preview_bt.grid(row = 1, column = 0, padx = 10, pady = 5)
            
            self.delete_button.place(x = self.width*(5/200), y = self.height*(3/200))
            self.modify_button.place(x = self.width*(35/200), y = self.height*(3/200))
            self.parameter_button.place(x = self.width*(70/200), y = self.height*(3/200))

            self.sideWidgetsUptdating()   
            self.codeFrame() if AppAttr.get("project") != None else None

        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)
            return False
            

    def configActionBt(self) -> None:
        """configActionBt 
        fonction de modification de l'état des boutons de suppression et de sauvegarde des widgets 
        """
        self.modify_button.configure(state = "disabled") if AppAttr.get("widget") == None else self.modify_button.configure(state = "normal")
        self.delete_button.configure(state = "disabled") if AppAttr.get("widget") == None else self.delete_button.configure(state = "normal")


    def sideWidgetsUptdating(self) -> None:
        """sideWidgetsUptdating
        Fonction de création des boutons pour les widgets, sur le coté droit de la fenêtre
        """
        self.clear('itemFrame')
        
        self.add_button = ct.CTkButton(self.main_item_frame, width= self.width*(16/100), height= 40, text = AppAttr.get("langdict")["menuwid1"][self.language],
                                       border_width= 2, border_color = "#FFFFFF",font=ct.CTkFont(size=15, weight="bold"), 
                                       corner_radius= 10, command= lambda : self.widgetAdding())
       
        self.add_button.configure(state = "disabled") if AppAttr.get("project") == None else None
        self.add_button.grid(padx = 5, pady = 5)

        for widgets in AppAttr.get("widnamelist") :
            if widgets != "" :
                w_bt = ct.CTkButton(self.main_item_frame, text = widgets, width= self.width*(16/100), height= self.height*(6/100), 
                                    font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda w_id = widgets : self.widgetParametersFrame(w_id))
                w_bt.grid(padx = 5, pady = 5)
            else : pass


    def widgetParametersFrame(self, widget : str = None)  -> None:
        """widgetParametersFrame 
        fonction de création de la frame de paramètres du widget

        Parameters
        ----------
        widget : str
            widget dont la fonction doit afficher les paramètres, et leur valeurs respectives
        """
        self.clear("sets")
        self.actual_sets = []
        if widget == None :
            return
        AppAttr.config("widget", widget)
        #on configue les boutons d'action pour les rendre actifs
        self.configActionBt()
        #on configure la disposition des paramètres selon la largeur de la fenêtre
        self.column_num = 1 if self.width*(30/100) < 490 else 3
        row = 2
        column = 0
        loading = True
        try :
            #on récupère les données du widget, les données associées à chaque paramètre, et les paramètre par défaut du widget
            AppAttr.config("widsetlist", AppAttr.get("prjtwidsetslist")[AppAttr.get("widget")])
            AppAttr.config("widget_id",AppAttr.get("widsetlist")[3]["ID"])
        except any as error :
            print(error)
            loading = False
            messagebox.showwarning("Fichier introuvable", "Une erreur est survenue lors du chargement des données.")

        if loading == True :
            try :
                #-------------------- création des entrées de modification des paramètres --------------------
                
                self.settings_frame = ct.CTkFrame(self.edit_frame)
                self.settings_frame.grid( row = 1, column = 0, sticky = 'w')

                #on crée le label titre, ainsi que l'entrée permettant de renseigner le nom du widget
                self.overal_lbl = ct.CTkLabel(self.edit_frame, text = AppAttr.get("widsetlist")[3]["name"],font=ct.CTkFont(size=25, weight="bold"))

                widnamelbl = ct.CTkLabel(self.settings_frame, text = "Nom du widget :",font=ct.CTkFont(size=15, weight="bold"))
                self.widname = ct.CTkEntry(self.settings_frame, width= 150, height = 40,font=ct.CTkFont(weight="bold"))
                createHelpBox(widget = widnamelbl, parameter = "name", preview = False)
                self.widname.insert(0, AppAttr.get("widsetlist")[3]["name"])

                self.overal_lbl.grid(column = 0, row = 0 , pady = 15, sticky = 'w')
                widnamelbl.grid(row = 1, column = 0, columnspan = 2 if self.column_num == 3 else 1, 
                                     pady = 20, sticky = 'e')
                self.widname.grid(row = 1, column = 2 if self.column_num == 3 else 1, 
                                  columnspan = 2 if self.column_num == 3 else 1 , padx = 10, pady = 20)
                
                detail_dico = {"Simple" : (0,1), "Normal" : (1,2), "Complet" : (1,2,3)}
                
                #on crée le reste des paramètres, selon le type ( soit une entrée texte, un menu, ou un switch)
                self.fontvar = ct.StringVar(value = "0")
                for parameter in AppAttr.get("widinfo")[AppAttr.get("widget_id")]["parameters"]:
                    if AppAttr.get("widsets")[parameter][1] in detail_dico[self.detail_lvl] :
                        lbl = ct.CTkLabel(self.settings_frame, text = parameter + " :", font=ct.CTkFont(size=12, weight="bold"))
                        if parameter in ("master", "onvalue", "offvalue", "textvariable", "variable", "command") or AppAttr.get("widget_id") == "frame": 
                            createHelpBox(widget = lbl, parameter = parameter, preview = False)
                        else : createHelpBox(widget = lbl, parameter = parameter, preview = True)
                        
                        if parameter in ["font", "hover", "image", "dropdown_font"]:
                            entry = ct.CTkSwitch(self.settings_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
                            if parameter in AppAttr.get("widsetlist")[0].keys() :
                                entry.select() if AppAttr.get("widsetlist")[0][parameter] == '1'  else None
                            if parameter == "font" : 
                                try : self.fontvar= ct.StringVar(value = AppAttr.get("widsetlist")[0][parameter])
                                except : self.fontvar = ct.StringVar(value = "0")
                                entry.configure(command = lambda : self.showFontFrame(), variable = self.fontvar)
                            elif parameter == "image" :
                                entry.configure(state = "disabled")
                            elif parameter == "hover" :
                                try : entry.select() if AppAttr.get("widsetlist")[0][parameter] == "True" else None
                                except : entry.select()
                            elif parameter == "dropdown_font" :
                                entry.configure(state = "disabled")
                            
                        elif parameter == "master" :
                            entry = ct.CTkEntry(self.settings_frame, width = 100,font=ct.CTkFont(weight="bold"))
                            entry.insert(0, AppAttr.get("widsetlist")[3]["master"])

                        elif parameter in ["state", "anchor", "compound", "justify"]:
                            entry = ct.CTkOptionMenu(self.settings_frame, values = AppAttr.get("widsets")[parameter][3])  
                            if parameter in AppAttr.get("widsetlist")[0].keys():
                                entry.set(AppAttr.get("widsetlist")[0][parameter])
                            else :   
                                entry.set(AppAttr.get("widsets")[parameter][0])
                        
                        elif parameter == "text":
                            entry = ct.CTkButton(self.settings_frame, text =  AppAttr.get("langdict")["add_label"][self.language], 
                                                 command = lambda : self.openTextTopLevel())
                            try : self.text = AppAttr.get("widsetlist")[0]["text"]
                            except : self.text = ""
                        
                        elif parameter == "values" :
                            entry = ct.CTkButton(self.settings_frame, text = AppAttr.get("langdict")["add_label"][self.language], 
                                                 command = lambda : self.openValuesTopLevel())
                            try : self.values = AppAttr.get("widsetlist")[0]["values"]
                            except : self.values = []

                        elif parameter == "command" :
                            entry = ct.CTkButton(self.settings_frame, text = AppAttr.get("langdict")["add_label"][self.language], 
                                                 command = lambda : self.openCommandTopLevel())
                            try : self.command = AppAttr.get("widsetlist")[0]["command"]
                            except : self.command = ["", {}]
                        
                        elif parameter == "variable" :
                            entry = ct.CTkButton(self.settings_frame, text = AppAttr.get("langdict")["add_label"][self.language], 
                                                 command = lambda x = parameter : self.openVariableTopLevel(x))
                            try : self.variable = AppAttr.get("widsetlist")[0]["variable"]
                            except : self.variable = ""

                        elif parameter == "textvariable" :
                            entry = ct.CTkButton(self.settings_frame, text = AppAttr.get("langdict")["add_label"][self.language], 
                                                 command = lambda x = parameter : self.openVariableTopLevel(x))
                            try : self.textvariable = AppAttr.get("widsetlist")[0]["textvariable"]
                            except : self.textvariable = ""

                        elif parameter in ["width", "height"] :
                            entry = ct.CTkEntry(self.settings_frame, width = 100,font=ct.CTkFont(weight="bold"))
                            if parameter not in AppAttr.get("widsetlist")[0].keys() :
                                entry.insert(0, "Default")
                            else :
                                entry.insert(0, AppAttr.get("widsetlist")[0][parameter])

                        else :
                            entry = ct.CTkEntry(self.settings_frame, width = 100,font=ct.CTkFont(weight="bold"))
                            if parameter in AppAttr.get("widsetlist")[0].keys():
                                entry.insert(0, AppAttr.get("widsetlist")[0][parameter])
                            else : 
                                entry.insert(0, AppAttr.get("widsets")[parameter][0])
                        self.actual_sets.append((entry, parameter))
                        
                        lbl.grid(row = row, column = column, padx = 5, pady = 10, sticky = 'n')
                        column = column + 1 if column < self.column_num else 0
                        row += 1 if column == 0 else 0
                        
                        entry.grid(row = row, column = column, padx = 5, pady = 10, sticky = 'n')
                        column = column + 1 if column < self.column_num else 0
                        row += 1 if column == 0 else 0

                self.layoutlbl = ct.CTkLabel(self.settings_frame, 
                                             text = "affichage du widget : ", font=ct.CTkFont(size=15, weight="bold") )
                self.layout = ct.CTkSegmentedButton(self.settings_frame, 
                                                    font=ct.CTkFont(size=15, weight="bold"), values = ["pack", "grid"], 
                                                     command = self.showLayoutFrame)
                self.layout.set(AppAttr.get("widsetlist")[3]["layout"]) if AppAttr.get("widsetlist")[3]["layout"] != None else None
                self.layoutlbl.grid(row = row +1, column = 0)
                self.layout.grid(row = row+1, column = 1)
                
                try : self.showFontFrame() if self.fontvar.get() == "1" else None
                except : pass
                
                try : self.showLayoutFrame(self.layout.get()) if self.layout.get() != "" else None
                except : pass

            except Exception as error:
                error_level = AppAttr.getErrorlevel(error)
                with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                    log.write(f"\n An error Occured | level : {error_level}\n")
                    traceback.print_exc(file = log)
                messagebox.showwarning("Erreur de chargement", "Une erreur est survenue lors de l'affichage des données")


    def codeFrame(self):
        #permet d'afficher le code de l'interface
        self.txt_code = AppAttr.get("code")
        if self.txt_code == None :
            messagebox.showerror("Erreur d'affichage", "Une erreur est survenue lors de l'affichage du code.")
            self.code_output.delete("0.0", "end")
            return
        self.code_output.delete("0.0", "end")
        self.code_output.insert("0.0", self.txt_code)


    def showFontFrame(self):
        """showFontFrame 
        Crée la boite "font" dans les paramètres du widget, 
        est appelée lorsque le paramètre font est activé
        """
        try :
            self.clear("fontframe")
            if self.fontvar.get() == "1" :

                self.font_frame = ct.CTkFrame(self.edit_frame, border_width = 3, border_color= '#FFFFFF')
                self.font_frame.grid(column = 0, row =2, pady = 30, sticky = "w", ipadx = self.width*(7/100))

                self.font_lbl = ct.CTkLabel(self.font_frame, text = "Font", font=ct.CTkFont(size=20, weight="bold"))
                self.font_lbl.grid(row = 0, column = 0, columnspan = 2, padx = 10)

                self.familylbl = ct.CTkLabel(self.font_frame , text = "Family : ", font=ct.CTkFont(size=15, weight="bold") )
                self.family = ct.CTkEntry(self.font_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.familylbl.grid(row = 1, column = 0, padx = 10, pady = 5)
                self.family.grid(row = 1, column = 1, padx = 10, pady = 5)

                self.fontsizelbl = ct.CTkLabel(self.font_frame , text = "Size : ", font=ct.CTkFont(size=15, weight="bold") )
                self.fontsize =ct.CTkEntry(self.font_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.fontsizelbl.grid(row = 2, column = 0, padx = 10, pady = 5)
                self.fontsize.grid(row = 2, column = 1, padx = 10, pady = 5)

                self.fontweightlbl = ct.CTkLabel(self.font_frame , text = "Weight : ", font=ct.CTkFont(size=15, weight="bold") )
                self.fontweight = ct.CTkOptionMenu(self.font_frame, values = ["normal", "bold"])
                self.fontweightlbl.grid(row = 3, column = 0, padx = 10, pady = 5)
                self.fontweight.grid(row = 3, column = 1, padx = 10, pady = 5)

                self.slantlbl = ct.CTkLabel(self.font_frame , text = "Slant : ", font=ct.CTkFont(size=15, weight="bold") )
                self.slant = ct.CTkOptionMenu(self.font_frame, values = ["roman", "italic"])
                self.slantlbl.grid(row = 4, column = 0, padx = 10, pady = 5)
                self.slant.grid(row = 4, column = 1, padx = 10, pady = 5)

                self.underlinelbl = ct.CTkLabel(self.font_frame , text = "Underline : ", font=ct.CTkFont(size=15, weight="bold") )
                self.underline = ct.CTkSwitch(self.font_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
                self.underlinelbl.grid(row = 5, column = 0, padx = 10, pady = 5)
                self.underline.grid(row = 5, column = 1, padx = 10, pady = 5)
        
                self.overstrikelbl = ct.CTkLabel(self.font_frame , text = "Overstrike : ", font=ct.CTkFont(size=15, weight="bold") )
                self.overstrike = ct.CTkSwitch(self.font_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
                self.overstrikelbl.grid(row = 6, column = 0, padx = 10, pady = 5)
                self.overstrike.grid(row = 6, column = 1, padx = 10, pady = 5)

                for keys, values in AppAttr.get("widsetlist")[1].items():
                    match keys :
                        case "family" :
                            self.family.insert(0, values)
                        case "size" :
                            self.fontsize.insert(0, values)
                        case "weight" :
                            self.fontweight.set(values)
                        case "slant" :
                            self.slant.set(values)
                        case "underline" :
                            self.underline.toggle() if values == "1" else None
                        case "overstrike" :
                            self.overstrike.toggle() if values == "1" else None
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)


    def showLayoutFrame(self, value : str) -> None:
        """showLayoutFrame 
        crée l'encadré pour les paramètre de layout

        Parameters
        ----------
        value : str
            prend pour valeur le type de layout choisit ( pack ou grid )
        """
        try :
            self.layout_list = []
            self.clear("layoutframe")
            self.layout_frame = ct.CTkFrame(self.edit_frame, border_width = 3, border_color= '#FFFFFF')
            self.layout_frame.grid(column = 0, row =3, pady = 30, sticky = "w", ipadx = self.width*(7/100))

            self.layoutlbl = ct.CTkLabel(self.layout_frame, text = value, font=ct.CTkFont(size=20, weight="bold"))
            self.layoutlbl.grid(row = 0, column = 0, columnspan = 2, padx = 10)
            
            self.ipadxlbl = ct.CTkLabel(self.layout_frame, text = "ipadx", font=ct.CTkFont(size=15, weight="bold"))
            self.ipadxlbl.grid(row = 1, column = 0, padx = 10, pady = 5)
            self.ipadx = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.ipadx.grid(row = 1, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["ipadx",self.ipadx, ""])

            self.ipadylbl = ct.CTkLabel(self.layout_frame, text = "ipady", font=ct.CTkFont(size=15, weight="bold"))
            self.ipadylbl.grid(row = 2, column = 0, padx = 10, pady = 5)
            self.ipady = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.ipady.grid(row = 2, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["ipady",self.ipady, ""])

            self.padxlbl = ct.CTkLabel(self.layout_frame, text = "padx", font=ct.CTkFont(size=15, weight="bold"))
            self.padxlbl.grid(row = 3, column = 0, padx = 10, pady = 5)
            self.padx = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.padx.grid(row = 3, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["padx",self.padx, ""])

            self.padylbl = ct.CTkLabel(self.layout_frame, text = "pady", font=ct.CTkFont(size=15, weight="bold"))
            self.padylbl.grid(row = 4, column = 0, padx = 10, pady = 5)
            self.pady = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.pady.grid(row = 4, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["pady", self.pady, ""])

            if value == "grid" :

                self.columnlbl = ct.CTkLabel(self.layout_frame, text = "column", font=ct.CTkFont(size=15, weight="bold"))
                self.columnlbl.grid(row = 5, column = 0, padx = 10, pady = 5)
                self.column = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.column.grid(row = 5, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["column", self.column, ""])

                self.columnspanlbl = ct.CTkLabel(self.layout_frame, text = "columnspan", font=ct.CTkFont(size=15, weight="bold"))
                self.columnspanlbl.grid(row = 6, column = 0, padx = 10, pady = 5)
                self.columnspan= ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.columnspan.grid(row = 6, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["columnspan", self.columnspan, ""])

                self.rowlbl = ct.CTkLabel(self.layout_frame, text = "row", font=ct.CTkFont(size=15, weight="bold"))
                self.rowlbl.grid(row = 7, column = 0, padx = 10, pady = 5)
                self.row = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.row.grid(row = 7, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["row", self.row, ""])

                self.rowspanlbl = ct.CTkLabel(self.layout_frame, text = "rowspan", font=ct.CTkFont(size=15, weight="bold"))
                self.rowspanlbl.grid(row = 8, column = 0, padx = 10, pady = 5)
                self.rowspan = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.rowspan.grid(row = 8, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["rowspan", self.rowspan, ""])

                self.stickylbl = ct.CTkLabel(self.layout_frame, text = "sticky", font=ct.CTkFont(size=15, weight="bold"))
                self.stickylbl.grid(row = 9, column = 0, padx = 10, pady = 5)
                self.sticky = ct.CTkOptionMenu(self.layout_frame, values = ["None", 'w', "n", 's', 'e'])
                self.sticky.grid(row = 9, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["sticky", self.sticky, "None"])

            elif value == "pack" :
                
                self.afterlbl = ct.CTkLabel(self.layout_frame, text = "after", font=ct.CTkFont(size=15, weight="bold"))
                self.afterlbl.grid(row = 5, column = 0, padx = 10, pady = 5)
                self.afterentry = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.afterentry.grid(row = 5, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["after", self.afterentry, ""])

                self.anchorlbl = ct.CTkLabel(self.layout_frame, text = "anchor", font=ct.CTkFont(size=15, weight="bold"))
                self.anchorlbl.grid(row = 6, column = 0, padx = 10, pady = 5)
                self.anchorentry = ct.CTkOptionMenu(self.layout_frame, values = ["None", 'w', "n", 's', 'e'])
                self.anchorentry.grid(row = 6, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["anchor", self.anchorentry, 'None'])

                self.beforelbl = ct.CTkLabel(self.layout_frame, text = "before", font=ct.CTkFont(size=15, weight="bold"))
                self.beforelbl.grid(row = 7, column = 0, padx = 10, pady = 5)
                self.before = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
                self.before.grid(row = 7, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["before", self.before, ""])

                self.expandlbl = ct.CTkLabel(self.layout_frame, text = "expand", font=ct.CTkFont(size=15, weight="bold"))
                self.expandlbl.grid(row = 8, column = 0, padx = 10, pady = 5)
                self.expand = ct.CTkSwitch(self.layout_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
                self.expand.grid(row = 8, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["expand", self.expand, "0"])

                self.filllbl = ct.CTkLabel(self.layout_frame, text = "fill", font=ct.CTkFont(size=15, weight="bold"))
                self.filllbl.grid(row = 9, column = 0, padx = 10, pady = 5)
                self.fill= ct.CTkOptionMenu(self.layout_frame, values = ["None", 'x', 'y', 'both'])
                self.fill.grid(row = 9, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["fill", self.fill, "None"])

                self.sidelbl = ct.CTkLabel(self.layout_frame, text = "side", font=ct.CTkFont(size=15, weight="bold"))
                self.sidelbl.grid(row = 10, column = 0, padx = 10, pady = 5)
                self.side= ct.CTkOptionMenu(self.layout_frame, values = ["top", "bottom", "left", "right"])
                self.side.grid(row = 10, column = 1, padx = 10, pady = 5)
                self.layout_list.append(["side", self.side, "top"])


            for element in self.layout_list :
                if element[0] in AppAttr.get("widsetlist")[2].keys() :
                    if element[0] == "expand" :
                        element[1].toggle() if AppAttr.get("widsetlist")[2][element[0]] == "1" else None
                    elif element[0] in ("side", "fill", "sticky", "anchor"):
                        element[1].set(AppAttr.get("widsetlist")[2][element[0]])
                    else :
                        element[1].insert(0, AppAttr.get("widsetlist")[2][element[0]])
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)


    #-------------------- fonctions de gestions des évènements --------------------
                 

    def clear(self, mod : str) -> None:
        """clear 
        fonction de destruction de widgets

        Parameters
        ----------
        mod : str
            défini les widgets à détruire :
            -all : détruit tous les widgets de l'interface ( frames comprises )
            -itemFrame : détruit les boutons associés aux widgets
            -sets : détruit les labels et entrées de paramètres d'un widget
            -fontframe : détruit la frame des paramètres de font
            -layoutframe : détruit la frame contenant les paramètres de layout du widget
        """
        try : 
            if mod == 'all' :
                liste = self.grid_slaves() + self.pack_slaves()
                for element in liste :
                    element.destroy()
                self.createInterface()
                if AppAttr.get("widget") != None :
                    self.widgetParametersFrame(AppAttr.get("widget"))
                self.sideWidgetsUptdating()
            if mod == 'itemFrame' :
                liste = self.main_item_frame.grid_slaves()
                for element in liste :
                    element.destroy()
            if mod == 'sets':
                liste = self.edit_frame.grid_slaves()
                for element in liste :
                    element.destroy()
            if mod == 'fontframe' :
                try : 
                    liste = self.font_frame.grid_slaves()
                    for element in liste :
                        element.destroy()
                    self.font_frame.destroy()
                except :
                    pass
            if mod == 'layoutframe' :
                try : 
                    liste = self.layout_frame.grid_slaves()
                    for element in liste :
                        element.destroy()
                    self.layout_frame.destroy()
                    self.layout_list = []
                except :
                    pass
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)


    def modifyWid(self, *event) -> None:
        """modifyWid 
        fonction de modification des paramètres d'un widget,
        appele la fonction de chargement/envoi de données (fLoadFunct)
        """
        try :
            if AppAttr.get("widget") == None :
                return
            layout_dico = {}
            font_dico = {}
            dico = {}
            id_card_dict = {}
            #creation of the ID card of the widget
            if ControlReq.tryWN(self.widname.get()) == True :
                id_card_dict["name"] = self.widname.get()
            else :
                messagebox.showerror("Erreur d'entrée", "Le nom du widget est invalide.")
                id_card_dict["name"] = AppAttr.get("widget")
                #on supprime le nom invalide dans l'entrée associée et le remplace par le précédent nom
                self.widname.delete()
                self.widname.insert(0, AppAttr.get("widget"))
            id_card_dict["ID"] = AppAttr.get("widget_id")
            id_card_dict["slaves"] = True if AppAttr.get("widsetlist")[3]["slaves"] == True else False
            id_card_dict["layout"] = None
            id_card_dict["initcode"] = AppAttr.get("widsetlist")[3]["initcode"]
            id_card_dict["layoutcode"] = AppAttr.get("widsetlist")[3]["layoutcode"]

            #vérification du layout et ajout dans le dictionnaire correspondant
            if self.layout.get() != "" :
                id_card_dict["layout"] = self.layout.get()
                for element in self.layout_list :
                    if element[1].get() != element[2] :
                        if (element[0] in ("column", "columnspan", "row", "rowspan") or 
                        (element[0] in ("ipadx", "ipady", "padx", "pady") and element[1].get() != "0")) :
                            try :
                                layout_dico[element[0]] = int(element[1].get())
                            except :
                                messagebox.showerror("Erreur d'entrée", "Un mauvais nombre a été entré comme paramètre dans le layout")
                        else : 
                            layout_dico[element[0]] = element[1].get()
            else :
                messagebox.showerror("Erreur d'entrée", "Aucune méthode de layout sélectionné")
                return 

            for element in self.actual_sets :
                
                if element[1] in ["width", "height"] :
                    if element[0].get() != "Default" :
                        dico[element[1]] = int(element[0].get())
                    
                #on s'occupe des paramètres de font
                elif element[1] == "font" :
                    dico[element[1]] = element[0].get()
                    if dico[element[1]] == "1" :
                        
                        if self.family.get() != "" :
                            family = ControlReq.tryFont(self.family.get())
                            if family == False :
                                messagebox.showerror("Erreur d'entrée", "Mauvaise police d'écriture entrée")
                                return 0
                            else :
                                font_dico["family"] = family
                        
                        if self.fontsize.get() != "" :
                            try :
                                font_dico["size"] = int(self.fontsize.get())
                            except :
                                messagebox.showerror("Erreur d'entrée", "Mauvaise taille de caractère entrée.")
                                return 0
                        
                        if self.fontweight.get() != "normal" :
                            font_dico["weight"] = self.fontweight.get()
                            
                        if self.slant.get() != "roman" :
                            font_dico["slant"] = self.slant.get()
                            
                        if self.underline.get() != '0' :
                            font_dico["underline"] = "True"
                            
                        if self.overstrike.get() != '0' :
                            font_dico["overstrike"] = "True"
                        #si aucun paramètre de font n'est utilisé, on met le paramètre font par défaut
                        if len(font_dico) == 0 :
                            dico[element[1]] = '0'
                    
                elif element[1] == "hover" :
                    if element[0].get() == "0" : dico[element[1]] = "False"
                    else : dico[element[1]] = "True"

                elif element [1] == "image" :
                    pass

                elif element [1] == "master":
                    if element[0].get() in AppAttr.get("widnamelist") or element[0].get().strip() == "window" :
                        id_card_dict["master"] = element[0].get()
                        if element[0].get() in AppAttr.get("widnamelist") : 
                            subdict = AppAttr.get("prjtwidsetslist")
                            subdict[element[0].get()][3]["slaves"] += 1
                            AppAttr.config("prjtwidsetslist", subdict)
                    else : 
                        messagebox.showerror("Erreur d'entrée","Widget parent désigné invalide.")
                        return
                elif element[1] == "text":
                    text = self.text.replace("\'", "\\\'").replace("\"", "\\\""). replace("\\", "\\\\")
                    dico[element[1]] = text

                elif element[1] == "values":
                        dico[element[1]] = self.values

                elif element[1] == "command" :
                    if self.command[0] != "" :
                        dico[element[1]] = self.command

                elif element[1] == "variable" :
                    if self.variable not in [None, ""] :
                        dico[element[1]] = self.variable

                elif element[1] == "textvariable" :
                    if self.textvariable not in [None, ""] :
                        dico[element[1]] = self.textvariable

                else : 
                    if element[0].get() != AppAttr.get("widsets")[element[1]][0] :
                        dico[element[1]] = element[0].get()


            main_dict = AppAttr.get("prjtwidsetslist")
            del main_dict[AppAttr.get("widget")]
            main_dict[id_card_dict["name"]] = (dico, font_dico, layout_dico, id_card_dict)
            AppAttr.config("prjtwidsetslist", main_dict)
            AppAttr.config("widget", (AppAttr.get("widget"),id_card_dict["name"]))

            widname_list = AppAttr.get("widnamelist")
            widname_list.insert(widname_list.index(AppAttr.get("widget")[0]), AppAttr.get("widget")[1])
            del widname_list[widname_list.index(AppAttr.get("widget")[0])]
            AppAttr.config("widnamelist", widname_list)

            WidgetReq.modifyWidSetReq()
            AppAttr.config("saved", False)
            self.overal_lbl.configure(text = id_card_dict["name"])
            self.sideWidgetsUptdating()
            self.codeFrame()
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)


    def getSettings(self, *event) -> None:
        """getSettings 
        fonction de récupération des paramètres de l'application,
        attribue les paramètres chargé aux variable de l'application
        """
        try :
            def getGeometry():
                match AppAttr.get("settings")["display"] :
                    case "windowed" :
                        self.state("normal")
                        self.attributes('-fullscreen', False)
                        self.width   = AppAttr.get( "settings")["width"]
                        self.height  = AppAttr.get( "settings")["height"]
                    case "fullscreen_windowed" :
                        self.attributes('-fullscreen', False)
                        self.state("zoomed")
                        self.width   = self.winfo_screenwidth() -10
                        self.height  = self.winfo_screenheight() -100
                        
                    case "fullscreen":
                        self.width   = self.winfo_screenwidth() -10
                        self.height  = self.winfo_screenheight() -10
                        self.attributes('-fullscreen', True)
                
                self.geometry("500x300")
                self.minsize(self.width, self.height)

            getGeometry()
            
            self.detail_lvl  = AppAttr.get( "settings")["detail"]
            self.language = AppAttr.get("settings")["int_language"]

            ct.set_default_color_theme(AppAttr.get( "settings")["color"])
            ct.set_appearance_mode(AppAttr.get( "settings")["theme"])
            
            self.title("Saturne")
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)
        

    def resetAttr(self) -> None:
        """resetAttr 
        Fonction de réinitialisation de certaines variables de l'application,
        utilisé lorsque l'application est lancé sans projet ouvert
        """
        if AppAttr.get("project") == None :
            AppAttr.config("widnamelist", [])
            AppAttr.config("widget", None)


    def delWid(self, *event) -> None:
        """delWid 
        Fonction de suppression d'un widget.
        """
        try :
            if AppAttr.get("widget") == None :
                messagebox.showinfo("Suppression impossible", "Suppression impossible, aucun widget n'est ouvert.")
                return 
            if AppAttr.get("widsetlist")[3]["slaves"] != 0 :
                messagebox.showerror("Suppression impossible", "Suppression impossible, ce widget possède des widgets enfants")
                return
            WidgetReq.delWidReq()
            self.clear("sets")
            self.actual_sets = []
                    
            data = AppAttr.get("prjtwidsetslist")
            del data[AppAttr.get("widget")]
            if AppAttr.get("widsetlist")[3]["master"] != "window":
                data[AppAttr.get("widsetlist")[3]["master"]][3]["slaves"] -= 1
            AppAttr.config("prjtwidsetslist", data)

            data = AppAttr.get("widnamelist")
            del data[data.index(AppAttr.get("widget"))]
            AppAttr.config("widnamelist", data)

            AppAttr.config("widget", None)
            AppAttr.config("widget_id", None)
            AppAttr.config("saved", False)
            AppAttr.config("widsetlist", [])
            self.sideWidgetsUptdating()
            self.configActionBt()
            self.codeFrame()
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)


    def on_quit(self) -> None:
        """on_quit 
        Détruit la fenêtre lorsque le bouton "Quitter" du menu est pressé
        """
        print(AppAttr.get("saved"))
        if AppAttr.get("saved") == False :
            quitting = messagebox.askokcancel("Modification non enregistrée", 
                                              "Voulez-vous quitter l'application ?\ntoute modfication non enregistrée sera perdue")
            if quitting == True :
                self.destroy()
                AppAttr.config("closelogs")
            else :
                pass
        else : 
            AppAttr.config("closelogs")
            self.destroy()


    def copyCode(self, event = None):
        copy = self.code_output.get("0.0", "end") + "\n\nwindow.mainloop()"
        self.clipboard_clear()
        self.clipboard_append(copy)


    def openPreview(self, event = None):
        path =  CodeReq.getProjectPath() + "\\" + "code_exemple.py"
        with open(path, "w", encoding = "utf8") as file :
            file.write(AppAttr.get("code") + "\n\nwindow.mainloop()")
        subprocess.run(["python", path])
        CodeReq.shutdownExe(path)


    def savefile(self, event = None):
        ProjectReq.saveModifReq()
        AppAttr.config("saved", True)


    def winState(self, event):
        if self.attributes("-fullscreen") == True :
            self.attributes('-fullscreen', False)
            self.state("zoomed")
            self.width   = self.winfo_screenwidth() -10
            self.height  = self.winfo_screenheight() -100
            self.minsize(self.width, self.height)
            self.clear('all')
            return
        elif self.state() == "normal":
            self.state("iconic")
            return
        else :
            self.state("normal")
            self.width   = AppAttr.get( "settings")["width"]
            self.height  = AppAttr.get( "settings")["height"]
            self.minsize(self.width, self.height)
            self.clear('all')


    def undo(self, *event):
        if len(AppAttr.get("cache")) == 0 :
            return
        AppAttr.config("saved", False)
        CacheReq.undo()
        self.codeFrame()
        self.sideWidgetsUptdating()
        self.widgetParametersFrame(AppAttr.get("widget"))


    def redo(self, *event):
        if len(AppAttr.get("redo_cache")) == 0 :
            return
        AppAttr.config("saved", False)
        CacheReq.redo()
        self.codeFrame()
        self.sideWidgetsUptdating()
        self.widgetParametersFrame(AppAttr.get("widget"))


    #-------------------- fonctions de création de fenêtres enfant --------------------
    

    def openTextTopLevel(self):
        if self.app != None :
            return
        self.app = TextTopLevelWin(self.text)
        self.app.grab_set()
        self.text = self.app.contentGet()
        self.app = None


    def openValuesTopLevel(self):
        if self.app != None :
            return
        self.app = ValuesTopLevelWin(values = self.values)
        self.app.grab_set()
        self.values = self.app.contentGet()
        self.app = None
    

    def openCommandTopLevel(self):
        if self.app != None :
            return
        self.app = CommandTopLevelWin(values = self.command)
        self.app.grab_set()
        self.command = self.app.contentGet()
        self.app = None


    def openVariableTopLevel(self, var):
        if self.app != None :
            return
        if var == "variable" : text = self.variable
        else : text = self.textvariable
        self.app = VariableTopLevelWin(texte = text)
        self.app.grab_set()
        if var == "variable" : self.variable = self.app.contentGet()
        else : self.textvariable = self.app.contentGet()
        self.app = None


    def openProjectApp(self, *event, **kwargs ) -> None:
        """openProjectApp 
        Fonction d'ouverture de la fenêtre de projets,
        modifie le nom de l'application si un projet est ouvert
        """
        if self.project_app != None :
            return
        if "reason" in kwargs.keys() :
            if kwargs["reason"] == None :
                reason = AppAttr.get("project")
            else :
                reason = kwargs["reason"]
        else :
            reason = AppAttr.get("project")

        self.project_app = ProjectApp(reason)
        self.project_app.grab_set()
        self.project_app.on_destroy()
        self.project_app = None
        if AppAttr.get("project") != None :
            self.title(f"Saturne : {AppAttr.get("project")}")
            init = ProjectReq.initProjectAttrReq()
            if init == False : 
                messagebox.showwarning("Error", "An error occured while loading the project's data.\n See the logs for more details")
                self.on_quit()
            self.sideWidgetsUptdating()
        else :
            self.title("Saturne")
            self.resetAttr()
        self.clear('all')


    def openParameters(self, *event) -> None:
        """openParameters 
        fonction d'ouverture des paramètres, 
        appele la fonction "getSettings" à l'issue
        """
        if self.settings == None :
            self.settings = AppEditing()
            self.settings.grab_set()
            self.settings = self.settings.on_destroy()
            self.settings = None
            self.getSettings()
            self.clear('all')
        else :
            print("fenêtre de paramètres déjà ouverte")


    def widgetAdding(self, *event) -> None:
        """widgetAdding 
        Fonction d'ouverture de la fenêtre d'ajout de Widgets
        """
        if self.widgetapp == None :
            self.widgetapp = WidgetApp()
            self.widgetapp.grab_set()
            self.widgetapp = self.widgetapp.on_destroy()
            if AppAttr.get( "widget_id") != None :
                WidgetReq.createWidSetFileReq()
                data = AppAttr.get("widnamelist")[::]
                data.append(AppAttr.get("widget"))
                AppAttr.config("widnamelist", data)
                AppAttr.config("saved", False)
                self.sideWidgetsUptdating()
        else :
            print("fenêtre d'ajout d'un widget déjà ouverte")


if __name__ == "__main__":
    if AppAttr.config("const") :
        app = interface()
        app.mainloop()
    else :
        AppAttr.config("closelogs")