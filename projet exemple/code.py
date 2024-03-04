import customtkinter

window = customtkinter.CTk()


window.title('Mon App')


frame1 = customtkinter.CTkFrame(window)
frame1.pack()

entry1 = customtkinter.CTkEntry(frame1, width = 150, height = 30)
entry1.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 1 ,sticky = 'W' )

bt1 = customtkinter.CTkButton(frame1, text = 'valider', font = customtkinter.CTkFont(family = 'Arial' ,size = 15 ,weight = 'bold' ))
bt1.grid(padx = 10 ,column = 1 ,row = 1 ,sticky = 'W' )

label1 = customtkinter.CTkLabel(frame1, text = 'Entrez un nombre :', font = customtkinter.CTkFont(family = 'Arial' ,size = 20 ,weight = 'bold'))
label1.grid(padx = 10 ,pady = 5 ,column = 0 ,columnspan = 2 ,row = 0 ,sticky = 'W' )


