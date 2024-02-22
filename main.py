#fichier contenant l'interface graphique du programme
from typing import Union
import tkinter as tk
from tkinter import messagebox
import customtkinter as ct
import tool_tip as tl
from intermediateLayer import *
from settingsApp import AppEditing
from widgetApp import WidgetApp
from projectApp import ProjectApp
import subprocess
from appattr import AppAttr



class interface(ct.CTk):


    def __init__(self) -> None:
        super().__init__()
        
        self.actual_sets = [] #liste des paramètres utilisés dans l'application
        self.layout_list = [] #liste contenant des paramètres de layout, comprenant pour chacun : leur nom, entrée associée, et valeur par défaut
        self.settings = None # défini si la fenêtre de paramètre est ouverte ou non
        self.widgetapp = None # défini si la fenêtre de widgets est ouverte ou non
        self.project_app = None # défini si la fenêtre des projets est ouverte ou non


        self.getSettings()
        self.createInterface()
        if AppAttr.get("widget") != None :
            self.widgetParametersFrame(AppAttr.get("widget"))
        self.openProjectApp(reason = "new")


    #-------------------- fonctions de création de la fenêtres --------------------
        

    def createInterface(self) -> None:
        """createInterface
        Fonction de création du corps de l'interface
        """
        #-------------------- création des frames --------------------
        
        
        self.code_frame = ct.CTkFrame(self, width=self.width*(45/100), height=self.height, border_color = "#000000", border_width= 2)
        self.edit_frame = ct.CTkScrollableFrame(self, width=self.width*(35/100), height=self.height*(90/100))
        self.actionbtframe = ct.CTkFrame(self, height = self.height*(10/100), width = self.width*(55/100))
        self.main_item_frame = ct.CTkScrollableFrame(self, height = self.height*(85/100), width = self.width*(18/100), label_text = "widgets :")


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
        
        self.fichier.add_command(label = "Ouvrir un projet", command = lambda x = AppAttr.get("project") : self.openProjectApp(x))
        self.fichier.add_command(label = "Nouveau projet", command = lambda x = "new" : self.openProjectApp(x))
        self.fichier.add_separator()
        self.fichier.add_command(label='Vérifier les fichiers', command = lambda : self.verifyFiles())
        
        self.application.add_command(label= "Recharger", command = lambda x = "all" : self.clear(x))
        self.application.add_command(label= "Paramètres", command = lambda : self.openParameters())
        self.application.add_command(label='Quitter', command = lambda : self.on_quit())

        self.widget_menu.add_command(label='Ajouter un widget', command = lambda : self.widgetAdding())
        self.widget_menu.add_command(label='Supprimer', command = lambda : self.delWid())
        self.widget_menu.add_command(label='Modifier', command = lambda : self.modifyWid())
        

        self.code_menu.add_command(label='Copier le code', command = lambda : self.copyCode())
        self.code_menu.add_command(label='Aperçu', command = lambda : self.openPreview())


        self.menubar.add_cascade(label = "fichiers", menu = self.fichier)
        self.menubar.add_cascade(label = "Application", menu = self.application)
        self.menubar.add_cascade(label = "Widget", menu = self.widget_menu)
        self.menubar.add_cascade(label = "Code", menu = self.code_menu)
        

        #-------------------- création des widgets et des boutons d'actions --------------------


        self.code_output = ct.CTkTextbox(self.code_frame, width=self.width*(40/100), height=self.height*(96/100)-20, activate_scrollbars=False)
        self.code_scrollbar = ct.CTkScrollbar(self.code_frame, command=self.code_output.yview, height=self.height*(96/100)-20)
        self.code_scrollbar.grid()
        self.code_output.configure(yscrollcommand=self.code_scrollbar.set)

        self.copy_bt = ct.CTkButton(self.code_frame, width= self.width*(10/100), height= self.height*(4/100),
                                    text = "Copier", font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, 
                                    command = lambda : self.copyCode())
        self.preview_bt = ct.CTkButton(self.code_frame, width= self.width*(10/100), height= self.height*(4/100),
                                       text = "Aperçu", font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, 
                                       command = lambda : self.openPreview())


        self.parameter_button = ct.CTkButton(self.actionbtframe, width= self.width*(10/100), height= self.height*(6/100),
                                             text = "paramètres", font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.openParameters())
        tl.CreateToolTip(self.parameter_button, text = "Bouton d'ouverture de la fenêtre de paramètres.") if self.showtooltip == "Oui" else None

        self.modify_button = ct.CTkButton(self.actionbtframe,  width= self.width*(10/100), height= self.height*(6/100),
                                             text = "modifier", font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.modifyWid())
        tl.CreateToolTip(self.modify_button, text = "Bouton de modification des paramètres d'un widget.") if self.showtooltip == "Oui" else None
        self.modify_button.configure(state = "disabled") if AppAttr.get("widget") == None else None

        self.delete_button = ct.CTkButton(self.actionbtframe,  width= self.width*(10/100), height= self.height*(6/100),
                                             text = "supprimer", font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda : self.delWid())
        tl.CreateToolTip(self.delete_button, text = "Bouton de suppression d'un widget.") if self.showtooltip == "Oui" else None
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
        
        self.add_button = ct.CTkButton(self.main_item_frame, width= self.width*(16/100), height= 40, text = "Ajouter",border_width= 2, border_color = "#FFFFFF",
                                       font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command= lambda : self.widgetAdding())
        tl.CreateToolTip(self.add_button, text = "Bouton d'ajout de widgets dans le projet.") if self.showtooltip == "Oui" else None
        self.add_button.configure(state = "disabled") if AppAttr.get("project") == None else None
        self.add_button.grid(padx = 5, pady = 5)
        for widgets in AppAttr.get("widnamelist") :
            if widgets != "" :
                w_bt = ct.CTkButton(self.main_item_frame, text = widgets, width= self.width*(16/100), height= self.height*(6/100), 
                                    font=ct.CTkFont(size=15, weight="bold"), corner_radius= 10, command = lambda w_id = widgets : self.widgetParametersFrame(w_id))
                w_bt.grid(padx = 5, pady = 5)
            else : pass


    def widgetParametersFrame(self, widget : str)  -> None:
        """widgetParametersFrame 
        fonction de création de la frame de paramètres du widget

        Parameters
        ----------
        widget : str
            widget dont la fonction doit afficher les paramètres, et leurx valeurs respectives
        """
        self.clear("sets")
        self.actual_sets = []
        AppAttr.config("widget", widget)
        #on configue les boutons d'action pour les rendre actifs
        self.configActionBt()
        #on configure la disposition des paramètres selon la largeur de la fenêtre
        self.column_num = 1 if self.width*(30/100) < 525 else 3
        row = 2
        column = 0
        loading = True
        try :
            #on récupère les données du widget, les données associées à chaque paramètre, et les paramètre par défaut du widget
            AppAttr.config("widsetlist",self.fLoadFunct("getWidSet"))
            AppAttr.config("widget_id",AppAttr.get("widsetlist")[0]["ID"])
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
                self.overal_lbl = ct.CTkLabel(self.edit_frame, text = AppAttr.get("widsetlist")[0]["name"],font=ct.CTkFont(size=25, weight="bold"))

                self.widnamelbl = ct.CTkLabel(self.settings_frame, text = "Nom du widget :",font=ct.CTkFont(size=15, weight="bold"))
                self.widname = ct.CTkEntry(self.settings_frame, width= 150, height = 40,font=ct.CTkFont(weight="bold"))
                tl.CreateToolTip(self.widnamelbl, "Nom du widget, attention ce nom sera aussi utilisé comme nom de variable dans le code.") if self.showtooltip == "Oui" else None
                self.widname.insert(0, AppAttr.get("widsetlist")[0]["name"])

                self.overal_lbl.grid(column = 0, row = 0 , pady = 15, sticky = 'w')
                self.widnamelbl.grid(row = 1, column = 0, columnspan = 2 if self.column_num == 3 else 1, 
                                     pady = 20, sticky = 'e')
                self.widname.grid(row = 1, column = 2 if self.column_num == 3 else 1, 
                                  columnspan = 2 if self.column_num == 3 else 1 , padx = 10, pady = 20)
                
                detail_dico = {"Simple" : (0,1), "Normal" : (1,2), "Complet" : (1,2,3)}
                
                #on crée le reste des paramètres, selon le type ( soit une entrée texte, un menu, ou un switch)
                for parameter in AppAttr.get("widinfo")[AppAttr.get("widget_id")]["parameters"]:
                    
                    if AppAttr.get("widsets")[parameter][1] in detail_dico[self.detail_lvl] :
                        lbl = ct.CTkLabel(self.settings_frame, text = parameter + " :", font=ct.CTkFont(size=12, weight="bold"))
                        
                        if parameter in ["font", "hover", "image"]:
                            entry = ct.CTkSwitch(self.settings_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
                            entry.select() if AppAttr.get("widsetlist")[0][parameter] == '1' else None
                            if parameter == "font" : self.fontvar= ct.StringVar(value = AppAttr.get("widsetlist")[0][parameter])
                            entry.configure(command = lambda : self.showFontFrame(), variable = self.fontvar) if parameter == "font" else None
                            
                        
                        elif parameter in ["state", "anchor", "compound", "justify"]:
                            entry = ct.CTkOptionMenu(self.settings_frame, values = AppAttr.get("widsets")[parameter][3])  
                            entry.set(AppAttr.get("widsetlist")[0][parameter])  
                        
                        else :
                            entry = ct.CTkEntry(self.settings_frame, width = 100,font=ct.CTkFont(weight="bold"))
                            entry.insert(0, AppAttr.get("widsetlist")[0][parameter])
                        self.actual_sets.append((entry, parameter))
                        tl.CreateToolTip(lbl, AppAttr.get("widsets")[parameter][2]) if self.showtooltip == "Oui" else None
                        
                        lbl.grid(row = row, column = column, padx = 5, pady = 10, sticky = 'n')
                        column = column + 1 if column < self.column_num else 0
                        row += 1 if column == 0 else 0
                        
                        entry.grid(row = row, column = column, padx = 5, pady = 10, sticky = 'n')
                        column = column + 1 if column < self.column_num else 0
                        row += 1 if column == 0 else 0

                self.layoutlbl = ct.CTkLabel(self.settings_frame, text = "affichage du widget : ", font=ct.CTkFont(size=15, weight="bold") )
                self.layout = ct.CTkSegmentedButton(self.settings_frame, font=ct.CTkFont(size=15, weight="bold"), values = ["pack", "grid"], 
                                                     command = self.showLayoutFrame)
                self.layout.set(AppAttr.get("widsetlist")[0]["layout"]) if AppAttr.get("widsetlist")[0]["layout"] != None else None
                self.layoutlbl.grid(row = row +1, column = 0)
                self.layout.grid(row = row+1, column = 1)
                
                try : self.showFontFrame() if self.fontvar.get() == "1" else None
                except : pass
                
                try : self.showLayoutFrame(self.layout.get()) if self.layout.get() != "" else None
                except : pass

            except any as error :
                print(error)
                messagebox.showwarning("Erreur de chargement", "Une erreur est survenue lors de l'affichage des données")


    def codeFrame(self):
        #permet d'afficher le code de l'interface
        self.txt_code = CodeReq.getCodeReq()
        if self.txt_code == None :
            messagebox.showerror("Erreur d'affichage", "Une erreur est survenue lors de l'affichage du code.")
            return
        self.code_output.delete("0.0", "end")
        self.code_output.insert("0.0", self.txt_code)


    def showFontFrame(self):
        """showFontFrame 
        Crée la boite "font" dans les paramètres du widget, 
        est appelée lorsque le paramètre font est activé
        """
        print("passed")
        self.clear("fontframe")
        if self.fontvar.get() == "1" :

            self.font_frame = ct.CTkFrame(self.edit_frame, border_width = 3, border_color= '#FFFFFF')
            self.font_frame.grid(column = 0, row =2, pady = 30, sticky = "w", ipadx = self.width*(7/100))

            self.font_lbl = ct.CTkLabel(self.font_frame, text = "Font", font=ct.CTkFont(size=20, weight="bold"))
            self.font_lbl.grid(row = 0, column = 0, columnspan = 2, padx = 10)

            self.familylbl = ct.CTkLabel(self.font_frame , text = "Family : ", font=ct.CTkFont(size=15, weight="bold") )
            self.family = ct.CTkEntry(self.font_frame, width = 100,font=ct.CTkFont(weight="bold"))
            tl.CreateToolTip(self.familylbl,"Nom de la police") if self.showtooltip == "Oui" else None
            self.familylbl.grid(row = 1, column = 0, padx = 10, pady = 5)
            self.family.grid(row = 1, column = 1, padx = 10, pady = 5)

            self.fontsizelbl = ct.CTkLabel(self.font_frame , text = "Size : ", font=ct.CTkFont(size=15, weight="bold") )
            self.fontsize =ct.CTkEntry(self.font_frame, width = 100,font=ct.CTkFont(weight="bold"))
            tl.CreateToolTip(self.fontsizelbl,"Taille du texte") if self.showtooltip == "Oui" else None
            self.fontsizelbl.grid(row = 2, column = 0, padx = 10, pady = 5)
            self.fontsize.grid(row = 2, column = 1, padx = 10, pady = 5)

            self.fontweightlbl = ct.CTkLabel(self.font_frame , text = "Weight : ", font=ct.CTkFont(size=15, weight="bold") )
            self.fontweight = ct.CTkOptionMenu(self.font_frame, values = ["normal", "bold"])
            tl.CreateToolTip(self.fontweightlbl,"Mise en Gras du texte ( bold ), normal sinon") if self.showtooltip == "Oui" else None
            self.fontweightlbl.grid(row = 3, column = 0, padx = 10, pady = 5)
            self.fontweight.grid(row = 3, column = 1, padx = 10, pady = 5)

            self.slantlbl = ct.CTkLabel(self.font_frame , text = "Slant : ", font=ct.CTkFont(size=15, weight="bold") )
            self.slant = ct.CTkOptionMenu(self.font_frame, values = ["roman", "italic"])
            tl.CreateToolTip(self.slantlbl,"Mise en italique du texte ( italic), roman sinon") if self.showtooltip == "Oui" else None
            self.slantlbl.grid(row = 4, column = 0, padx = 10, pady = 5)
            self.slant.grid(row = 4, column = 1, padx = 10, pady = 5)

            self.underlinelbl = ct.CTkLabel(self.font_frame , text = "Underline : ", font=ct.CTkFont(size=15, weight="bold") )
            self.underline = ct.CTkSwitch(self.font_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
            tl.CreateToolTip(self.underlinelbl,"Soulignage du texte") if self.showtooltip == "Oui" else None
            self.underlinelbl.grid(row = 5, column = 0, padx = 10, pady = 5)
            self.underline.grid(row = 5, column = 1, padx = 10, pady = 5)
    
            self.overstrikelbl = ct.CTkLabel(self.font_frame , text = "Overstrike : ", font=ct.CTkFont(size=15, weight="bold") )
            self.overstrike = ct.CTkSwitch(self.font_frame, text = "", onvalue="1", offvalue="0", switch_width= 48,switch_height= 18)
            tl.CreateToolTip(self.overstrikelbl,"Raturage du texte") if self.showtooltip == "Oui" else None
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


    def showLayoutFrame(self, value : str) -> None:
        """showLayoutFrame 
        crée l'encadré pour les paramètre de layout

        Parameters
        ----------
        value : str
            prend pour valeur le type de layout choisit ( pack ou grid )
        """
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
            self.sticky = ct.CTkOptionMenu(self.layout_frame, values = ['W', "N", 'S', 'E'])
            self.sticky.grid(row = 9, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["sticky", self.sticky, "E"])

        elif value == "pack" :
            
            self.afterlbl = ct.CTkLabel(self.layout_frame, text = "after", font=ct.CTkFont(size=15, weight="bold"))
            self.afterlbl.grid(row = 5, column = 0, padx = 10, pady = 5)
            self.afterentry = ct.CTkEntry(self.layout_frame, width = 100,font=ct.CTkFont(weight="bold"))
            self.afterentry.grid(row = 5, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["after", self.afterentry, ""])

            self.anchorlbl = ct.CTkLabel(self.layout_frame, text = "anchor", font=ct.CTkFont(size=15, weight="bold"))
            self.anchorlbl.grid(row = 6, column = 0, padx = 10, pady = 5)
            self.anchorentry = ct.CTkOptionMenu(self.layout_frame, values = ['W', "N", 'S', 'E'])
            self.anchorentry.grid(row = 6, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["anchor", self.anchorentry, 'W'])

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
            self.fill= ct.CTkOptionMenu(self.layout_frame, values = ["None", 'X', 'Y', 'BOTH'])
            self.fill.grid(row = 9, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["fill", self.fill, "None"])

            self.sidelbl = ct.CTkLabel(self.layout_frame, text = "side", font=ct.CTkFont(size=15, weight="bold"))
            self.sidelbl.grid(row = 10, column = 0, padx = 10, pady = 5)
            self.side= ct.CTkOptionMenu(self.layout_frame, values = ["TOP", "BOTTOM", "LEFT", "RIGHT"])
            self.side.grid(row = 10, column = 1, padx = 10, pady = 5)
            self.layout_list.append(["side", self.side, "TOP"])


        for element in self.layout_list :
            if element[0] in AppAttr.get("widsetlist")[2].keys() :
                if element[0] == "expand" :
                    element[1].toggle() if AppAttr.get("widsetlist")[2][element[0]] == "1" else None
                elif element[0] in ("side", "fill", "sticky", "anchor"):
                    element[1].set(AppAttr.get("widsetlist")[2][element[0]])
                else :
                    element[1].insert(0, AppAttr.get("widsetlist")[2][element[0]])


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


    def fLoadFunct(self, event : str, *dico : list) -> Union[None, dict]:
        """fLoadFunct _summary_
        fonction d'envoi de requêtes de chargement/envoi de données

        Parameters
        ----------
        event : str
            décrit l'action à réaliser :
            -getWidSet : récupère les données d'un widget ciblé            ( fichier "[nom du projet]\[nom du widget].json")
            -modifyWidSet : modifie les données d'un widget ciblé          ( fichier "[nom du projet]\[nom du widget].json")
        Returns
        -------
        Union[None, dict]
            renvoie None dans la plupart des cas, 
            renvoie un dictionnaire si l'appel est lié à l'obtention des données d'un widget
        """
        if event == "getWidSet" :
            return WidgetReq.getWidSetReq()
        if event == 'modifyWidSet' :
            AppAttr.config("widsetlist", dico[0])
            WidgetReq.modifyWidSetReq()


    def modifyWid(self) -> None:
        """modifyWid 
        fonction de modification des paramètres d'un widget,
        appele la fonction de chargement/envoi de données (fLoadFunct)
        """
        if AppAttr.get("widget") != None :
            layout_dico = {}
            font_dico = {}
            dico = {}
            dico['ID'] = AppAttr.get("widget_id")

            #vérification du layout et ajout dans le dictionnaire correspondant
            if self.layout.get() != "" :
                dico["layout"] = self.layout.get()
                for element in self.layout_list :
                    if element[1].get() != element[2] :
                        if element[0] in ("column", "columnspan", "row", "rowspan") or (element[0] in ("ipadx", "ipady", "padx", "pady") and element[1].get() != "0") :
                            try :
                                layout_dico[element[0]] = int(element[1].get())
                            except :
                                messagebox.showerror("Erreur d'entrée", "Un mauvais nombre a été entré comme paramètre dans le layout")
                        else : 
                            layout_dico[element[0]] = element[1].get()
            else :
                messagebox.showerror("Erreur d'entrée", "Aucune méthode de layout sélectionné")
                return 0
            #on vérifie que le nom de widget donné respecte les règles de typage pour une variable
            if ControlReq.tryWN(self.widname.get()) == True :
                dico["name"] = self.widname.get() 
            else :
                messagebox.showerror("Erreur d'entrée", "Le nom du widget est invalide.")
                dico["name"] = AppAttr.get("widget")
                #on supprime le nom invalide dans l'entrée associée et le remplace par le précédent nom
                self.widname.delete()
                self.widname.insert(0, AppAttr.get("widget"))
            
            for element in self.actual_sets :
                
                if element[1] in ["width", "height"] :
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
                
                else : 
                    dico[element[1]] = element[0].get()
            
            self.fLoadFunct("modifyWidSet", [dico, font_dico, layout_dico])
            self.overal_lbl.configure(text = dico["name"])
            AppAttr.config("widget", dico["name"])
            self.sideWidgetsUptdating()
            self.codeFrame()
        else : 
            messagebox.showinfo("Utilisation impossible", "Modification impossible, aucun widget n'est ouvert.")


    def getSettings(self) -> None:
        """getSettings 
        fonction de récupération des paramètres de l'application,
        attribue les paramètres chargé aux variable de l'application
        """

        if AppAttr.get( "settings")["fullscreen"]: 
            self.width   = self.winfo_screenwidth() -10
            self.height  = self.winfo_screenheight() -10
            self.attributes('-fullscreen', True)
        else : 
            self.attributes('-fullscreen', False)
            self.width   = AppAttr.get( "settings")["width"]
            self.height  = AppAttr.get( "settings")["height"]
        self.showtooltip = AppAttr.get( "settings")["tooltip"]
        self.detail_lvl  = AppAttr.get( "settings")["detail"]

        ct.set_default_color_theme(AppAttr.get( "settings")["color"])
        ct.set_appearance_mode(AppAttr.get( "settings")["theme"])
        
        self.title("Saturne")
        self.geometry("500x300")
        self.minsize(self.width, self.height)


    def verifyFiles(self) -> None:
        """verifyFiles 
        Fonction de vérification des fichiers de l'application
        """
        verify = ControlReq.verifyFilesRqst()
        if verify[0] != True :
            messagebox.showwarning("Fichier manquant", f"Un fichier ou dossier est manquant \nname : {verify[0]}; class : {verify[1]}")
        else :
            messagebox.showinfo("Fichiers complets", "Tous les fichiers sont présents")
        

    def resetAttr(self) -> None:
        """resetAttr 
        Fonction de réinitialisation de certaines variables de l'application,
        utilisé lorsque l'application est lancé sans projet ouvert
        """
        if AppAttr.get("project") == None :
            AppAttr.config("widnamelist", [])
            AppAttr.config("widget", None)


    def delWid(self) -> None:
        """delWid 
        Fonction de suppression d'un widget.
        """
        if AppAttr.get("widget") != None :
            WidgetReq.delWidReq()
            self.clear("sets")
            self.actual_sets = []
            AppAttr.config("widget", None)
            AppAttr.config("widget_id", None)
            self.sideWidgetsUptdating()
            self.configActionBt()
            self.codeFrame()
        else :
            messagebox.showinfo("Utilisation impossible", "Suppression impossible, aucun widget n'est ouvert.")

    
    def on_quit(self) -> None:
        """on_quit 
        Détruit la fenêtre lorsque le bouton "Quitter" du menu est pressé
        """
        self.destroy()


    def copyCode(self):
        copy = self.code_output.get("0.0", "end") + "\n\nwindow.mainloop()"
        self.clipboard_clear()
        self.clipboard_append(copy)


    def openPreview(self):
        CodeReq.prepareExe()
        path =  CodeReq.getProjectPath() + "\\" + "code.py"
        subprocess.run(["python", path])
        CodeReq.shutdownExe()


#-------------------- fonctions de création de fenêtres enfant --------------------
    

    def openProjectApp(self, reason) -> None:
        """openProjectApp 
        Fonction d'ouverture de la fenêtre de projets,
        modifie le nom de l'application si un projet est ouvert
        """
        if self.project_app == None :
            self.project_app = ProjectApp(reason)
            self.project_app.grab_set()
            self.project_app.on_destroy()
            if AppAttr.get("project") != None :
                self.title(f"Saturne : {AppAttr.get("project")}")
                ProjectReq.initProjectAttrReq()
                self.sideWidgetsUptdating()
            else :
                self.title("Saturne")
                self.resetAttr()
            self.clear('all')


    def openParameters(self) -> None:
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


    def widgetAdding(self) -> None:
        """widgetAdding 
        Fonction d'ouverture de la fenêtre d'ajout de Widgets
        """
        if self.widgetapp == None :
            self.widgetapp = WidgetApp()
            self.widgetapp.grab_set()
            self.widgetapp = self.widgetapp.on_destroy()
            if AppAttr.get( "widget_id") != None :
                WidgetReq.createWidSetFileReq(AppAttr.get( "widget_id"))
                data = AppAttr.get("widnamelist")[::]
                data.append(AppAttr.get("widget"))
                AppAttr.config("widnamelist", data)

                self.sideWidgetsUptdating()
        else :
            print("fenêtre d'ajout d'un widget déjà ouverte")


if __name__ == "__main__":
    if AppAttr.config( "const") != "Error" :
        app = interface()
        app.mainloop()