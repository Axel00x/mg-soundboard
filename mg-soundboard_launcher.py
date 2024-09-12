import os, sys
import tkinter as tk
from tkinter import messagebox
import subprocess
import time
from win32com.client import Dispatch

launcher_version = "1.0.0"

'''def create_shortcut(path_to_py):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop, 'mg-soundboard_launcher.lnk')

    # Ensure the target path exists
    if not os.path.isfile(path_to_py):
        messagebox.showerror("Error", f"The file {path_to_py} does not exist.")
        return
    
    # Debugging output
    print(f"Creating shortcut at: {shortcut_path}")
    print(f"Target path for shortcut: {path_to_py}")

    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = path_to_py
        shortcut.IconLocation = path_to_py
        shortcut.Description = "Shortcut to mg-soundboard_launcher.py"
        shortcut.save()
        messagebox.showinfo("Shortcut Created", "Shortcut to mg-soundboard_launcher.py created on your desktop.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create shortcut: {e}")
        print(e)
'''
def execute_main_exe():
    execute_button["state"] = "disabled"
    
    current_dir = os.getcwd()
    dist_folder = os.path.join(current_dir, "dist")
    main_exe = os.path.abspath(os.path.join(dist_folder, "mg-soundboard_main.exe"))
    launcher_py = os.path.abspath("mg-soundboard_launcher.py")

    #print(f"Main EXE Path: {main_exe}")
    #print(f"Launcher PY Path: {launcher_py}")

    if os.path.exists(main_exe):
        '''result = messagebox.askyesno("Create Shortcut", "Do you want to create a desktop shortcut for mg-soundboard_launcher.py?")
        
        if result:
            create_shortcut(launcher_py)
        ''' 
        
        # Execute the mg-soundboard_main.exe file
        try:
            subprocess.Popen(main_exe)
        except Exception as e:
            messagebox.showerror("Error", f"Could not run mg-soundboard_main.exe: {e}")
            execute_button.config(text="Error!")
    else:
        messagebox.showerror("File Not Found", "The file mg-soundboard_main.exe was not found in the 'dist' folder.")
        execute_button.config(text="File Not Found")

    root.quit()
    
# Main function to create a GUI
root = tk.Tk()
root.title("mg-soundboard launcher")
root.geometry("300x200")

version = tk.Label(root, text="Launcher version: "+launcher_version, pady=20)
version.pack()

label = tk.Label(root, text="Welcome! Click below to execute mg-soundboard.", pady=20)
label.pack()

execute_button = tk.Button(root, text="Execute", command=execute_main_exe, padx=20, pady=10)
execute_button.pack()

root.mainloop()
