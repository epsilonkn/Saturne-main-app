from typing import Tuple
import customtkinter as ct
from copy import deepcopy
from appattr import *
from tkinter import messagebox
from intermediateLayer import ControlReq



class TextTopLevelWin(ct.CTkToplevel):

    def __init__(self, *args, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.choice = ""
        self.weight = "normal" if AppAttr.get("settings")["int_language"] == 2 else "bold"
        self.language = AppAttr.get("settings")["int_language"]

        self.label = ct.CTkLabel(self, text = AppAttr.get("langdict")["text_label"][self.language], font= ct.CTkFont(family = "arial", size=25, weight=self.weight))
        self.text_input = ct.CTkEntry(self, height= 30, width=250, font= ct.CTkFont(family = "arial", size=12, weight=self.weight))
        try : self.text_input.insert(0, AppAttr.get("widsetlist")[0]["text"])
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

    def __init__(self, *args, values, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
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

        self.bind("<Escape>", self.on_quit)

    
    def delValue(self, cross): #à modifier
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
            self.return_values.append(entry[0].get())
        self.destroy()


    def contentGet(self):
        self.wait_window()
        return self.return_values
    

class CommandTopLevelWin(ct.CTkToplevel):

    def __init__(self, *args, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.weight = "normal" if AppAttr.get("settings")["int_language"] == 2 else "bold"
        self.language = AppAttr.get("settings")["int_language"]

        try : self.choice = AppAttr.get("widsetlist")[0]["command"]
        except : self.choice = ""


        #-------------------------- Tabview --------------------------


        self.infotabview = ct.CTkTabview(self, width = 250, height = 75)
        self.infotabview.grid(row = 0, column = 0,sticky="wsen", columnspan = 2)

        self.infotabview.add(AppAttr.get("langdict")["with_set_label"][self.language])
        self.infotabview.add(AppAttr.get("langdict")["without_set_label"][self.language])

        self.lambda_label = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["with_set_label"][self.language]), text = "comand = lambda : ", 
                                        font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
        
        self.lambda_command_entry = ct.CTkEntry(self.infotabview.tab(AppAttr.get("langdict")["with_set_label"][self.language]), width = 200, height = 30, 
                                                font = ct.CTkFont(family = "arial", size = 15))

        self.lambda_label.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = "w")
        self.lambda_command_entry.grid(row = 0, column = 1, padx = 5, pady = 10, sticky = "w")

        self.default_label = ct.CTkLabel(self.infotabview.tab(AppAttr.get("langdict")["without_set_label"][self.language]), text = "comand = ", 
                                         font = ct.CTkFont(family = "arial", size = 15, weight = self.weight))
        
        self.default_command_entry = ct.CTkEntry(self.infotabview.tab(AppAttr.get("langdict")["without_set_label"][self.language]), width = 200, height = 30, 
                                                 font = ct.CTkFont(family = "arial", size = 15))

        self.default_label.grid(row = 0, column = 0, padx = 5, pady = 10, sticky = "w")
        self.default_command_entry.grid(row = 0, column = 1, padx = 5, pady = 10, sticky = "w")


        #-------------------------- Buttons --------------------------
        

        self.validate_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["content_valid_bt"][self.language], 
                                        font= ct.CTkFont(family = "arial", size=15, weight=self.weight), 
                                        width= 100, command = lambda : self.contentValidation())
        
        self.cancel_bt = ct.CTkButton(self, text = AppAttr.get("langdict")["cancel_btn"][self.language], 
                                      font= ct.CTkFont(family = "arial", size=15, weight=self.weight), 
                                      width= 100, command = lambda : self.on_quit())

        self.validate_bt.grid(row = 1, column =0, padx = 5, pady = 10)
        self.cancel_bt.grid(row = 1, column =1, padx = 5, pady = 10)

        self.bind("<Escape>", self.on_quit)


    def on_quit(self, *event):
        self.destroy()

 
    def contentValidation(self):
        if self.infotabview.get() == AppAttr.get("langdict")["with_set_label"][self.language] :
            if not self.verifyContent(self.lambda_command_entry.get()) :
                return
            self.choice = "lambda : " + self.lambda_command_entry.get() 
        elif self.infotabview.get() == AppAttr.get("langdict")["without_set_label"][self.language] :
            if not self.verifyContent(self.default_command_entry.get()) :
                return
            if "()" in self.default_command_entry.get() : 
                self.choice = "lambda : " + self.default_command_entry.get()
            else : 
                self.choice = self.default_command_entry.get()
        self.destroy()


    def contentGet(self):
        self.wait_window()
        return self.choice
    

    def verifyContent(self, content):
        backslash = False
        parenthesis_count = 0
        simple_quote = 0
        double_quote = 0
        for char in content :
            match char :
                case "(" :
                    parenthesis_count += 1
                case ")" :
                    if parenthesis_count == 0 :
                        messagebox.showwarning("Erreur de commande", "La commande entrée est invalide, veuillez vérifier les parenthèses.")
                        return False
                    else : parenthesis_count -= 1
                case "\"" :
                    if backslash == True :
                        if not simple_quote and not double_quote :
                            messagebox.showwarning("Erreur de commande", "La commande entrée est invalide, veuillez vérifier les guillemets.")
                            return
                        else :
                            backslash = False
                    else :
                        if double_quote == 1 : 
                            double_quote -= 1
                        else : 
                            double_quote += 1
                case "\'" :
                    if backslash == True :
                        if not simple_quote and not double_quote :
                            messagebox.showwarning("Erreur de commande", "La commande entrée est invalide, veuillez vérifier les guillemets.")
                            return
                        else :
                            backslash = False
                    else :
                        if simple_quote  == 1 : 
                            simple_quote -= 1
                        else : 
                            simple_quote += 1
                case "\\":
                    if backslash == False : backslash = True
                    else : backslash = False
        if simple_quote :
            messagebox.showwarning("Erreur de commande", "La commande entrée est invalide, veuillez vérifier les simples guillemets.")
            return False
        if double_quote :
            messagebox.showwarning("Erreur de commande", "La commande entrée est invalide, veuillez vérifier les doubles guillemets.")
            return False
        if parenthesis_count :
            messagebox.showwarning("Erreur de commande", "La commande entrée est invalide, veuillez vérifier les parenthèses.")
            return False
        else :
            return True


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