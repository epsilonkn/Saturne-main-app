import customtkinter

window = customtkinter.CTk()

frame1 = customtkinter.CTkFrame(window)
frame1.grid()

label1 = customtkinter.CTkLabel(frame1, text = 'j\'aime les label...rigole pas', wraplength = 0)
label1.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 0 )

bt1 = customtkinter.CTkButton(frame1, text = 'j\'aime les bouton...wesh')
bt1.grid(padx = 10 ,pady = 10 ,column = 0 ,row = 1 )

