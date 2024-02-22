import customtkinter

window = customtkinter.CTk()


window.title('mon application')


main_frame = customtkinter.CTkFrame(window)
main_frame.pack()

main_label = customtkinter.CTkLabel(main_frame, text = 'entrez un nombre :', font = customtkinter.CTkFont(family = 'Arial' ,size = 14 ,weight = 'bold' ))
main_label.grid(padx = 10 ,pady = 10 ,column = 0 ,columnspan = 2 ,row = 0 ,sticky = 'W' )

valider_bt = customtkinter.CTkButton(main_frame, border_spacing = 2, text = 'valider', font = customtkinter.CTkFont(family = 'Arial' ,size = 12 ,weight = 'bold' ))
valider_bt.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 2 ,sticky = 'W' )

text_entry = customtkinter.CTkEntry(main_frame, width = 220)
text_entry.grid(padx = 10 ,pady = 5 ,column = 0 ,columnspan = 2 ,row = 1 ,sticky = 'W' )

cancel_bt = customtkinter.CTkButton(main_frame, border_spacing = 2, text = 'annuler', font = customtkinter.CTkFont(family = 'Arial' ,size = 12 ,weight = 'bold' ))
cancel_bt.grid(padx = 10 ,pady = 10 ,column = 1 ,row = 2 ,sticky = 'W' )

