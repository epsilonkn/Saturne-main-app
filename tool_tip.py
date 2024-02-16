# ToolTip widget based on this code : https://stackoverflow.com/a/56749167
# Was modified to correspond to the color theme of our program.

import json
from tkinter import *
from customtkinter import *

class ToolTip(object):


    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.settings = self.loadsets()
        set_default_color_theme(self.settings["color"])
        set_appearance_mode(self.settings["theme"])

    def showtip(self, text):
        """
        Displays text in tooltip window
        """
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() +20
        self.tipwindow = tw = CTkToplevel(self.widget, highlightthickness=1, borderwidth = 2)
        tw.wm_overrideredirect(1)
        tw.attributes("-topmost", True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = CTkLabel(tw, text=self.text, justify=LEFT, height = 15,
                      font=CTkFont(family = "Arial",size = 11,weight= "bold"))
        label.pack(ipadx=5)


    def hidetip(self):
        """
        Destroys the window ToolTip when the mouse's cursor is moved out of the object
        """
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


    def loadsets(self):
        """loadsets 
        Function created for the sake of the saturn application,
        load the settings of the application tu get the current theme settings

        Returns
        -------
        _type_ : dict
            return the settings of the interfaces
        """
        with open("rssDir" + "\\" + "wdSettings.json") as file :
            return json.load(file)


def CreateToolTip(widget, text):
    """
    Creates a ToolTip when the mouse's cursor is on the object where the ToolTip is a assigned

    Parameters
    ----------
    widget : object
        define the object where the ToolTip is assigned
    text : str
       text which appear with the ToolTip
    """
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)