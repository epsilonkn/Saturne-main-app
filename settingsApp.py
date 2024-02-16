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
        
        self.parameters = deepcopy(AppAttr.get(AppAttr, "settings"))
        self.color = ct.StringVar()
        self.theme = ct.StringVar()
        self.theme_translation = {"eng-fra" : {"green" : "Vert", "dark-blue" : "Bleu foncé", "blue" : "Bleu", "system" : "Système", "dark" : "Sombre", "light" : "Clair"}, 
                                  "fra-eng" : {"Vert" : "green", "Bleu" : "blue", "Bleu foncé" : "dark-blue", "Système" : "system", "Sombre" : "dark", "Clair" : "light"}}
        

        self.infotabview = ct.CTkTabview(self)
        self.infotabview.grid(padx=10, pady=10, sticky="wsen")

        self.infotabview.add("Affichage")
        self.infotabview.add("Fonctionnement")
        self.infotabview.add("Thème")

        self.bottom_frame = ct.CTkFrame(self)
        self.bottom_frame.grid(row = 1, column = 0, pady = 5)


        self.apply_button = ct.CTkButton(self.bottom_frame, text = "confirmer", font=ct.CTkFont(size=15, weight="bold") , command = lambda : self.applySettings())
        self.return_button = ct.CTkButton(self.bottom_frame, text = "annuler", font=ct.CTkFont(size=15, weight="bold") , command = lambda : self.quitSettings())

        self.return_button.grid(row = 0, column = 0, padx = 10)
        self.apply_button.grid(row = 0, column =1)


        #-------------------- Création de la fenêtre "Affichage" --------------------


        self.affichage_lbl = ct.CTkLabel(self.infotabview.tab("Affichage"), text = "Affichage", font=ct.CTkFont(size= 25, weight="bold"))

        self.sub_res_frame = ct.CTkFrame(self.infotabview.tab("Affichage"))

        self.screen_res_lbl = ct.CTkLabel(self.sub_res_frame, text = "Résolution :", font=ct.CTkFont(size=15, weight="bold"))
        self.pixel_ind_lbl = ct.CTkLabel(self.sub_res_frame, text = "x", font=ct.CTkFont(size=15, weight="bold"))
        self.screen_width = ct.CTkEntry(self.sub_res_frame, width =60)
        self.screen_height = ct.CTkEntry(self.sub_res_frame, width =60)
        
        self.screen_width.insert(0, self.parameters["width"])
        self.screen_height.insert(0, self.parameters["height"])

        self.fullscreenlbl = ct.CTkLabel(self.infotabview.tab("Affichage"), text = "Plein écran", font=ct.CTkFont(size=15, weight="bold"))
        self.fullscreen = ct.CTkSwitch(self.infotabview.tab("Affichage"), text = "", onvalue= 1, offvalue= 0, switch_width= 48, switch_height= 18)
        self.fullscreen.select() if self.parameters["fullscreen"] else None
        self.get_tooltip_lbl = ct.CTkLabel(self.infotabview.tab("Affichage"), text = "Afficher les tooltip :", font=ct.CTkFont(size=15, weight="bold"))
        self.get_tooltip = ct.CTkSegmentedButton(self.infotabview.tab("Affichage"), values = ["Oui", "Non"])
        self.get_tooltip.set(self.parameters["tooltip"])


        self.affichage_lbl.grid(row = 0, column =0, columnspan = 2, pady = 10, sticky = 'w')
        self.sub_res_frame.grid(row = 1, column =0, columnspan = 2, pady = 10, sticky = 'w')

        self.screen_res_lbl.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.screen_width.grid(row = 0, column = 1, padx = 5, pady = 10)
        self.pixel_ind_lbl.grid(row =0, column = 2, pady = 10, sticky = 'w')
        self.screen_height.grid(row = 0, column = 3, padx = 5, pady = 10)

        self.fullscreenlbl.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.fullscreen.grid( row = 2, column = 1, padx = 10, pady = 10, sticky = 'w')

        self.get_tooltip_lbl.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.get_tooltip.grid(row = 3, column = 1, padx = 10, pady = 10, ipadx = 20)


        #-------------------- Création de la fenêtre "Fonctionnement" --------------------


        self.fonc_lbl = ct.CTkLabel(self.infotabview.tab("Fonctionnement"), text = "Fonctionnement", font=ct.CTkFont(size= 25, weight="bold"))

        self.detail_lvl_lbl = ct.CTkLabel(self.infotabview.tab("Fonctionnement"), text = "Niveau de détail :", font=ct.CTkFont(size= 15, weight="bold"))
        self.detail_lvl = ct.CTkOptionMenu(self.infotabview.tab("Fonctionnement"), values = ["Simple", "Normal", "Complet"])
        self.detail_lvl.set(self.parameters["detail"])


        self.fonc_lbl.grid(row = 0, column =0, columnspan = 2, pady = 10, sticky = 'w')

        self.detail_lvl_lbl.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'w')
        self.detail_lvl.grid(row = 1, column = 1, padx = 10, pady = 10)


        #-------------------- Création de la fenêtre "Thème" --------------------

        self.Affichage_frame = ct.CTkFrame(self)

        self.theme_label = ct.CTkLabel(self.infotabview.tab("Thème"), text = "Thème", font=ct.CTkFont(size=25, weight="bold"))

        self.color_theme_change_label = ct.CTkLabel(self.infotabview.tab("Thème"), text = "Couleur :", font=ct.CTkFont(size=15, weight="bold"))
        self.color_theme_change_option = ct.CTkOptionMenu(self.infotabview.tab("Thème"), values = ["Bleu foncé", "Bleu", "Vert"], variable=self.color)
        self.color_theme_change_option.set(self.theme_translation["eng-fra"][self.parameters["color"]])

        self.theme_change_label = ct.CTkLabel(self.infotabview.tab("Thème"), text = "Thème :", font=ct.CTkFont(size=15, weight="bold"))
        self.theme_change_option = ct.CTkOptionMenu(self.infotabview.tab("Thème"), values = ["Système", "Sombre", "Clair"], variable=self.theme)
        self.theme_change_option.set(self.theme_translation["eng-fra"][self.parameters["theme"]])

        
        self.theme_label.grid(row = 0, column = 0, pady = 10, columnspan = 2, sticky="w")

        self.color_theme_change_label.grid(column =0, row = 1, pady =5, padx = 10)
        self.color_theme_change_option.grid(row = 1, column = 1, pady =5, padx = 10)

        self.theme_change_label.grid(row = 2, column = 0, pady = 5)
        self.theme_change_option.grid(row = 2, column = 1, pady = 5)


    #-------------------- Création des fonctions --------------------


    def quitSettings(self):
        on_quit = messagebox.askyesno("Qitter les paramètres", "Voulez-vous quitter les paramètres ?\n(les modifications ne seront pas enregistrées).")
        if on_quit :
            self.destroy()


    def applySettings(self):
        try :
            self.parameters["width"] = int(self.screen_width.get())
            self.parameters["height"] = int(self.screen_height.get())
            self.parameters["fullscreen"] = self.fullscreen.get()
            self.parameters["tooltip"]     = self.get_tooltip.get()
            self.parameters["detail"]      = self.detail_lvl.get()
            self.parameters["color"]       = self.theme_translation["fra-eng"][self.color.get()]
            self.parameters["theme"]       = self.theme_translation["fra-eng"][self.theme.get()] 
            with open("rssDir\wdSettings.json", "w") as file:
                json.dump(self.parameters, file)
            AppAttr.config(AppAttr, "settings", self.parameters)
            file.close()
            self.destroy()
        except :
            messagebox.showerror("Erreur de sauvergarde", "Une erreur est survenue lors de la sauvergarde des données,\nvérifiez les paramètres entrés.")


    def on_destroy(self):
        self.master.wait_window(self)
        return None
    

if __name__ == "__main__" :
    with open ("rssDir\wdSettings.json", "r") as file :
        settings = json.load(file)
    app = AppEditing(settings)
    app.mainloop()