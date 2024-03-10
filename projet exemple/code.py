import customtkinter

window = customtkinter.CTk()


window.title('Mon App')


frame = customtkinter.CTkFrame(window)
frame.pack()

entry = customtkinter.CTkEntry(frame, width = 150, height = 30)
entry.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 1 ,sticky = 'W' )

button = customtkinter.CTkButton(frame, text = 'valider', font = customtkinter.CTkFont(family = 'Arial' ,size = 15 ,weight = 'bold' ))
button.grid(padx = 10 ,column = 1 ,row = 1 ,sticky = 'W' )

label = customtkinter.CTkLabel(frame, text = 'Entrez un nombre :', font = customtkinter.CTkFont(family = 'Arial' ,size = 20 ,weight = 'bold'))
label.grid(padx = 10 ,pady = 5 ,column = 0 ,columnspan = 2 ,row = 0 ,sticky = 'W' )

