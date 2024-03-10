#fichier créant le code en python
from appattr import AppAttr


class CodeGeneration():

    str_sets = ["bg_color", "fg_color", "border_color", "text_color", "text_color_disabled",
                 "compound", "anchor", "hover_color", "checkmark_color", "state"
                "button_color", "button_hover_color", "dropdown_fg_color", "dropdown_hover_color"
                "dropdown_text_color", "placeholder_text_color", "background_corner_colors"]
    print("codeGen loaded")


    @classmethod
    def mWinCode(cls, old_data, data):
        code = AppAttr.get("code_list")
        try :
            if data["WinName"] != "" and data["WinName"] != old_data["WinName"] :
                if f"window.title('{old_data["WinName"]}')\n" in code :
                    del code[code.index(f"window.title('{old_data["WinName"]}')\n")]
                code.insert(5, f"window.title('{data["WinName"]}')\n")
        except any as error:
            print(error)
        
        try :
            if data["height"] == "" or data["width"] == "" :
                if f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" in code :
                    del code[code.index(f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n")]
            
            elif data["height"] > 50 and data["width"] > 50 and f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" not in code :
                code.insert(6, f"window.geometry('{data["height"]}x{data["width"]}')\n")
            
            elif f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" in code :
                del code[code.index(f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n")]
                code.insert(6, f"window.geometry('{data["height"]}x{data["width"]}')\n")
        except any as error:
            print(error)
        code.insert(7, "\n")
        AppAttr.config("code_list", code)
    

    @classmethod
    def createWidCode(cls, data : dict) -> list:
        """createWidCode 
        create the code of the widget

        Parameters
        ----------
        data : dict
            list of the widget's settings

        Returns
        -------
        list
            list containing the code widget's initialisation ( element 0 )
            and the widget's layout ( element 1 ) 
        """
        init_seq = data[3]["name"] + " = " + AppAttr.get("widinfo")[data[3]["ID"]]["tkid"]+ "(" + data[3]["master"]
        init_seq += cls._cPC(data)
        init_seq += ')\n'
        layout_seq = cls._cLC(data)
        return [init_seq, layout_seq]
    

    @classmethod
    def _cPC(cls, data) -> str :
        sets_seq = ""
        for keys, values in data[0].items() :
            if keys in ["name", "ID", "layout", "master"]:
                pass
            if  keys == "text" :
                sets_seq += f", {keys} = '{values}'"
            elif values != AppAttr.get("widsets")[keys][0] and keys != "text": 
                if keys == "font" and values != "0":
                    sets_seq += f", {keys} = {cls._cFC(data)}"
                
                elif keys != "font" :
                    if keys in cls.str_sets:
                        sets_seq += f", {keys} = '{values}'"
                    elif keys == "values" :
                        if len(values) > 0 :
                            sub_seq = "["
                            for element in values :
                                sub_seq += f"\"{element}\","
                            sub_seq = sub_seq[:-1] + "]"
                            sets_seq += f", {keys} = {sub_seq}"
                    elif keys == "command" :
                        pass
                    elif keys == "variable" :
                        pass
                    else :
                        sets_seq += f", {keys} = {values}"
        return sets_seq
    

    @classmethod
    def _cFC(cls, data)-> str:
        font = "customtkinter.CTkFont("
        for sets, val in data[1].items():
            if sets in ["family", "weight", "slant"] :
                font += f"{sets} = '{val}' ,"
            else :
                font += f"{sets} = {val} ,"
        font = font[0:-1] + ")"
        return font


    @classmethod
    def _cLC(cls, data) -> str :
        """cLC : create Layout Code
        create the code of the widget's layout

        Returns
        -------
        list
            _description_
        """
        if data[3]["layout"] != None :
            layout_seq = f"{data[3]["name"]}.{data[3]["layout"]}("
            for sets, val in data[2].items():
                if sets in ["sticky", "side", "fill", "anchor"]:
                    layout_seq += f"{sets} = '{val}' ,"
                else : 
                    layout_seq += f"{sets} = {val} ,"
            layout_seq = layout_seq[0:-1] + ")\n" if len(data[2].keys()) > 0 else layout_seq + ")\n"
            return layout_seq
        else : return f"{data[3]["name"]}.pack()"


    @classmethod
    def mWidCode(cls):
        code = AppAttr.get("code_list")
        old_widcode = AppAttr.get("widsetlist")
        new_widcode = cls.createWidCode(data = AppAttr.get("prjtwidsetslist")[AppAttr.get("widget")[1]])
        if old_widcode[3]["initcode"] in code :
            code.insert(code.index(old_widcode[3]["initcode"]), new_widcode[0])
            del code[code.index(old_widcode[3]["initcode"])]
        else :
            code.append(new_widcode[0])

        if old_widcode[3]["layoutcode"] in code :
            code.insert(code.index(old_widcode[3]["layoutcode"]), new_widcode[1])
            del code[code.index(old_widcode[3]["layoutcode"])]
        else :
            code.append(new_widcode[1])

        if AppAttr.get("widget")[0] != AppAttr.get("widget")[1] :
            for lines in code :
                if lines != new_widcode[0] and lines != new_widcode[1] :
                    code[code.index(lines)] = lines.replace(AppAttr.get("widget")[0], AppAttr.get("widget")[1])

        data = AppAttr.get("prjtwidsetslist")
        for  dico in data.values() :
            if dico[3]["master"] == AppAttr.get("widget")[0]:
                dico[3]["master"] = AppAttr.get("widget")[1]
        subdata = data[AppAttr.get("widget")[1]]
        subdata[3]["initcode"] = new_widcode[0]
        subdata[3]["layoutcode"] = new_widcode[1]
        data[AppAttr.get("widget")[1]] = subdata
        AppAttr.config("prjtwidsetslist", data)
        AppAttr.config("widsetlist", subdata)
        AppAttr.config("widget", AppAttr.get("widget")[1])

        if code.index(new_widcode[1]) == len(code) -1 :
            code.append("\n")

        AppAttr.config("code_list", code)


    def delWidCode(cls):
        code = AppAttr.get("code_list")
        for lines in code :
            if AppAttr.get("widsetlist")[3]["initcode"] in lines :
                del code[code.index(lines):code.index(lines)+3]
        AppAttr.config("code_list", code)


if __name__ == "__main__" :
    data = [{"name": "optionmenu1", "ID": "optionmenu", "layout": "pack", "master": "self", "width": 200, "height": 200, "corner_radius": "None", "border_width": "None", "bg_color": "transparent", "fg_color": "None", "border_color": "None", "button_color": "None", "button_hover_color": "None", "dropdown_fg_color": "None", "dropdown_hover_color": "None", "dropdown_text_color": "None", "text_color": "None", "text_color_disabled": "None", "font": "1", "dropdown_font": "None", "values": "None", "state": "normal", "hover": "True", "variable": "None", "command": "None"}, {"family": "Arial", "size": 15, "weight": "bold"}, {"ipadx": 20, "ipady": 10, "anchor": "N", "fill": "X", "side": "BOTTOM"}]
    print(CodeGeneration.createWidCode(cls =CodeGeneration,  data = data))
    # data = {"PrjtName": "nouvtest", "WinName": "inter", "height": 100, "width": 50}
    # old_data = {"PrjtName": "nouvtest", "WinName": "inter", "height": 100, "width": 50}
    # path = fileop.createPath("projet" + "\\" + "code.py")
    # print(path)
    # print(CodeGeneration.mWinCode(CodeGeneration, old_data, data, path))
        