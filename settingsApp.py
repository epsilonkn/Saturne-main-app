#fichier pour l'interface de paramètres

from typing import Optional, Tuple, Union
from copy import deepcopy
import customtkinter as ct 
import json
from tkinter import messagebox
from appattr import AppAttr

class AppEditing(ct.CTkToplevel):

    def __init__(self):
        super().__init__()
        
        self.parameters = deepcopy(AppAttr.get( "settings"))
        self.color = ct.StringVar()
        self.theme = ct.StringVar()
        self.theme_translation = {"eng-fra" : {"green" : "Vert", "dark-blue" : "Bleu foncé", "blue" : "Bleu", "system" : "Système", "dark" : "Sombre", "light" : "Clair"}, 
                                  "fra-eng" : {"Vert" : "green", "Bleu" : "blue", "Bleu foncé" : "dark-blue", "Système" : "system", "Sombre" : "dark", "Clair" : "light"}}
        self.language_dict = {"Français" : 1, "English" : 0, "日本語" : 2}
        self.language = self.parameters["int_language"]

        self.char_weight = "normal" if self.parameters["language"] == "日本語" else "bold"
        self.protocol("WM_DELETE_WINDOW", self.quitSettings)
        

        self.infotabview = ct.CTkTabview(self)
        self.infotabview.grid(padx=10, pady=10, sticky="wsen")

        self.infotabview.add(AppAttr.get("langdict")["display_tab"][self.language])
        self.infotabview.add(AppAttr.get("langdict")["operation_tab"][self.language]) 
        self.infotabview.add(AppAttr.get("langdict")["theme_tab"][self.language])

        self.bottom_frame = ct.CTkFrame(self)
        self.bottom_frame.grid(row = 1, column = 0, pady = 5)


        self.apply_button = ct.CTkButton(self.bottom_frame, text = AppAttr.get("langdict")["confirm_btn"][self.language], font=ct.CTkFont(size=20, weight=self.char_weight) , command = lambda : self.applySettings())
        self.return_button = ct.CTkButton(self.bottom_frame, text = AppAttr.get("langdict")["cancel_btn"][self.language], font=ct.CTkFont(size=20, weight=self.char_weight) , command = lambda : self.quitSettings())

        self.return_button.grid(row = 0, column = 0, padx = 10)
        self.apply_button.grid(row = 0, column =1)


        #-------------------- Création de la fenêtre "Affichage" --------------------


        self.affichage_lbl = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["display_tab"][self.language]), text = AppAttr.get("langdict")["display_tab"][self.language], font=ct.CTkFont(size= 25, weight=self.char_weight))

        self.sub_res_frame = ct.CTkFrame(self.infotabview.tab(AppAttr.get("langdict")["display_tab"][self.language]))

        self.screen_res_lbl = ct.CTkLabel(self.sub_res_frame, text = AppAttr.get("langdict")["resolution_label"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        self.pixel_ind_lbl = ct.CTkLabel(self.sub_res_frame, text = "x", font=ct.CTkFont(size=15, weight=self.char_weight))
        self.screen_width = ct.CTkEntry(self.sub_res_frame, width =60)
        self.screen_height = ct.CTkEntry(self.sub_res_frame, width =60)
        

        self.fullscreenlbl = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["display_tab"][self.language]), 
                                         text = AppAttr.get("langdict")["fullscreen_label"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        
        self.fullscreen = ct.CTkSwitch(self.infotabview.tab(AppAttr.get("langdict")["display_tab"][self.language]), 
                                       text = "", onvalue= 1, offvalue= 0, switch_width= 48, switch_height= 18)

        self.get_tooltip_lbl = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["display_tab"][self.language]), 
                                           text = AppAttr.get("langdict")["tooltip_label"][self.language], 
                                           font=ct.CTkFont(size=15, weight=self.char_weight))
        
        self.get_tooltip = ct.CTkSegmentedButton(self.infotabview.tab(AppAttr.get("langdict")["display_tab"][self.language]), 
                                                 values = [AppAttr.get("langdict")["yes_option"][self.language], 
                                                           AppAttr.get("langdict")["no_option"][self.language]])


        self.affichage_lbl.grid(row = 0, column =0, columnspan = 2, pady = 10, sticky = 'w')
        self.sub_res_frame.grid(row = 1, column =0, columnspan = 2, pady = 10, sticky = 'w')

        self.screen_res_lbl.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.screen_width.grid(row = 0, column = 1, padx = 5, pady = 10)
        self.pixel_ind_lbl.grid(row =0, column = 2, pady = 10, sticky = 'w')
        self.screen_height.grid(row = 0, column = 3, padx = 5, pady = 10)

        self.fullscreenlbl.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.fullscreen.grid( row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')

        self.get_tooltip_lbl.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.get_tooltip.grid(row = 3, column = 1, padx = 10, pady = 10, ipadx = 15)


        #-------------------- Création de la fenêtre "Fonctionnement" --------------------


        self.fonc_lbl = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["operation_tab"][self.language]), 
                                    text = AppAttr.get("langdict")["operation_tab"][self.language], 
                                    font=ct.CTkFont(size= 25, weight=self.char_weight))

        self.detail_lvl_lbl = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["operation_tab"][self.language]), text = AppAttr.get("langdict")["detail_level_label"][self.language], font=ct.CTkFont(size= 15, weight=self.char_weight))
        self.detail_lvl = ct.CTkOptionMenu(self.infotabview.tab(AppAttr.get("langdict")["operation_tab"][self.language]), values = [AppAttr.get("langdict")["simple_option"][self.language], 
                                                                                                              AppAttr.get("langdict")["normal_option"][self.language], 
                                                                                                              AppAttr.get("langdict")["full_option"][self.language]])


        self.language_lbl = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["operation_tab"][self.language]), text = AppAttr.get("langdict")["language_label"][self.language], font=ct.CTkFont(size= 15, weight=self.char_weight))
        self.language_choice = ct.CTkOptionMenu(self.infotabview.tab(AppAttr.get("langdict")["operation_tab"][self.language]), values = ["Français", "English", "日本語"])
        

        self.fonc_lbl.grid(row = 0, column =0, columnspan = 2, pady = 10, sticky = 'w')

        self.detail_lvl_lbl.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.detail_lvl.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.language_lbl.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.language_choice.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')


        #-------------------- Création de la fenêtre "Thème" --------------------

        self.Affichage_frame = ct.CTkFrame(self)

        self.theme_label = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["theme_tab"][self.language]), text = AppAttr.get("langdict")["theme_tab"][self.language], font=ct.CTkFont(size=25, weight=self.char_weight))

        self.color_theme_change_label = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["theme_tab"][self.language]), text = AppAttr.get("langdict")["color_label"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        self.color_theme_change_option = ct.CTkOptionMenu(self.infotabview.tab(AppAttr.get("langdict")["theme_tab"][self.language]), variable=self.color, values = 
                                                          [AppAttr.get("langdict")["dark_blue_option"][self.language],
                                                          AppAttr.get("langdict")["blue_option"][self.language],
                                                          AppAttr.get("langdict")["green_option"][self.language]])
        

        self.theme_change_label = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["theme_tab"][self.language]), text = AppAttr.get("langdict")["theme_label"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        self.theme_change_option = ct.CTkOptionMenu(self.infotabview.tab(AppAttr.get("langdict")["theme_tab"][self.language]), variable=self.theme, values = 
                                                    [AppAttr.get("langdict")["system_theme_option"][self.language],
                                                    AppAttr.get("langdict")["dark_theme_option"][self.language],
                                                    AppAttr.get("langdict")["light_theme_option"][self.language]])

        
        self.theme_label.grid(row = 0, column = 0, pady = 10, columnspan = 2, sticky="w")

        self.color_theme_change_label.grid(column =0, row = 1, pady =5, padx = 10)
        self.color_theme_change_option.grid(row = 1, column = 1, pady =5, padx = 10)

        self.theme_change_label.grid(row = 2, column = 0, pady = 5)
        self.theme_change_option.grid(row = 2, column = 1, pady = 5)


        self.screen_width.insert(0, self.parameters["width"])
        self.screen_height.insert(0, self.parameters["height"])
        self.fullscreen.select() if self.parameters["fullscreen"] else None
        self.fullscreen.select() if self.parameters["fullscreen"] else None
        self.language_choice.set(self.parameters["language"])
       
        match self.parameters["detail"] :
            case "Simple" :
                self.detail_lvl.set(AppAttr.get("langdict")["simple_option"][self.language]) 
            case "Normal" :
                self.detail_lvl.set(AppAttr.get("langdict")["normal_option"][self.language]) 
            case "Complet" :
                self.detail_lvl.set(AppAttr.get("langdict")["full_option"][self.language]) 
        
        match self.parameters["color"] :
            case "dark-blue" :
                self.color_theme_change_option.set(AppAttr.get("langdict")["dark_blue_option"][self.language])
            case "blue" :
                self.color_theme_change_option.set(AppAttr.get("langdict")["blue_option"][self.language])
            case "green" :
                self.color_theme_change_option.set(AppAttr.get("langdict")["green_option"][self.language])

        match self.parameters["theme"] :
            case "system" :
                self.theme_change_option.set(AppAttr.get("langdict")["system_theme_option"][self.language])
            case "dark" :
                self.theme_change_option.set(AppAttr.get("langdict")["dark_theme_option"][self.language])
            case "light" :
                self.theme_change_option.set(AppAttr.get("langdict")["light_theme_option"][self.language])



    #-------------------- Création des fonctions --------------------


    def quitSettings(self):
        on_quit = messagebox.askyesno("Qitter les paramètres", "Voulez-vous quitter les paramètres ?\n(les modifications ne seront pas enregistrées).")
        if on_quit :
            self.destroy()


    def applySettings(self):
        try :
            self.parameters["width"] = int(self.screen_width.get())
        except any as error :
            print(error)
            messagebox.showerror("Erreur de sauvergarde", "Mauvaise largeur de fenêtre entrée.")
            return
            
        try :
            self.parameters["height"] = int(self.screen_height.get())
        except any as error :
            print(error)
            messagebox.showerror("Erreur de sauvergarde", "Mauvaise hauteur de fenêtre entrée.")
            return
        try :
            self.parameters["fullscreen"] = self.fullscreen.get()
        except any as error :
            print(error)
            messagebox.showwarning("Erreur de sauvergarde", "Une erreur est survenue le l'enregistrement du plein écran.")
            return
        
        try :
            if self.get_tooltip.get() in ["yes","Oui", "はい"] :
                self.parameters["tooltip"] = "Oui" 
            elif self.get_tooltip.get() in ["No","Non", "いいえ"] :
                self.parameters["tooltip"] = "Non" 
        except any as error :
            print(error)
            messagebox.showwarning("Erreur de sauvergarde", "Une erreur est survenue lors de la sauvergarde de l'affichage des tooltip.")
            return

        try :
            if self.detail_lvl.get() in ["Simple","Simple", "シンプル"]:
                self.parameters["detail"] = "Simple"
            elif self.detail_lvl.get() in ["Normal","Normal", "普通"]:
                self.parameters["detail"] = "Normal"
            elif self.detail_lvl.get() in ["Full","Complet", "フル"]:
                self.parameters["detail"] = "Complet"
        except any as error :
            print(error)
            messagebox.showwarning("Erreur de sauvergarde", "Une erreur est survenue lors de la sauvergarde du niveau de détail.")
            return

        try :
            if self.color.get() in ["Dark Blue","Bleu foncé", "濃い青"]:
                self.parameters["color"] = "dark-blue"
            elif self.color.get() in ["Blue","Bleu", "青"] :
                self.parameters["color"] = "blue"
            elif self.color.get() in ["Green","Vert", "緑"] :
                self.parameters["color"] = "green"
        except any as error :
            print(error)
            messagebox.showwarning("Erreur de sauvergarde", "Une erreur est survenue lors de la sauvergarde de la couleur de thème.")
            return

        try :
            if self.theme.get() in ["System","Système", "システム"]:
                self.parameters["theme"] = "system"
            elif self.theme.get() in ["Dark","Sombre", "暗い"]:
                self.parameters["theme"] = "dark"
            elif self.theme.get() in ["Light","Clair", "明るい"]:
                self.parameters["theme"] = "light"
        except any as error :
            print(error)
            messagebox.showwarning("Erreur de sauvergarde", "Une erreur est survenue lors de la sauvergarde du thème.")
            return

        self.parameters["language"]     = self.language_choice.get()
        self.parameters["int_language"] = self.language_dict[self.language_choice.get()]
        with open("rssDir"+"\\"+"wdSettings.json", "w", encoding="utf8") as file:
            json.dump(self.parameters, file)
        AppAttr.config( "settings", self.parameters)
        AppAttr.config("language", self.language_dict[self.language_choice.get()])
        file.close()
        self.destroy()


    def on_destroy(self):
        self.master.wait_window(self)
        return None
    

if __name__ == "__main__" :
    if AppAttr.config( "const") != "Error" :
        app = AppEditing()
        app.mainloop()