#programme d'ajout de widget, permet de gagner du temps
from typing import Optional, Tuple, Union
import customtkinter as ct
import json 


class AddWidgetTool(ct.CTk):

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        with open("rssDir\WidParaInfo.json", "r",) as file :
            self.validparameters = json.load(file)
            file.close()
        self.entries = [] 
        
        self.readFile()

        self.upper_frame = ct.CTkFrame(self)
        self.lower_frame = ct.CTkFrame(self) 

        self.upper_frame.grid(row =0, column = 0)    
        self.lower_frame.grid(row = 1, column = 0)  
        
        self.frameCreation()


    def frameCreation(self):
        self.entry_name = ct.CTkEntry(self.upper_frame, width=200)
        self.entry_name.insert(0, 'nom du widget')
        
        self.entry_id = ct.CTkEntry(self.upper_frame, width=200)
        self.entry_id.insert(0, 'id du widget')
        
        self.entry_name.grid(row = 0, column =0, padx= 5)
        self.entry_id.grid (row = 0, column = 1, padx= 5)
        
        self.add_bt = ct.CTkButton(self.upper_frame, text = "valider", command = lambda : self.addWidgetParameter())
        self.add_bt.grid(row =0, column = 3, padx= 5)
        
        row =0
        column =0
        for parameters in self.validparameters.keys():
        
            check = ct.CTkCheckBox(self.lower_frame, text = parameters, command = lambda x = parameters : self.addtoListe(x) )

            check.grid(row = row, column = column, padx= 5, pady = 5)
            
            column = column + 1 if column < 5 else 0
            row += 1 if column == 0 else 0


    def addtoListe(self, add : str):
        if add not in self.entries :
            self.entries.append(add)
            print(add)


    def readFile(self):
        with open("rssDir\widgetInfo.json", "r") as file :
            self.widget_info = json.load(file)
        file.close()


    def addWidgetParameter(self):
        dico = {}
        dico["name"]        = self.entry_name.get()
        dico["id"]          = self.entry_id.get()

        with open("rssDir\widgetRss.json", "r") as file :
            info = json.load(file)
            info.append(dico)
        with open("rssDir\widgetRss.json", "w") as file :
            json.dump(info, file)
        file.close()

        dico["parameters"]  = self.entries
        
        self.widget_info.append(dico)
        self.clear()
        self.frameCreation()
        
        with open("rssDir\widgetInfo.json", "w") as file :
            json.dump(self.widget_info, file)
        file.close()

        self.entries = []
        self.readFile()


    def clear(self):
        liste = self.upper_frame.grid_slaves() + self.lower_frame.grid_slaves()
        for element in liste :
            element.destroy()


if __name__ == "__main__" :
    app = AddWidgetTool()
    app.mainloop()