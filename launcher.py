import os
import tkinter as tk
from tkinter import messagebox
import subprocess
import time
import winshell

# Function to create a desktop shortcut for launcher.py
def create_shortcut(path_to_py):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop, 'launcher.lnk')

    try:
        winshell.CreateShortcut(
            Path=shortcut_path,
            Target=path_to_py,
            Icon=(path_to_py, 0),
            Description="Shortcut to launcher.py"
        )
        messagebox.showinfo("Shortcut Created", "Shortcut to launcher.py created on your desktop.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create shortcut: {e}")
        print(e)

# Function to check for dist folder and execute main.exe
def execute_main_exe():
    execute_button["state"] = "disabled"
    execute_button.config(text="Waiting response...")  # Change to "Waiting response..."
    
    current_dir = os.getcwd()
    dist_folder = os.path.join(current_dir, "dist")
    main_exe = os.path.join(dist_folder, "main.exe")
    launcher_py = os.path.join(current_dir, "launcher.py")

    if os.path.exists(main_exe):
        # Ask the user if they want to create a shortcut for launcher.py
        result = messagebox.askyesno("Create Shortcut", "Do you want to create a desktop shortcut for launcher.py?")
        
        if result:
            create_shortcut(launcher_py)

        execute_button.config(text="Loading...")  # Change to "Loading..."
        
        # Execute the main.exe file
        try:
            subprocess.Popen(main_exe)
            time.sleep(3)  # Simulate a delay for launching
            execute_button.config(text="Ready!")  # Change to "Ready!"
        except Exception as e:
            messagebox.showerror("Error", f"Could not run main.exe: {e}")
            execute_button.config(text="Error!")
    else:
        messagebox.showerror("File Not Found", "The file main.exe was not found in the 'dist' folder.")
        execute_button.config(text="File Not Found")


# Main function to create a GUI
root = tk.Tk()
root.title("Main.exe Executor")
root.geometry("300x200")

label = tk.Label(root, text="Welcome! Click below to execute main.exe.", pady=20)
label.pack()

execute_button = tk.Button(root, text="Execute main.exe", command=execute_main_exe, padx=20, pady=10)
execute_button.pack()

root.mainloop()
