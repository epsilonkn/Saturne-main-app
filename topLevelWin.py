#file version 0.2.0
from typing import Tuple
import customtkinter as ct
from copy import deepcopy
from appattr import *
from tkinter import messagebox
from intermediateLayer import ControlReq



class TextTopLevelWin(ct.CTkToplevel):

    def __init__(self, text : str = ""):
        super().__init__()

        self.choice = ""
        self.weight = "normal" if AppAttr.get("settings")["int_language"] == 2 else "bold"
        self.language = AppAttr.get("settings")["int_language"]

        self.label = ct.CTkLabel(self, text = AppAttr.get("langdict")["text_label"][self.language], font= ct.CTkFont(family = "arial", size=25, weight=self.weight))
        self.text_input = ct.CTkEntry(self, height= 30, width=250, font= ct.CTkFont(family = "arial", size=12, weight=self.weight))
        try : self.text_input.insert(0, text) if text != "" else AppAttr.get("widsetlist")[0]["text"]
        except : pass
        self.validate_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["content_valid_bt"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 100, command = lambda : self.contentValidation())
        self.cancel_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["cancel_btn"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 100, command = lambda : self.on_quit())


        self.label.grid(row = 0, column =0, columnspan = 2, padx = 10, pady = 10, sticky = "w")
        self.text_input.grid(row = 1, column =0, columnspan = 2, padx = 10, pady = 10)
        self.validate_bt.grid(row = 2, column =0, padx = 10, pady = 10)
        self.cancel_bt.grid(row = 2, column =1, padx = 10, pady = 10)

        self.bind("<Escape>", self.on_quit)


    def on_quit(self, event):
        self.destroy()


    def contentValidation(self):
        self.choice = self.text_input.get()
        self.destroy()
        

    def contentGet(self):
        self.wait_window()
        return self.choice


class ValuesTopLevelWin(ct.CTkToplevel):

    def __init__(self,values):
        super().__init__()
        if values :
            self.values = values
        else :
            try : self.values = deepcopy(AppAttr.get("widsetlist")[0]["values"])
            except : self.values = []

        self.weight = "normal" if AppAttr.get("settings")["int_language"] == 2 else "bold"
        self.language = AppAttr.get("settings")["int_language"]

        self.return_values = []
        self.entries = []
        self.max_row =len(self.values) +1

        self.add_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["add_value_label"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 200, command = lambda : self.addValue())
        self.add_bt.grid(column =0, row = 0, padx = 5, pady = 10, columnspan =2)

        self.validate_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["content_valid_bt"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 65, command = lambda : self.contentValidation())
        self.cancel_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["cancel_btn"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 65, command = lambda : self.on_quit())

        
        if len(self.values) > 0 :
            for i in range(len(self.values)):
                entry = ct.CTkEntry(self, height= 30, width=200, font= ct.CTkFont(family = "arial", size=15, weight=self.weight))
                entry.insert(0, self.values[i])
                cross_bt = ct.CTkButton(self, text = "X", font= ct.CTkFont(family = "arial", size=15, weight=self.weight), text_color="#FC2626", width= 20)
                cross_bt.configure(command= lambda x= cross_bt : self.delValue(x))

                self.entries.append((entry, cross_bt))
                entry.grid(column =0, row = i +1, padx = 5, pady = 5, columnspan =2)
                cross_bt.grid(column = 2, row = i + 1, padx = 5, pady = 5, sticky = "w")

        self.validate_bt.grid(row = self.max_row, column =0, padx = 5, pady = 5)
        self.cancel_bt.grid(row = self.max_row, column =1, padx = 5, pady = 5)

        self.bind("<Escape>", self.on_quit)


    def addValue(self):
        entry = ct.CTkEntry(self, height= 30, width=200, font= ct.CTkFont(family = "arial", size=15, weight=self.weight))
        cross_bt = ct.CTkButton(self, text = "X", font= ct.CTkFont(family = "arial", size=15, weight=self.weight), text_color="#FC2626", width= 20)
        cross_bt.configure(command= lambda x= cross_bt : self.delValue(x))
        
        self.entries.append((entry, cross_bt))
        
        entry.grid(column =0, row = self.max_row, padx = 5, pady = 5, columnspan =2)
        cross_bt.grid(column = 2, row = self.max_row, padx = 5, pady = 5, sticky = "w")
        self.max_row += 1
        self.validate_bt.grid_configure(row = self.max_row)
        self.cancel_bt.grid_configure(row = self.max_row)

    
    def delValue(self, cross):
        for entries in self.entries :
            if entries[1] == cross :
                entries[0].destroy()
                entries[1].destroy()
                del self.entries[self.entries.index(entries)]


    def on_quit(self, event):
        self.destroy()

 
    def contentValidation(self):
        print(self.entries)
        for entry in self.entries :
            val =entry[0].get()
            if val != "" :
                self.return_values.append(val)
        self.destroy()


    def contentGet(self):
        self.wait_window()
        return self.return_values
    

class CommandTopLevelWin(ct.CTkToplevel):

    var_type = ["int", "float", "str", "bool"]

    def __init__(self, values):
        super().__init__()

        self.weight = "normal" if AppAttr.get("settings")["int_language"] == 2 else "bold"
        self.language = AppAttr.get("settings")["int_language"]

        try : 
            if AppAttr.get("widsetlist")[0]["command"] != None :
                self.choice = AppAttr.get("widsetlist")[0]["command"]
            else : self.choice = values
        except : self.choice = values
        self.entries = []


        #-------------------------- Widgets --------------------------

        self.param_frame = ct.CTkFrame(self)
        self.param_frame.grid(row = 1, column= 0, columnspan = 2)


        self.command_label = ct.CTkLabel(self, text = "command = ", 
                                         font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
        
        self.command_entry = ct.CTkEntry(self, width = 200, height = 30, 
                                                 font = ct.CTkFont(family = "arial", size = 15))
        self.command_entry.insert(0, self.choice[0])

        self.command_label.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = "e")
        self.command_entry.grid(row = 0, column = 1, padx = 5, pady = 10, sticky = "w")

        self.add_bt = ct.CTkButton(self.param_frame, text = AppAttr.get("langdict")["add_value_label"][self.language], 
                                   font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 200, command = lambda : self._addValue())
        self.add_bt.grid(column =0, row = 0, padx = 5, pady = 10)

        self.max_row = len(self.choice[1])+1


        if len(self.choice[1]) > 0 :
            i = 1
            for param in self.choice[1].keys():
                frame = ct.CTkFrame(self.param_frame)
                frame.grid(row = i, column = 0) 
                
                param_label = ct.CTkLabel(frame, text = "Parameter name :", 
                                         font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
                param_label.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "w")
                
                param_entry = ct.CTkEntry(frame, height= 30, width=200, font= ct.CTkFont(family = "arial", size=15, weight=self.weight))
                param_entry.insert(0, param)
                param_entry.grid(column = 1, row = 0, padx = 5, pady = 5, sticky = "w")
                
                val_label = ct.CTkLabel(frame, text = "Value :", 
                                         font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
                val_label.grid(column = 2, row = 0, padx = 5, pady = 5, sticky = "w")

                val_type = ct.CTkOptionMenu(frame, values = self.var_type)
                val_type.set(self.choice[1][param][1])
                val_type.grid(column = 3, row = 0, padx = 5, pady = 5, sticky = "w")

                val_entry = ct.CTkEntry(frame, height= 30, width=200, font= ct.CTkFont(family = "arial", size=15, weight=self.weight))
                val_entry.insert(0, self.choice[1][param])
                val_entry.grid(column = 4, row = 0, padx = 5, pady = 5, sticky = "w")
                
                cross_bt = ct.CTkButton(frame, text = "X", font= ct.CTkFont(family = "arial", size=15, weight=self.weight), text_color="#FC2626", width= 20)
                cross_bt.configure(command= lambda x= cross_bt : self._delValue(x))
                cross_bt.grid(column = 5, row = 0, padx = 5, pady = 5, sticky = "w")

                self.entries.append((frame, cross_bt, param_entry, val_entry, val_type))
                i += 1


        #-------------------------- Buttons --------------------------
        

        self.validate_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["content_valid_bt"][self.language], 
                                        font= ct.CTkFont(family = "arial", size=15, weight=self.weight), 
                                        width= 100, command = lambda : self._contentValidation())
        
        self.cancel_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["cancel_btn"][self.language], 
                                      font= ct.CTkFont(family = "arial", size=15, weight=self.weight), 
                                      width= 100, command = lambda : self._on_quit())

        self.validate_bt.grid(row = 2, column =0, padx = 10, pady = 10)
        self.cancel_bt.grid(row = 2, column =1, padx = 10, pady = 10)

        self.bind("<Escape>", self._on_quit)


    def _addValue(self):
        frame = ct.CTkFrame(self.param_frame)
        frame.grid(row = self.max_row, column = 0) 
                
        param_label = ct.CTkLabel(frame, text = "Parameter name :", 
                                    font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
        param_label.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "w")
                
        param_entry = ct.CTkEntry(frame, height= 30, width=200, font= ct.CTkFont(family = "arial", size=15, weight=self.weight))
        param_entry.grid(column = 1, row = 0, padx = 5, pady = 5, sticky = "w")
                
        val_label = ct.CTkLabel(frame, text = "Value :", 
                                         font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
        val_label.grid(column = 2, row = 0, padx = 5, pady = 5, sticky = "w")

        val_type = ct.CTkOptionMenu(frame, values = self.var_type,width=70)
        val_type.grid(column = 3, row = 0, padx = 5, pady = 5, sticky = "w")
                
        val_entry = ct.CTkEntry(frame, height= 30, width=200, font= ct.CTkFont(family = "arial", size=15, weight=self.weight))
        val_entry.grid(column = 4, row = 0, padx = 5, pady = 5, sticky = "w")
                
        cross_bt = ct.CTkButton(frame, text = "X", font= ct.CTkFont(family = "arial", size=15, weight=self.weight), text_color="#FC2626", width= 20)
        cross_bt.configure(command= lambda x= cross_bt : self._delValue(x))
        cross_bt.grid(column = 5, row = 0, padx = 5, pady = 5, sticky = "w")

        self.entries.append((frame, cross_bt, param_entry, val_entry, val_type))
        self.max_row += 1


    def _on_quit(self, *event):
        self.destroy()


    def _delValue(self, cross):
        for entries in self.entries :
            if entries[1] == cross :
                for widgets in entries[0].grid_slaves():
                    widgets.destroy()
                entries[0].destroy()
                del self.entries[self.entries.index(entries)]

 
    def _contentValidation(self):
        dico = {}
        command = self.command_entry.get()
        if not ControlReq.tryWN(command) :
            messagebox.showerror("Command Error", "The function name does not respect the python syntax")
            return
        for entry in self.entries :
            param = entry[2].get()
            val = entry[3].get()
            type_ = entry[4].get()
            if type_ not in self.var_type :
                messagebox.showerror("Command Error", "You must specify the values type")
                return
            if val == "" or param == "" :
                messagebox.showerror("Command Error", "Parameters fields are missings,\nmake sure you filled every field")
                return
            else :
                if type_ == "int" :
                    try : 
                        val = int(val)
                    except :
                        messagebox.showerror("Command Error", "Values don't match the specified type")
                        return
                if type_ == "float" :
                    try :
                        val = float(val)
                    except :
                        messagebox.showerror("Command Error", "Values don't match the specified type")
                        return
                if type_ == "str" :
                    val = val.replace("\"", "\\\"").replace("\'","\\\'")
                if type_ == "bool" :
                    if val not in ("True", "False") :
                        messagebox.showerror("Command Error", "Values don't match the specified type")
                        return
                dico[param] = (val, type_)
        if command == "" and len(dico) > 0 :
            messagebox.showerror("Command Error", "You can't add a nameless function,\nplease add a name to your function before validate")
            return
        self.choice = [command, dico]

        self.destroy()


    def contentGet(self):
        self.wait_window()
        return self.choice
    

class VariableTopLevelWin(ct.CTkToplevel):

    def __init__(self, *args, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.choice = ""
        self.weight = "normal" if AppAttr.get("settings")["int_language"] == 2 else "bold"
        self.language = AppAttr.get("settings")["int_language"]

        self.label = ct.CTkLabel(self, text = AppAttr.get("langdict")["variable_label"][self.language], font= ct.CTkFont(family = "arial", size=25, weight=self.weight))
        self.text_input = ct.CTkEntry(self, height= 30, width=250, font= ct.CTkFont(family = "arial", size=12, weight=self.weight))
        try : self.text_input.insert(0, AppAttr.get("widsetlist")[0]["variable"])
        except : pass
        self.validate_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["content_valid_bt"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 100, command = lambda : self.contentValidation())
        self.cancel_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["cancel_btn"][self.language], font= ct.CTkFont(family = "arial", size=15, weight=self.weight), width= 100, command = lambda : self.on_quit())


        self.label.grid(row = 0, column =0, columnspan = 2, padx = 10, pady = 10, sticky = "w")
        self.text_input.grid(row = 1, column =0, columnspan = 2, padx = 10, pady = 10)
        self.validate_bt.grid(row = 2, column =0, padx = 10, pady = 10)
        self.cancel_bt.grid(row = 2, column =1, padx = 10, pady = 10)

        self.bind("<Escape>", self.on_quit)


    def on_quit(self, event):
        self.destroy()


    def contentValidation(self):
        if ControlReq.tryWN(self.text_input.get()) :
            self.choice = self.text_input.get()
            self.destroy()
        else : 
            messagebox.showerror("Erreur d'entrée", "Le nom de variable ne correspond pas aux attentes de Python")
            return
        

    def contentGet(self):
        self.wait_window()
        return self.choice


if __name__ == "__main__":
    values = ["val1", "val2", "val3"]
    app = CommandTopLevelWin()
    values = app.contentGet()
    print(values)