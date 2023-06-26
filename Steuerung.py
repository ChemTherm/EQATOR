import time
import json
import customtkinter as ctk
from PIL import Image,ImageTk
from ChemTherm_library.tinkerforge_lib import *


    


def tk_loop():
    
    MFC_N2.set(0)
    #MFC_CO2.set(int(set_MFC[1].get()))
   # MFC_CH4.set(int(set_MFC[2].get()))
    
    
    value_MFC[0].configure(text = str(MFC_N2.voltage) + " mV") 
    value_MFC[1].configure(text = str(MFC_CO2.voltage) + " mV") 
    value_MFC[2].configure(text = str(MFC_CH4.voltage) + " mV") 
    
    
    window.after(500, tk_loop)
        
 

#----------- Json Setup ----------
with open('SetUp1.json', 'r') as config_file:
    config = json.load(config_file)
    
     
 
#----------- TKforge Devices
HOST = "localhost"
PORT = 4223

ipcon = IPConnection() # Create IP connection
ipcon.connect(HOST, PORT) # Connect to brickd
 

MFC_N2 = MFC_AIO_30(ipcon, "21uc", "21ft")
MFC_CO2 = MFC_AIO_30(ipcon, "21u9","21fe")
MFC_CH4 = MFC_AIO_30(ipcon, "21un","21fi") 
 
 
    
window = ctk.CTk()
ctk.set_appearance_mode("light")
scrW = window.winfo_screenwidth()
scrH = window.winfo_screenheight()
window.geometry("600x200")


#----------- Frames ----------
lf_MFC = ctk.CTkFrame(window, border_color=config['TKINTER']['background-color'], border_width=0, height=scrH, width=scrW)
name_Frame = ctk.CTkLabel(lf_MFC, font = ('Arial',16), text='MFC Steuerung')
name_Frame.grid(column=0, columnspan = 2, row=0, ipadx=5, ipady=5)
lf_MFC.place(x= 0,y= 0)



name_MFC={}; set_MFC={}; unit_MFC={}; value_MFC={}
for i in range(0,3):
    name_MFC[i]= ctk.CTkLabel(lf_MFC, font = ('Arial',16), text=config['MFC']['name'][i])
    name_MFC[i].grid(column=0, row=i+1, ipadx=5, ipady=5)
    set_MFC[i] = tk.Entry(lf_MFC, font = ('Arial',16), width = 6 )
    set_MFC[i].grid(column=1, row=i+1, ipadx=5, ipady=5)
    unit_MFC[i]= ctk.CTkLabel(lf_MFC, font = ('Arial',16), text=' mV')
    unit_MFC[i].grid(column=2, row=i+1, ipadx=5, ipady=5)
    value_MFC[i]= ctk.CTkLabel(lf_MFC, font = ('Arial',16), text='0 mV')
    value_MFC[i].grid(column=3, row=i+1, ipadx=5, ipady=5)


window.after(1000, tk_loop())
window.mainloop()

print("shutting down...")