import time
import json
import customtkinter as ctk
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
from ChemTherm_library.tinkerforge_lib import *


    


def tk_loop():
    
    #MFC_N2.set(int(0))
    #MFC_CO2.set(int(set_MFC[1].get()))
   # MFC_CH4.set(int(set_MFC[2].get()))
    
    
    if (MFC_N2.voltage > 0.03):
        value_MFC[0].configure(text = str("{0:.2f}").format((MFC_N2.voltage+N2_zero)*config['MFC']['gradient'][0] + config['MFC']['x-axis'][0])+ " ml/min")  
    else:
        value_MFC[0].configure(text = str("{0:.2f}").format(0.0) + " ml/min")

    if (MFC_CO2.voltage > 0.15):
        value_MFC[1].configure(text = str("{0:.2f}").format((MFC_CO2.voltage+CO2_zero)*config['MFC']['gradient'][1] + config['MFC']['x-axis'][1])+ " ml/min")  
    else:
        value_MFC[1].configure(text = str("{0:.2f}").format(0.0) + " ml/min")

    if (MFC_CH4.voltage > 0.02):
        value_MFC[2].configure(text = str("{0:.2f}").format((MFC_CH4.voltage+CH4_zero)*config['MFC']['gradient'][2] + config['MFC']['x-axis'][2])+ " ml/min") 
    else:
        value_MFC[2].configure(text = str("{0:.2f}").format(0.0) + " ml/min")
    
    window.after(500, tk_loop)
        
def getdata():

    if set_MFC[0].get() !='':
        MFC_N2.set(int(max(1000*(float(set_MFC[0].get())- config['MFC']['x-axis'][0])/ config['MFC']['gradient'][0],0)))
    if set_MFC[1].get() !='':
        MFC_CO2.set(int(max(1000*(float(set_MFC[1].get())- config['MFC']['x-axis'][1])/ config['MFC']['gradient'][1],0)))
    if set_MFC[2].get() !='':
        MFC_CH4.set(int(max(1000*(float(set_MFC[2].get())- config['MFC']['x-axis'][2])/ config['MFC']['gradient'][2],0)))
   
def getfile():
    filename = askopenfilename()

#----------- Json Setup ----------
with open('config.json', 'r') as config_file:
  config = json.load(config_file)
    
     
 
#------ Tinkerforge Devices -------
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
window.title("Equator MFC-Steuerung")
window.geometry("350x300")


#----------- Frames ----------
lf_MFC = ctk.CTkFrame(window, border_color='#F2F2F2', border_width=0, height=scrH, width=scrW)
name_Frame = ctk.CTkLabel(lf_MFC, font = ('Arial',16), text='MFC Steuerung')
name_Frame.grid(column=0, columnspan = 2, row=0, ipadx=5, ipady=5)
lf_MFC.place(x= 30,y= 80)

#------ Buttons ---------
set_Value = ctk.CTkButton(window,text = 'Set Values', command = getdata, fg_color = 'brown')
set_Value.place(x=30, y=10)
#get_filename = ctk.CTkButton(window,text = 'Config File', command = getfile, fg_color = 'brown')
#get_filename.place(x=30, y=40)

MFC_List = config['MFC']['name']
name_MFC={}; set_MFC={}; unit_MFC={}; value_MFC={}
for i in range(0,3):
    name_MFC[i]= ctk.CTkLabel(lf_MFC, font = ('Arial',16), text=MFC_List[i])
    name_MFC[i].grid(column=0, row=i+1, ipadx=5, ipady=5)
    set_MFC[i] = tk.Entry(lf_MFC, font = ('Arial',16), width = 6 )
    set_MFC[i].grid(column=1, row=i+1, ipadx=5, ipady=5)
    unit_MFC[i]= ctk.CTkLabel(lf_MFC, font = ('Arial',16), text=' mV')
    unit_MFC[i].grid(column=2, row=i+1, ipadx=5, ipady=5)
    value_MFC[i]= ctk.CTkLabel(lf_MFC, font = ('Arial',16), text='0 mV')
    value_MFC[i].grid(column=3, row=i+1, ipadx=5, ipady=5)


CH4_zero = MFC_CH4.voltage
N2_zero = MFC_N2.voltage
CO2_zero = MFC_CO2.voltage

window.after(1000, tk_loop())
window.mainloop()

MFC_N2.set(int(0))
MFC_CO2.set(int(0))
MFC_CH4.set(int(0))
print("shutting down...")