#Saved 10/26/2024
from ina219 import INA219, DeviceRangeError
from time import sleep
import tkinter
from datetime import datetime
import os

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)
FONT_MAIN = ("Helvetica", 36)
FONT_BUTTON = ("Helvetica", 20)
BG_MAIN = "black"
FG_MAIN = "white"
BG_BOX = "white"
FG_BOX = "black"
PAD_X = 20
PAD_Y = 5
default_text = True
is_recording = False

#------------------GPIO DATA LOGGING------------------------------#
def read_ina219():
    global power, bus_current, bus_voltage
    try:
        print('Bus Voltage: {0:0.2f}V'.format(ina.voltage()))
        print('Bus Current: {0:0.2f}mA'.format(ina.current()))
        print('Power: {0:0.2f}mW'.format(ina.power()))
        print('Shunt Voltage: {0:0.2f}mV\n'.format(ina.shunt_voltage()))
        power='{0:0.2f}'.format(ina.power())
        bus_current='{0:0.2f}'.format(ina.current())
        bus_voltage='{0:0.2f}V'.format(ina.voltage())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resister
        print(e)


#------------------SCREEN REFRESH FUNCTION-------------------------#
def screen_refresh():
    global display_time
    now = datetime.now()
    hms = now.strftime("%H:%M:%S")
    ms = now.strftime("%f")[:2]
    display_time = ":".join([hms, ms])
    read_ina219()
    row_1_box.config(text=power)
    row_2_box.config(text=bus_current)
    row_3_box.config(text=bus_voltage)
    if is_recording:  # Checks if is_recording is True
        record_data()  # Records a row of data using record_data function
        window.after(100, screen_refresh)  # Waits 100ms and recalls this screen refresh function
    else:
        window.after(500, screen_refresh)  # Waits 500ms and recalls this screen refresh function


#------------------TEMPORARY TEXT FUNCTION FOR FILE NAME BOX------#
def temp_text(e):
    row_4.delete(0, "end")


#-------------------START AND STOP FUNCTIONS----------------------#
def start_rec():
    global is_recording, file_name
    user_input = row_4.get()
    print("User input:", user_input)
    file_name = user_input + '.txt'
    if os.path.isfile(file_name):
        print("This file already exists")
        row_4_recording.config(text="Pick a New Name", bg="red")
    else:
        print("We can continue")
        row_4_recording.config(text="Recording", bg="red")
        with open(file_name, "w") as file:
            file.write(f"time, power(mW), bus voltage(mV), current(mA)\n")
        is_recording = True


def stop_rec():
    global is_recording
    is_recording = False
    row_4.delete(0, 'end')
    row_4.insert(0, "Type your file name here")
    window.focus_set()
    row_4.bind("<FocusIn>", temp_text)
    row_4_recording.config(text="Not Recording", bg=BG_MAIN)
    window.update_idletasks()


def record_data():
    global is_recording
    read_ina219()
    if is_recording:
        with open(file_name, "a") as file:
            file.write(f"{display_time}, {power}, {bus_voltage}, {bus_current}\n")
    else:
        return


#-------------------WINDOW UI--------------------------------------------------------------#

window = tkinter.Tk()
window.title("Wind Power Station")
window.minsize(width=1100, height=450)
window.config(padx=20, pady=30, bg="black")

row_1 = tkinter.Label(text="Power", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_1.grid(column=1, row=1, pady=PAD_Y, sticky="E")
row_1_box = tkinter.Label(text="0.00", fg=FG_BOX, bg=BG_BOX, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_1_box.grid(column=2, row=1, pady=PAD_Y)
row_1_units = tkinter.Label(text="milliWatts", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_1_units.grid(column=3, row=1, pady=PAD_Y, sticky="W")

row_2 = tkinter.Label(text="Current", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_2.grid(column=1, row=2, pady=PAD_Y, sticky="E")
row_2_box = tkinter.Label(text="0.00", fg=FG_BOX, bg=BG_BOX, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_2_box.grid(column=2, row=2, pady=PAD_Y)
row_2_units = tkinter.Label(text="milliAmps", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_2_units.grid(column=3, row=2, pady=PAD_Y, sticky="W")

row_3 = tkinter.Label(text="Bus Voltage", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_3.grid(column=1, row=3, pady=PAD_Y, sticky="E")
row_3_box = tkinter.Label(text="0.00", fg=FG_BOX, bg=BG_BOX, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_3_box.grid(column=2, row=3, pady=PAD_Y)
row_3_units = tkinter.Label(text="Volts", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_3_units.grid(column=3, row=3, pady=PAD_Y, sticky="W")

row_4 = tkinter.Entry(window, width=25, font=("Helvetica", 24), fg="black")
row_4.insert(0, "Type your file name here")
row_4.bind("<FocusIn>", temp_text)
row_4.grid(column=1, row=4, columnspan=2, pady=PAD_Y, sticky="E")
row_4_label = tkinter.Label(text=".txt", fg=FG_MAIN, bg=BG_MAIN, font=FONT_MAIN, padx=PAD_X, pady=PAD_Y)
row_4_label.grid(column=3, row=4, pady=PAD_Y, sticky="W")

button1 = tkinter.Button(text="Start Recording", font=(FONT_MAIN, 20, "bold"), command=start_rec)
button1.grid(column=1, row=5, padx=PAD_X)

button2 = tkinter.Button(text="Stop Recording", font=(FONT_MAIN, 20, "bold"), command=stop_rec)
button2.grid(column=2, row=5, padx=PAD_X)

row_4_recording = tkinter.Label(text="Not Recording", fg=FG_MAIN, bg=BG_MAIN, font=FONT_BUTTON, padx=PAD_X, pady=PAD_Y)
row_4_recording.grid(column=3, row=5, pady=PAD_Y)

#-------------------------------Screen Freshing Function Call --------------------------------------#
screen_refresh()

#------------------------------GUI Main Loop End---------------------------------------------------#
window.mainloop()
