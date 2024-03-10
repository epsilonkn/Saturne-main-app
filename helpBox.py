from typing import Tuple
import customtkinter as ct
from appattr import *

class HelpBox(object):

    def __init__(self):
        self.language = AppAttr.get("settings")["int_language"]
        self.char_weight = "normal" if self.language == 2 else "bold"
        self.app = None
        self.slider_dict = {"width" : (75, 200), "height" : (20,60), "corner_radius" : (0,15), "border_width" : (0, 10), 
                            "checkbox_height" : (15,40), "checkbox_width" : (15,40), "border_spacing" : (0,10), "wraplength" : (0,100) }
        

    def personalize(self, **kwargs) -> None :
        try :
            try : preview = kwargs["preview"]
            except : preview = False
            self.app = win = ct.CTkToplevel( highlightthickness=1, borderwidth = 2)
            win.bind("<Escape>", self.kill)
            win.wm_overrideredirect(1)
            win.attributes("-topmost", True)
            win.focus()
            #test
            screen_width = win.winfo_screenwidth()
            screen_height = win.winfo_screenheight()

            x_cordinate = int((screen_width/2)-250)
            y_cordinate = int((screen_height/2)-100)

            win.wm_geometry("+%d+%d" % (x_cordinate, y_cordinate))


            text_frame = ct.CTkFrame(win)
            text_frame.grid(row = 0, column = 0)

            text_label = ct.CTkLabel(text_frame, text = "help_text", font = ct.CTkFont(family = "Arial", size = 16, weight = self.char_weight), justify = "left")
            text_label.grid(row = 0, column = 0, padx = 20, pady = 15)

            text =  AppAttr.get("langdict")[f"{kwargs["parameter"]}_helptxt"][self.language] 
            text_label.configure(text = text) if text != "" else None

            if preview == True  :
                match AppAttr.get("widget_id"):
                    case "bt" :
                        exemple = ct.CTkButton(win, text = "Exemple")
                    case "label" :
                        exemple = ct.CTkLabel(win, text = "Exemple")
                    case "optionmenu" :
                        exemple = ct.CTkOptionMenu(win, values = ["exemple 1", "exemple 2", "exmple 3"])
                    case "checkbox" :
                        exemple = ct.CTkCheckBox(win, text = "Checkbox exemple")
                    case "entry" :
                        exemple = ct.CTkEntry(win)
                print(kwargs["parameter"])
                if kwargs["parameter"] in ["state" , "compound", "anchor"]:
                    test_element = ct.CTkOptionMenu(text_frame, values = AppAttr.get("widsets")[kwargs["parameter"]][3],
                                                    command = lambda x : self.exempleUpdate(exemple, test_element.get(), kwargs["parameter"]))
                    test_element.set(exemple.cget(kwargs["parameter"]))
                elif kwargs["parameter"] in ("hover", "font"):
                    test_element = ct.CTkSwitch(text_frame, text = "", onvalue =1, offvalue= 0,switch_width = 48,
                                                command = lambda : self.exempleUpdate(exemple, test_element.get(), kwargs["parameter"]))
                    test_element.select() if kwargs["parameter"] == "hover" else None
                else : 
                    test_element = ct.CTkSlider(text_frame, from_ = self.slider_dict[kwargs["parameter"]][0], 
                                                to = self.slider_dict[kwargs["parameter"]][1],
                                                command = lambda x : self.exempleUpdate(exemple, test_element.get(), kwargs["parameter"]))
                    test_element.set(exemple.cget(kwargs["parameter"]))
                print(exemple.cget(kwargs["parameter"]))
                
                test_element.grid(row = 1, column = 0, padx = 20, pady = 15)
                exemple.grid( row = 0, column = 1, padx = 20)

        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)


    def exempleUpdate(self, widget, val, param):
        try :
            match param :
                case "width" :
                    widget.configure(width = val)
                case "height" :
                    widget.configure(height = val)
                case "corner_radius" :
                    widget.configure(corner_radius = val)
                case "border_width" :
                    widget.configure(border_width = val)
                case "state" :
                    widget.configure(state = val)
                case "checkbox_height" :
                    widget.configure(checkbox_height = val)
                case "checkbox_width" :
                    widget.configure(checkbox_width = val)
                case "border_spacing" :
                    widget.configure(border_spacing = val)
                case "wraplength" :
                    widget.configure(wraplength = val)
                case "compound" :
                    widget.configure(compound = val)
                case "anchor" :
                    widget.configure(anchor = val)
                case "font" :
                    if val == 1 :
                        widget.configure(font = ct.CTkFont(family = "Arial", size = 16, weight= "bold"))
                    else :
                        widget.configure(font = ct.CTkFont(family = None, size = None, weight= "normal"))
                case "hover":
                    if val == 1 :
                        widget.configure(hover = True)
                    else :
                        widget.configure(hover = False)
        except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n")
                traceback.print_exc(file = log)

    
    def kill(self, *event):
        win = self.app
        self.app = None
        if win :    
            win.destroy()


def createHelpBox(**kwargs):
    try :
        if "widget" not in kwargs.keys() or "parameter" not in kwargs.keys() :
            raise AttributeError
        helpbox = HelpBox()
        def create(*event):
            helpbox.personalize(**kwargs)
        kwargs["widget"].bind("<Button-1>", create)
    except Exception as error:
            error_level = AppAttr.getErrorlevel(error)
            if error == AttributeError : error_msg = "Attributes are missing or invalides\n"
            else : error_msg =""
            with open("rssDir"+ "\\" +"logs.txt", "a", encoding= 'utf8') as log:
                log.write(f"\n An error Occured | level : {error_level}\n{error_msg}")
                traceback.print_exc(file = log)
    


#for debuging and visualization purposes
if __name__ == "__main__" :
    AppAttr.config("const")
    AppAttr.config("widget_id", "label") #modify here the type of widget
    
    #we create the main window
    window = ct.CTk()
    label = ct.CTkLabel(window, text = 'click here')
    label.pack(padx = 10 ,pady = 10 )
    createHelpBox(widget = label, parameter = "anchor", preview = True)#modify here the type of parameter 
    #                                                                 ( make sure to choose a valid parameter for the widget chose)
    window.mainloop()