from typing import Tuple
import os
import json
import customtkinter as ct
from tkinter import messagebox

class AdminApp(ct.CTk):

    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.open_logs_bt = ct.CTkButton(self, text = "Open Logs", width = 100, command = AdminApp.viewLogs)
        self.open_logs_bt.grid(row = 0, column = 0, padx = 10, pady = 10)
        
        self.reset_log_bt = ct.CTkButton(self, text = "Reset Logs", width = 100, command = AdminApp.resetLogs)
        self.reset_log_bt.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.verify_files_bt = ct.CTkButton(self, text = "Verify Files", width = 100, command = AdminApp.verifyFiles)
        self.verify_files_bt.grid(row = 2, column = 0, padx = 10, pady = 10)


    @staticmethod
    def resetLogs():
        with open("rssDir" + "\\" + "logs.txt", "w", encoding="utf8") as log :
            log.write("")


    @staticmethod
    def viewLogs():
        os.system("rssDir" + "\\" + "logs.txt")


    @staticmethod
    def verifyFiles():
        missing_f = []
        corrupt_f = []
        module_list = ['addWidgetTool.py', 'Admin.py', 'appattr.py', 'codeGen.py', 'fileManagemt.py', 'fileOpening.py', 
                       'intermediateLayer.py', 'logsFile.py', 'main.py', 'projectApp.py', 'settingsApp.py',  
                       'tool_tip.py', 'topLevelWin.py', 'widgetApp.py']
        log_report = ""
        path = os.getcwd()
        cfiles = os.listdir(path)
        try : del cfiles[cfiles.index(".git")]
        except : pass
        try : del cfiles[cfiles.index(".__pycache__")]
        except : pass
        for files in module_list :
            if files not in cfiles :
                missing_f.append(files)
                del cfiles[cfiles.index(files)]
                log_report += f"\n {files} : missing"
            else :
                del cfiles[cfiles.index(files)]
                log_report += f"\n {files} : ok"
        if "rssDir" not in cfiles :
            missing_f.append("directory rssDir")
            del cfiles[cfiles.index("rssDir")]
            log_report += "\n directory rssDir : missing"
        else :
            del cfiles[cfiles.index("rssDir")]
            log_report += "\n\n directory rssDir : ok\n ressources Files :"
            scfiles =os.listdir(path + "\\" + "rssDir")
            rss_f = ["logs.txt", "languageDict.json","tk_family.txt", 'prjctNameSave.txt', "wdSettings.json", "widgetInfo.json",
                    "widgetRss.json",  "widParaInfo.json"]
            
            for files in rss_f :
                if files not in scfiles :
                    missing_f.append(files)
                    del scfiles[scfiles.index(files)]
                    log_report += f"\n {files} : missing"
                else :
                    if files == "tk_family.txt" :
                        with open(os.getcwd() + "\\" + "rssDir" + "\\" + files, "r", encoding="utf8") as file :
                                    fdata = file.readlines()
                        if len(fdata) != 419 :
                            corrupt_f.append(files)
                            log_report += f"\n {files} : corrupted\n ---> fonts are missings "
                        else :
                            log_report += f"\n {files} : ok"
                    if files == 'prjctNameSave.txt' :
                        fdata = open(os.getcwd() + "\\" + "rssDir" + "\\" + files, "r", encoding="utf8").read().split(",")
                        if len(fdata) > len(cfiles) :
                            log_report += f"\n {files} : corrupted\n ---> projects in the file does not exists in the app "
                        if len(fdata) > len(cfiles) :
                            log_report += f"\n {files} : corrupted\n ---> projects in the app does not exists in the file "
                    else :
                        log_report += f"\n {files} : ok"
        project_f = ["code.py", "prjtset.json", "widgetlist.json", "widNmeList.txt"]
        for dir in cfiles :
            if dir in fdata :
                log_report += f"\nproject {dir} : ok\n files :"
                scfiles =os.listdir(path + "\\" + dir)
                for sfiles in project_f :
                    if sfiles not in scfiles :
                        missing_f.append(dir +" : "+sfiles)
                        log_report += f"\n {sfiles} : missing"
                    else :
                        if sfiles == "widgetlist.json" :
                            with open(os.getcwd() + "\\" + dir + "\\" + sfiles, "r", encoding="utf8") as file :
                                widgetlist = json.load(file)
                        if sfiles == "widNmeList.txt" :
                            with open(os.getcwd() + "\\" + dir + "\\" + sfiles, "r", encoding="utf8") as file :
                                widnmeList = file.read().split(",")
                                if len(widnmeList) > 1 and widnmeList[0] == "" :
                                    del widnmeList[0]
                        log_report += f"\n {sfiles} : ok"
                try :
                    if len( widgetlist) > len(widnmeList):
                        log_report += "\n Error : widgets exists in widgetlist.json but not in widNmelist.txt "
                    elif len( widgetlist) < len(widnmeList):
                        log_report += "\n Error : widgets exists in widNmelist.txt but not in widgetlist.json "
                except :
                    pass
            else :      
                log_report += f"\n {dir} is not accessible"
        
        
        if "logs.txt" not in missing_f :
            with open("rssDir" + "\\" + "logs.txt", "a", encoding="utf8") as log :
                log.write("\n------------ file verify start ------------\n"+log_report + "\n\n------------ file verify end ------------\n")
        else :
            with open("rssDir" + "\\" + "logs.txt", "w", encoding="utf8") as log :
                log.write("\n------------ file verify start ------------\n"+log_report + "\n\n------------ file verify end ------------\n")
        if len(missing_f) ==0 and len(corrupt_f) == 0 :
            messagebox.showinfo("Files verified", "files verified, no error detected.\nSee logs for more details")
        else :
            messagebox.showwarning("Files verified", f"error detected in the files.\nSee logs for more details")


if __name__ == "__main__" :
    app = AdminApp()
    app.mainloop()
