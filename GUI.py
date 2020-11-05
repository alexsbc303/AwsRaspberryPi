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
#     print('get_data')
    os.system('python3 EscDDEnter.py')

def sync_clock():
#     print('sync_clock')
    os.system('python3 EscCCEnter.py')
    
def reset_field_unit():
#     print('reset_field_unit')
    os.system('python3 EscIREnter.py')
    
def get_backlog():
#     print('get_backlog')
    os.system('python3 EscBHEnter.py')
    
def exit_program():
    exit()

# 4 function keys
topleft_button = tk.Button(top_frame, text='Get Data', command=get_data)
topleft_button.pack(side=tk.LEFT)

topright_button = tk.Button(top_frame, text='Sync Clock', command=sync_clock)
topright_button.pack(side=tk.LEFT)

middleleft_button = tk.Button(middle_frame, text='Reset Field Unit', command=reset_field_unit)
middleleft_button.pack(side=tk.LEFT)

middleright_button = tk.Button(middle_frame, text='Get Backlog', command=get_backlog)
middleright_button.pack(side=tk.LEFT)

# exit button
bottom_button = tk.Button(bottom_frame, text='Exit Program', command=exit_program)
bottom_button.pack(side=tk.LEFT)

# Main Program
window.mainloop()