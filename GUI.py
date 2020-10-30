# import ESCDDEnter as dd
import tkinter as tk
import os

# Create window and frame
window = tk.Tk()
window.title('Manual Functions')
window.geometry("400x100")
top_frame = tk.Frame(window)
top_frame.pack()
middle_frame = tk.Frame(window)
middle_frame.pack()
bottom_frame = tk.Frame(window)
bottom_frame.pack()

# event handler for 4 python scripts
def get_data():
    print('get_data')
    os.system('python3 ESCDDEnter.py')

def sync_clock():
    print('sync_clock')
    os.system('python3 ESCCCEnter.py')
    
def reset_field_unit():
    print('reset_field_unit')
    os.system('python3 ESCIREnter.py')
    
def request_backlog_data():
    print('request_backlog_data')
    
def exit_program():
    exit()

# 4 function keys
topleft_button = tk.Button(top_frame, text='ESC DD ↵', command=get_data)
topleft_button.pack(side=tk.LEFT)

topright_button = tk.Button(top_frame, text='ESC CC ↵', command=sync_clock)
topright_button.pack(side=tk.LEFT)

middleleft_button = tk.Button(middle_frame, text='ESC IR ↵', command=reset_field_unit)
middleleft_button.pack(side=tk.LEFT)

middleright_button = tk.Button(middle_frame, text='ESC BH ↵', command=request_backlog_data)
middleright_button.pack(side=tk.LEFT)

# exit button
bottom_button = tk.Button(bottom_frame, text='Exit', fg='black', command=exit_program)
bottom_button.pack(side=tk.BOTTOM)

# Main Program
window.mainloop()