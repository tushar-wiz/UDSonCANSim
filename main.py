from tkinter import *
import customtkinter as tk
import server as sv
import client as cl
import headerfile as hf
from PIL import Image
import time

# Create a new window
root = tk.CTk()
root.geometry("700x700")
root.resizable(width=False, height=False)
root.iconbitmap("./media/favicon.ico")
root.title("UDS SIM")

top_frame = tk.CTkFrame(root)
top_frame.pack(fill= tk.X, side = tk.TOP)
engine_image = tk.CTkImage(Image.open("./media/engine.webp"), size=(190,190))
engine_label = tk.CTkLabel(top_frame, image=engine_image, text="")
engine_label.pack(side="left", padx=25, pady=10)

computer_image = tk.CTkImage(Image.open("./media/computer.png"), size=(190,190))
computer_label = tk.CTkLabel(top_frame, image=computer_image, text="")
computer_label.pack(side="right", padx=25, pady=10)

frame_progress_var = tk.DoubleVar()
frame_progress = tk.CTkProgressBar(top_frame, variable=frame_progress_var ,orientation='horizontal', mode='determinate')
frame_progress.pack(side="right", padx=25, pady=10)

# ----------------------------------------------------
# LEFT FRAME
left_frame = tk.CTkFrame(root)
left_frame.pack(side="left",fill= tk.X, padx=20, pady=10)

# Add a label to the top of the left frame
SERVER_label = tk.CTkLabel(left_frame, text="SERVER")
SERVER_label.pack(side="top", padx = 10, pady = 10, fill=tk.X)

RESPONSE_label = tk.CTkLabel(left_frame, text="RX Message:")
RESPONSE_label.pack(side="top", padx = 10, pady = 10, fill=tk.X)

RESPONSE_textField = tk.CTkTextbox(left_frame, width=400,height=310)
RESPONSE_textField.pack(side="top", padx=10, pady=10)

def CLEAR_func():
    RESPONSE_textField.delete("1.0","end")

CLEAR_button = tk.CTkButton(left_frame, text="CLEAR", command=CLEAR_func)
CLEAR_button.pack(side="top", padx=10, pady=10)

# ----------------------------------------------------
# RIGHT FRAME
right_frame = tk.CTkFrame(root)
right_frame.pack(side="right", fill= tk.BOTH, padx=10, pady=10)

client_label = tk.CTkLabel(right_frame, text="MESSAGE")
client_label.pack(side="top")

manual_frame = tk.CTkFrame(right_frame)
example_frame = tk.CTkFrame(right_frame)

PCI_frame = tk.CTkFrame(manual_frame)
PCI_frame.pack(side="top", fill= tk.X, padx=10, pady=10)
PCI_label = tk.CTkLabel(PCI_frame, text = "PCI")
PCI_label.pack(side="left", padx=10, pady=10)
PCI_textField = tk.CTkTextbox(PCI_frame,width=95,height=10)
PCI_textField.pack(side="right", padx=10, pady=10)

SID_frame = tk.CTkFrame(manual_frame)
SID_frame.pack(side="top", fill= tk.X, padx=10, pady=10)
SID_label = tk.CTkLabel(SID_frame, text = "SID")
SID_label.pack(side="left", padx=10, pady=10)
SID_options = list(hf.SID.keys())
SID_key = tk.StringVar()
SID_dropdown = tk.CTkOptionMenu(SID_frame, variable=SID_key, values= SID_options, width=95)
SID_dropdown.pack(side="right", padx=10, pady=10)

DID_SUB_frame = tk.CTkFrame(manual_frame)
DID_SUB_frame.pack(side="top", fill= tk.X, padx=10, pady=10)
DID_SUB_key = tk.StringVar()
DID_SUB_options = ["DID","SUB"]
DID_SUB_dropdown = tk.CTkOptionMenu(DID_SUB_frame, variable=DID_SUB_key, values= DID_SUB_options, width=65, fg_color="#1D1E1E")
DID_SUB_dropdown.pack(side="left", padx=5)
DID_SUB_textField = tk.CTkTextbox(DID_SUB_frame,width=95, height=10)
DID_SUB_textField.pack(side="right", padx=10 ,pady=10)

DATA_frame = tk.CTkFrame(manual_frame)
DATA_frame.pack(side="top", fill= tk.X, padx=10, pady=10)
DATA_label = tk.CTkLabel(DATA_frame, text = "DATA")
DATA_label.pack(side="left", padx=10, pady=10)
DATA_textField = tk.CTkTextbox(DATA_frame,width=95,height=10)
DATA_textField.pack(side="right", padx=10, pady=10)

EXAMPLE_key = tk.StringVar()
EXAMPLE_options = ["Session Control","Single Frame"]
EXAMPLE_dropdown = tk.CTkOptionMenu(example_frame, variable=EXAMPLE_key, values=EXAMPLE_options, width=250)
EXAMPLE_dropdown.pack(side="top", padx=10, pady=20)

def MANUAL_EXAMPLE_func(MANUAL_EXAMPLE_key):
    if(MANUAL_EXAMPLE_key == "MANUAL"):
        example_frame.pack_forget()
        manual_frame.pack(padx=10)

    elif(MANUAL_EXAMPLE_key == "EXAMPLE"):
        manual_frame.pack_forget()
        example_frame.pack(padx=10)

MANUAL_EXAMPLE_options = ["MANUAL", "EXAMPLE"]
MANUAL_EXAMPLE_key_ext = tk.StringVar(value="MANUAL")
MANUAL_EXAMPLE_button = tk.CTkSegmentedButton(right_frame, values=MANUAL_EXAMPLE_options, variable=MANUAL_EXAMPLE_key_ext, command=MANUAL_EXAMPLE_func)
MANUAL_EXAMPLE_button.pack(side="top", fill=tk.X, padx=10, pady=10)

manual_frame.pack(padx=10)

def serverRun():
    # imitate reading bus data
    sv.readMessage()

    # configure active session as last used session
    sv.readSession()

    response = ""

    flagS = 0
    for i in range(0, 5):
        if sv.stored_SID[i] == sv.fr[1]:
            flagS = 1
            break

    if(flagS):
        if sv.fr[1] == 0x10:
            if sv.fr[2] == 0x02 and sv.currentSession == 0x01:
                response += sv.session_change_fail()  # defaultSession to programmingSession is unallowed
            else:
                response += sv.session_change_pass()
                sv.writeSession()
        else:
            response += sv.service_present()
    else:
        response += sv.service_not_supported()

    response += sv.displayFrame(sv.fr)
    RESPONSE_textField.insert(INSERT,response)
    sv.writeSession()
    

def clientRun():
    
    if(MANUAL_EXAMPLE_key_ext.get()=="MANUAL"):
        PCI = PCI_textField.get(1.0,"end-1c")
        SID = SID_key.get()
        DID_SUB = DID_SUB_key.get()
        DID_SUB_VAL = DID_SUB_textField.get(1.0,"end-1c")
        DATA = DATA_textField.get(1.0,"end-1c")

        if(PCI == "" or SID == "" or DID_SUB == "" or DATA == ""):
            print("error")
            return

        hf.fr[0] = int(PCI,16)
        hf.fr[1] = hf.SID[SID]

        if(DID_SUB == "DID"):
            hf.fr[2] = int(DID_SUB_VAL,16) >> 8
            hf.fr[3] = int(DID_SUB_VAL,16) & 0xff
        else:
            hf.fr[2] = int(DID_SUB_VAL,16)
        hf.displayFrame(hf.fr)
        
    else:
        if(EXAMPLE_key.get() == EXAMPLE_options[0]):
            cl.example_sessionControl()
        else:
            cl.example_singleFrame1()
    
    cl.fr = hf.fr
    RESPONSE_textField.insert(INSERT, '\n\nFRAME RECEIVED:')
    RESPONSE_textField.insert(INSERT, cl.displayFrame(cl.fr)+'\n')
    cl.writeMessage()

    serverRun()

# Add a button to the bottom of the right frame
send_button = tk.CTkButton(right_frame, text="SEND", command=clientRun)
send_button.pack(side="bottom", padx=10, pady=10)

# Run the main event loop
root.mainloop()
