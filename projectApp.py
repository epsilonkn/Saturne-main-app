import customtkinter as ct
from tkinter import messagebox
from intermediateLayer import *
import tool_tip as tl
from appattr import AppAttr


class ProjectApp(ct.CTkToplevel):

    def __init__(self, reason):
        super().__init__()

        self.newprojectname = None
        self.tooltip = AppAttr.get( "settings")["tooltip"]
        self.language = AppAttr.get("settings")["int_language"]

        self.char_weight = "normal" if AppAttr.get("settings")["language"] == "日本語" else "bold"

        self.main_frame = ct.CTkFrame(self)
        self.side_frame = ct.CTkScrollableFrame(self.main_frame, height = 300, width = 180)
        self.work_frame = ct.CTkFrame(self.main_frame, height = 300, width=600)

        self.main_frame.grid()
        self.side_frame.grid(row = 0, column =0)
        self.work_frame.grid(row =0, column = 1)
        
        self.validation = False
        if reason == "new" :
            self.sideFrameUpdating()
            self.workFrameCreation()
        else :
            self.sideFrameUpdating()
            self.modifyFrame(reason) if reason != None else self.workFrameCreation()
        self.eventControl("init")

        


    def workFrameCreation(self, *event):
        self.eventControl("add")
        self.clear("workFrame")
        
        self.project_label = ct.CTkLabel(self.work_frame, text = AppAttr.get("langdict")["project_label"][self.language], width=600)
        self.entry = ct.CTkEntry(self.work_frame, width=200)
        self.content_valid_bt = ct.CTkButton(self.work_frame, text = AppAttr.get("langdict")["content_valid_bt"][self.language], height = 30, width=200, command = lambda : self.addProject())

        self.project_label.grid(row = 0, column = 0, pady = 15)
        self.entry.grid(row = 1, column = 0, pady = 15)
        self.content_valid_bt.grid(row =2, column = 0, pady = 15)


    def modifyFrame(self, project):
        self.eventControl("mod")
        self.clear("workFrame")

        AppAttr.config("project", project)
        dico = self.loadPrjctInfo()
        if dico == False :
            messagebox.showwarning("Error", "An error occured while loading the project's settings.\nSee the logs for more details")


        #-------------------- création des frames -------------------- 


        self.upper_frame = ct.CTkFrame(self.work_frame, corner_radius=0)
        self.lower_frame = ct.CTkFrame(self.work_frame, corner_radius=0)

        self.upper_frame.grid(row = 0, column = 0)
        self.lower_frame.grid(row =1, column = 0)


        #-------------------- création des labels -------------------- 

        self.prjt_name_lbl = ct.CTkLabel(self.upper_frame, text = AppAttr.get("langdict")["prjt_name_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.prjt_name_lbl , "Nom du projet") if self.tooltip == "Oui" else None
        self.win_name_lbl = ct.CTkLabel(self.upper_frame, text = AppAttr.get("langdict")["win_name_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.win_name_lbl , "Nom de la fenêtre") if self.tooltip == "Oui" else None
        self.win_height_lbl = ct.CTkLabel(self.upper_frame, text = AppAttr.get("langdict")["win_height_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.win_height_lbl , "Hauteur de la fenêtre,\n200 par défaut") if self.tooltip == "Oui" else None
        self.win_width_lbl = ct.CTkLabel(self.upper_frame, text = AppAttr.get("langdict")["win_width_lbl"][self.language], font=ct.CTkFont(size=15, weight=self.char_weight))
        tl.CreateToolTip(self.win_width_lbl , "Largeur de la fenêtre,\n200 par défaut.") if self.tooltip == "Oui" else None

        self.prjt_name_lbl.grid(row = 0, column =0, padx = 10, pady = 10)
        self.win_name_lbl.grid(row = 1, column =0, padx = 10, pady = 10)
        self.win_height_lbl.grid(row = 0, column =2, padx = 5, pady = 10)
        self.win_width_lbl.grid(row = 1, column =2, padx = 5, pady = 10)


        #-------------------- création des entrées -------------------- 


        self.prjt_name = ct.CTkEntry(self.upper_frame, width = 100)
        self.prjt_name.insert(0, AppAttr.get("project"))

        self.win_name = ct.CTkEntry(self.upper_frame, width = 100)
        self.win_name.insert(0, dico['WinName'] if dico != False else "")

        self.win_height = ct.CTkEntry(self.upper_frame, width=90)
        self.win_height.insert(0, dico["height"] if dico != False else "")

        self.win_width = ct.CTkEntry(self.upper_frame, width=90)
        self.win_width.insert(0, dico["width"] if dico != False else "")


        self.prjt_name.grid(row = 0, column = 1)
        self.win_name.grid(row = 1, column = 1)
        self.win_height.grid(row = 0, column =3, padx = 5)
        self.win_width.grid(row = 1, column =3, padx = 5, pady = 10)


        #-------------------- création des boutons -------------------- 


        self.del_bt = ct.CTkButton(self.lower_frame, text = AppAttr.get("langdict")["menuwid2"][self.language], height = 30, width=130, command = lambda : self.delProject())
        self.modify_bt = ct.CTkButton(self.lower_frame, text = AppAttr.get("langdict")["menuwid3"][self.language], height = 30, width=130, command = lambda :self.modifyInfo())
        self.open_bt = ct.CTkButton(self.lower_frame, text = AppAttr.get("langdict")["open_bt"][self.language], height = 30, width=130, command = lambda : self.validate())

        self.del_bt.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.modify_bt.grid(row = 0, column = 1, padx = 10, pady = 10)
        self.open_bt.grid(row = 0, column = 2, padx = 10, pady = 10)


        self.work_frame.configure(bg_color = self.upper_frame.cget("bg_color"))


    def loadPrjctInfo(self):
        return  ProjectReq.getPrjtSetRqst()

            

    def modifyInfo(self, *event):
        modify = True
        try : 
            name = self.win_name.get()
        except :
            modify = False
            messagebox.showerror("Mauvais titre de fenêtre.", "Mauvais Titre de fenêtre entré.")
        try : 
            height = self.win_height.get()
            height.replace(" ", "")
            height = int(height) if height != "" else ""
        except :
            modify = False

            messagebox.showerror("Hauteur invalide.", "Hauteur entrée invalide.")
        try : 
            width = self.win_width.get()
            width.replace(" ", "")
            width = int(width) if width != "" else ""
        except :
            modify = False
            messagebox.showerror("Largeur invalide.", "Largeur entrée invalide.")
        try : 
            newname = self.prjt_name.get()
        except :
            modify = False
            messagebox.showerror("Nom de projet invalide.", "Nouveau nom de projet entré invalide.")

        if modify == True :
            dico = {}
            dico["PrjtName"]    = newname
            dico["WinName"]     = name
            dico["height"]      = height
            dico["width"]       = width
            if newname != AppAttr.get("project") :
                rename = ProjectReq.renameDirReq(newname)
                if rename == False :
                    messagebox.showerror("Erreur de sauvergade.", "Une erreur est survenue lors du renommage du projet.")
                    return 0
                else :
                    self.project_info.insert(self.project_info.index(AppAttr.get("project")), newname)
                    del self.project_info[self.project_info.index(AppAttr.get("project"))]
                    converted_info = ",".join(self.project_info)
                    with open("rssDir" +"\\"+  "prjctNameSave.txt", "w", encoding= 'utf8') as file :
                        file.write(converted_info)
                    file.close()
                    AppAttr.config("project", newname )
                    self.clear("sideFrame")
                    self.sideFrameUpdating()
            ProjectReq.modidyPrjctRqst(dico)

    
    def openProjectInfo(self):
        with open("rssDir" +"\\"+  "prjctNameSave.txt", "r", encoding= 'utf8') as file :
            self.project_info = file.read().split(",")
        file.close()


    def sideFrameUpdating(self):
        self.openProjectInfo()
        self.clear("sideFrame")
        self.add_button = ct.CTkButton(self.side_frame, text = AppAttr.get("langdict")["add_project_label"][self.language], width = 160, height = 30, command = lambda : self.workFrameCreation())
        self.add_button.grid(padx = 10, pady = 5)

        for projects in self.project_info:
            if projects != "":
                bt = ct.CTkButton(self.side_frame, text = projects, width = 160, height = 30, command = lambda projects = projects : self.modifyFrame(projects))
                bt.grid(padx = 10, pady = 5)


    def addProject(self, *event):
        AppAttr.config( "project", self.entry.get())
        print(AppAttr.get("project"))
        if AppAttr.get( "project") != "" and type(AppAttr.get( "project")) == str :
            ProjectReq.newPrjctRqst()
        else : return
        self.project_info.append(AppAttr.get( "project"))
        converted_info = ",".join(self.project_info)

        
        with open("rssDir" +"\\"+  "prjctNameSave.txt", "w", encoding= 'utf8') as file :
            file.write(converted_info)
        file.close()
        
        
        self.clear("sideFrame")
        self.clear("workFrame")
        self.sideFrameUpdating()
        self.modifyFrame(AppAttr.get( "project"))


    def delProject(self, *event):
        try : 
            if type(AppAttr.get("project")) == str :
                ProjectReq.rmproject()

            del self.project_info[self.project_info.index(AppAttr.get("project"))]
            converted_info = ",".join(self.project_info)
            
            with open("rssDir" +"\\"+  "prjctNameSave.txt", "w", encoding= 'utf8') as file :
                file.write(converted_info)
            file.close()
            AppAttr.config("project", None)
            
            self.clear("workFrame")
            self.clear("sideFrame")
            self.sideFrameUpdating()
        except :
            messagebox.showerror("Suppression impossible", "Une erreur est survenue lors de la suppresion du projet.")


    def clear(self, choice):
        if choice == "sideFrame":
            liste = self.side_frame.grid_slaves()
        if choice =='workFrame':
            liste = self.work_frame.grid_slaves()
        for widgets in liste :
            widgets.destroy()

    
    def validate(self, *event) -> NoReturn :
        self.validation = True
        self.destroy()


    def on_destroy(self) :
        self.wait_window()
        if self.validation != True :
            AppAttr.config("project", None)

    def eventControl(self, event : str) -> None:
        if event == "add" :
            self.unbind("<Control-o>")
            self.unbind("<Control-s>")
            self.unbind("<Control-w>")
            self.bind("<Control-a>", self.addProject)
        if event == "mod" :
            self.unbind("<Control-a>")
            self.bind("<Control-o>", self.validate)
            self.bind("<Control-s>", self.modifyInfo)
            self.bind("<Control-w>", self.delProject)
        if event == "init" :
            self.bind("<Control-t>", self.workFrameCreation)
            self.bind("<Control-Key-1>", lambda event : self.eventControl(0))
            self.bind("<Control-Key-2>", lambda event : self.eventControl(1))
            self.bind("<Control-Key-3>", lambda event : self.eventControl(2))
            self.bind("<Control-Key-4>", lambda event : self.eventControl(3))
            self.bind("<Control-Key-5>", lambda event : self.eventControl(4))
            self.bind("<Control-Key-6>", lambda event : self.eventControl(5))
            self.bind("<Control-Key-7>", lambda event : self.eventControl(6))
            self.bind("<Control-Key-8>", lambda event : self.eventControl(7))
            self.bind("<Control-Key-9>", lambda event : self.eventControl(8))
        if type(event) == int :
            if event >= len(self.project_info):
                pass
            else : 
                self.modifyFrame(self.project_info[event])

  

if __name__ == "__main__" :
    if AppAttr.config( "const") != "Error" :
        testapp = ProjectApp("new")
        testapp.mainloop()