#fichier créant le code en python
import fileOpening as fileop
from appattr import AppAttr

class CodeGeneration(AppAttr):

    str_sets = ["bg_color", "fg_color", "border_color", "text_color", "text_color_disabled",
                 "compound", "anchor", "hover_color", "checkmark_color", "state"
                "button_color", "button_hover_color", "dropdown_fg_color", "dropdown_hover_color"
                "dropdown_text_color", "placeholder_text_color", "background_corner_colors"]
    print("codeGen loaded")


    def mWinCode(cls, old_data, data, project_path):
        code_dico = fileop.loadInfo(project_path, data = "prjtCodeList")
        try :
            if data["WinName"] != "" and data["WinName"] != old_data["WinName"] and f"window.title('{old_data["WinName"]}')\n" not in code_dico :
                code_dico.insert(5, f"window.title('{data["WinName"]}')\n")
            elif f"window.title('{old_data["WinName"]}')\n" in code_dico :
                del code_dico[code_dico.index(f"window.title('{old_data["WinName"]}')\n")]
                code_dico.insert(5, f"window.title('{data["WinName"]}')\n")
        except :
            pass
        
        try :
            if data["height"] == "" or data["width"] == "" :
                if f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" :
                    del code_dico[code_dico.index(f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n")]
            elif data["height"] > 50 and data["width"] > 50 and f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" not in code_dico :
                code_dico.insert(6, f"window.geometry('{data["height"]}x{data["width"]}')\n")
            elif f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n" in code_dico :
                del code_dico[code_dico.index(f"window.geometry('{old_data["height"]}x{old_data["width"]}')\n")]
                code_dico.insert(6, f"window.geometry('{data["height"]}x{data["width"]}')\n")
        except :
            pass
        code_dico.insert(7, "\n")
        return code_dico
    
    def createWidCode(cls, data : dict):
        init_seq = data[0]["name"] + " = " + AppAttr.get(AppAttr,"widinfo")[data[0]["ID"]]["tkid"]+ "(" + data[0]["master"]
        for keys, values in data[0].items() :
            if keys in ["name", "ID", "layout", "master"]:
                pass
            elif keys == "text" :
                init_seq += f", {keys} = '{values}'"
            elif values != AppAttr.get(AppAttr,"widsets")[keys][0] and keys != "text": 
                if keys == "font" and values != "0":
                    font = "customtkinter.CTkFont("
                    for sets, val in data[1].items():
                        if sets in ["family", "weight", "slant"] :
                            font += f"{sets} = '{val}' ,"
                        else :
                            font += f"{sets} = {val} ,"
                    font = font[0:-1] + ")"
                    init_seq += f", {keys} = {font}"
                
                elif keys != "font" :
                    if keys in cls.str_sets:
                        init_seq += f", {keys} = '{values}'"
                    elif keys == "values" :
                        init_seq += f", {keys} = [{values}]"
                    else :
                        init_seq += f", {keys} = {values}"
        init_seq += ')\n'
        layout_seq = f"{data[0]["name"]}.{data[0]["layout"]}("
        for sets, val in data[2].items():
            if sets in ["sticky", "side", "fill", "anchor"]:
                layout_seq += f"{sets} = '{val}' ,"
            else : 
                layout_seq += f"{sets} = {val} ,"
        layout_seq = layout_seq[0:-1] + ")\n" if len(data[2].keys()) > 0 else layout_seq + ")\n"
        return [init_seq, layout_seq, "\n"]
    

    def mWidCode(cls, old_data : list, new_data : list, project_path):
        code = fileop.loadInfo(project_path, data = "prjtCodeList")
        old_widcode = cls.createWidCode(cls =CodeGeneration,  data = old_data)
        new_widcode = cls.createWidCode(cls =CodeGeneration,  data = new_data)
        print(old_data, "\n", new_widcode)
        if old_widcode[0] != new_widcode[0] :
            if old_widcode[0] in code :
                code.insert(code.index(old_widcode[0]), new_widcode[0])
                del code[code.index(old_widcode[0])]
            else :
                code.append(new_widcode[0])
        
        if old_widcode[1] != new_widcode[1] :
            if old_widcode[1] in code :
                code.insert(code.index(old_widcode[1]), new_widcode[1])
                del code[code.index(old_widcode[1])]
            else :
                code.append(new_widcode[1])
        code.append(new_widcode[2])
        return code


    def delWidCode(cls, widget, wid_id, project_path):
        code = fileop.loadInfo(project_path, data = "prjtCodeList")
        for lines in code :
            print(lines)
            if f"{widget} = {AppAttr.get(AppAttr,"widinfo")[wid_id]["tkid"]}" in lines :
                del code[code.index(lines):code.index(lines)+3]
                #del code[code.index(lines)]
            
        return code


if __name__ == "__main__" :
    data = [{"name": "optionmenu1", "ID": "optionmenu", "layout": "pack", "master": "self", "width": 200, "height": 200, "corner_radius": "None", "border_width": "None", "bg_color": "transparent", "fg_color": "None", "border_color": "None", "button_color": "None", "button_hover_color": "None", "dropdown_fg_color": "None", "dropdown_hover_color": "None", "dropdown_text_color": "None", "text_color": "None", "text_color_disabled": "None", "font": "1", "dropdown_font": "None", "values": "None", "state": "normal", "hover": "True", "variable": "None", "command": "None"}, {"family": "Arial", "size": 15, "weight": "bold"}, {"ipadx": 20, "ipady": 10, "anchor": "N", "fill": "X", "side": "BOTTOM"}]
    print(CodeGeneration.createWidCode(cls =CodeGeneration,  data = data))
    # data = {"PrjtName": "nouvtest", "WinName": "inter", "height": 100, "width": 50}
    # old_data = {"PrjtName": "nouvtest", "WinName": "inter", "height": 100, "width": 50}
    # path = fileop.createPath("projet" + "\\" + "code.py")
    # print(path)
    # print(CodeGeneration.mWinCode(CodeGeneration, old_data, data, path))
        