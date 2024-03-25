import customtkinter

window = customtkinter.CTk()

window.title('interface')


#variables

checkbox_var = None

#functions


#frames

label_frame = customtkinter.CTkFrame(window)
label_frame.pack(fill = 'both' ,side = 'top' )

action_frame = customtkinter.CTkFrame(window)
action_frame.pack(fill = 'both' ,side = 'top' )

sub_frame = customtkinter.CTkFrame(window)
sub_frame.pack(fill = 'both' ,side = 'top' )


#widgets

label = customtkinter.CTkLabel(label_frame, text = 'Ceci est un exemple :', font = customtkinter.CTkFont(family = 'Arial' ,size = 20 ,weight = 'bold' ))
label.pack(padx = 10 ,pady = 10 ,side = 'left' )

entry = customtkinter.CTkEntry(action_frame, width = 150, height = 30)
entry.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 0 )

button = customtkinter.CTkButton(action_frame, border_spacing = 2, text = 'Valider', hover = False)
button.grid(padx = 10 ,pady = 10 ,column = 1 ,row = 0 )

verif_label = customtkinter.CTkLabel(sub_frame, text = 'ne plus afficher', font = customtkinter.CTkFont(family = 'Arial' ,size = 16 ,weight = 'bold' ))
verif_label.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 0 ,sticky = 'E' )

checkbox = customtkinter.CTkCheckBox(sub_frame, checkbox_width = 24, checkbox_height = 24, text = '', hover = False, variable = checkbox_var)
checkbox.grid(padx = 10 ,pady = 10 ,column = 1 ,row = 0 ,sticky = 'E' )

