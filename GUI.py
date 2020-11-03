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

# event handler for 4 python scripts
def get_data():
#     print('get_data')
    os.system('python3 EscDDEnterEscBHEnter.py')

def sync_clock():
#     print('sync_clock')
    os.system('python3 ESCCCEnter.py')
    
def reset_field_unit():
#     print('reset_field_unit')
    os.system('python3 ESCIREnter.py')
    
def exit_program():
    exit()

# 3 function keys
topleft_button = tk.Button(top_frame, text='Get Data', command=get_data)
topleft_button.pack(side=tk.LEFT)

topright_button = tk.Button(top_frame, text='Sync Clock', command=sync_clock)
topright_button.pack(side=tk.LEFT)

middleleft_button = tk.Button(middle_frame, text='Reset Field Unit', command=reset_field_unit)
middleleft_button.pack(side=tk.LEFT)

# exit button
middleright_button = tk.Button(middle_frame, text='Exit', command=exit_program)
middleright_button.pack(side=tk.LEFT)

# Main Program
window.mainloop()