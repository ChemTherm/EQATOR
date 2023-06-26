import time
import json
import customtkinter as ctk
from PIL import Image,ImageTk
from ChemTherm_library.tinkerforge_lib import *


    


def tk_loop():
    
    
    window.after(500, tk_loop)
        
    
window = ctk.CTk()
ctk.set_appearance_mode("light")
scrW = window.winfo_screenwidth()
scrH = window.winfo_screenheight()
window.geometry("600x200")


window.after(1000, tk_loop())
window.mainloop()

print("shutting down...")