########################################
#                                      #
# Raspberry Pi Thermometer Dial        #
# Adapted from Adafruit DS18B20 Lesson #
# Written by Ryan Eggers               #
#                                      #
########################################
import os
import glob
import time
import Tkinter

from viewidget import Dial


TITLE = 'Thermometer Dial'
MODPROBE_GPIO = 'modprobe w1-gpio'
MODPROBE_THERM = 'modprobe w1-therm'
BASE_DIRECTORY = '/sys/bus/w1/devices/'


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def make_window():
    window = Tkinter.Tk()
    window.title(TITLE)
    window.frame = Tkinter.Frame(window, relief='ridge', borderwidth=2)
    window.frame.pack(fill='both', expand=1)
    # Add Dial Viewidget
    window.dialframe = Tkinter.Frame(window.frame)
    window.dialframe.pack(expand=1, fill='x')
    window.dial = Dial(window.dialframe, unit='degF')
    window.dial.pack(side=Tkinter.TOP)
    # Add exit button
    window.exitbutton = Tkinter.Button(window.frame, text='Exit', width=10, command=window.quit)
    window.exitbutton.pack(side='bottom', pady=17)
    return window


def update_dial():
    test_window.dial.set_value(read_temp()[1])  # degF
    test_window.after(1000, update_dial)


if __name__ == '__main__':
    os.system(MODPROBE_GPIO)
    os.system(MODPROBE_THERM)

    device_folder = glob.glob(BASE_DIRECTORY + '28*')[0]
    device_file = device_folder + '/w1_slave'

    # create the graphical interface
    test_window = make_window()
    update_dial()
    test_window.focus_set()
    test_window.mainloop()
