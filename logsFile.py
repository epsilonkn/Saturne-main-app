import datetime
import os



class Logs():

    error_level = {"FileExistsError" : "Critical", "FileNotFoundError" : "Critical", "KeyError" : "Issue", "NameError" : "Issue", "TypeError" : "Issue", "SyntaxError" : "Issue", 
                   "ModuleNotFoundError" : "critical", "UnicodeTranslateError" : "Issue", "ValueError" : "Issue", "AttributeError" : "Critical", "JSONDecodeError" : "Critical",
                   "Exception" : "Undefined", "UnboundLocalError" : "Critical", "TclError" : "Critical"}

    def __init__(self) -> None:
    
        self.log = f"\n{datetime.datetime.now()} | New session started\n\n"

    def addToLogs(self, message, data, *code) :
        if code :
            data.replace("\\n", "\\n ")
        else :
            data = str(data)
            for i in range(0, len(data), 175):
                if i ==0 :
                    pass
                else :
                    data = data[:i] + "\n " + data[i:]
        self.log += f"\n {datetime.datetime.now()} | {message} : {data}\n" 



    def save(self):
        self.log += "\n session closed\n"
        path = os.getcwd() + "\\" + "rssDir" + "\\" + "logs.txt"
        try :
            with open(path, "a", encoding="utf8") as file :
                file.write(self.log)
        except :
            with open(path, "w", encoding="utf8") as file :
                file.write(self.log)
            print("logs file inexisting or corrupted")


    def getErrorLevel(self, error):
        path = os.getcwd() + "\\" + "rssDir" + "\\" + "logs.txt"
        with open(path, "a", encoding="utf8") as file :
                file.write(f"\n{datetime.datetime.now()}")
        file.close()
        return self.error_level[error]