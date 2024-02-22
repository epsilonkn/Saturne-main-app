import customtkinter

window = customtkinter.CTk()

test = customtkinter.CTkOptionMenu()
test.grid(sticky = 'W' )

bt1 = customtkinter.CTkButton(, text = '', font = customtkinter.CTkFont(family = 'Arial' ))
bt1.grid(sticky = 'W' )

bt2 = customtkinter.CTkButton(, text = 'テスト')
bt2.grid(sticky = 'W' )

