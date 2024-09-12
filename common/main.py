from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import keyboard
import json
import os

pygame.mixer.init()

CONFIG_FILE = "config.json"

def save_config(soundboard):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(soundboard, config_file)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    return {}

class Sound:
    def __init__(self, name, file, loop=False, stop_others=True, volume=1.0, active=True):
        self.name = name
        self.file = file
        try:
            self.sound = pygame.mixer.Sound(file)  
        except pygame.error as e:
            print(f"Error loading audio file {file}: {e}")
            self.sound = None
        self.loop = loop
        self.stop_others = stop_others
        self.volume = volume
        self.active = active
        if self.sound:
            self.apply_settings()

    def apply_settings(self):
        if self.sound:
            self.sound.set_volume(self.volume)

    def play(self):
        if not self.active or not self.sound:
            return  
        if self.stop_others:
            pygame.mixer.stop()
        self.apply_settings()
        if self.loop:
            self.sound.play(-1)  
        else:
            self.sound.play()  

    def stop(self):
        if self.sound:
            self.sound.stop()

class SoundboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("mg-soundboard")
        self.soundboard = load_config()  
        self.sounds = {key: Sound(**settings) for key, settings in self.soundboard.items()}

        style = ttk.Style()
        style.configure("Treeview", foreground="black", background="white", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="lightgrey", foreground="black")

        self.tree = ttk.Treeview(root, columns=("Key", "File", "Name", "Loop", "Stop Others", "Volume", "Active"), show='headings')
        self.tree.heading("Key", text="Key")
        self.tree.heading("File", text="File")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Loop", text="Loop")
        self.tree.heading("Stop Others", text="Stop Others")
        self.tree.heading("Volume", text="Volume")
        self.tree.heading("Active", text="Active")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for key, sound in self.sounds.items():
            self.tree.insert("", "end", iid=key, text=key, values=(key, sound.file, sound.name, str(sound.loop), str(sound.stop_others), str(int(sound.volume * 100)), str(sound.active)))

        self.tree.bind("<Double-1>", self.on_item_double_click)

        self.shortcut_active = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Shortcut", variable=self.shortcut_active).pack()

        tk.Button(self.root, text="Add Sound", command=self.add_sound).pack(pady=10)
        tk.Button(self.root, text="Remove Sound", command=self.remove_sound).pack(pady=5)

        self.setup_hotkeys()

        self.auto_apply_settings()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def auto_apply_settings(self):
        for key in self.sounds.keys():
            sound = self.sounds[key]
            self.save_changes(key, key, sound.name, 
                            tk.BooleanVar(value=sound.loop), 
                            tk.BooleanVar(value=sound.stop_others), 
                            tk.IntVar(value=int(sound.volume * 100)), 
                            tk.BooleanVar(value=sound.active), None)


    def on_item_double_click(self, event):
        item_id = self.tree.selection()[0]
        sound = self.sounds[item_id]
        item = self.tree.item(item_id)
        values = item['values']

        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Modify {item_id}")

        edit_window.columnconfigure(0, weight=1)
        edit_window.columnconfigure(1, weight=2)
        edit_window.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        label_font = ('Arial', 10, 'bold')
        entry_font = ('Arial', 10)
        button_font = ('Arial', 12)
        padding = 10

        tk.Label(edit_window, text="Nome", font=label_font).grid(row=0, column=0, padx=padding, pady=padding, sticky="e")
        name_var = tk.StringVar(value=sound.name)
        tk.Entry(edit_window, textvariable=name_var, font=entry_font).grid(row=0, column=1, padx=padding, pady=padding, sticky="w")

        tk.Label(edit_window, text="Shortcut", font=label_font).grid(row=1, column=0, padx=padding, pady=padding, sticky="e")
        key_var = tk.StringVar(value=item_id)
        tk.Entry(edit_window, textvariable=key_var, font=entry_font).grid(row=1, column=1, padx=padding, pady=padding, sticky="w")

        tk.Label(edit_window, text="Loop", font=label_font).grid(row=2, column=0, padx=padding, pady=padding, sticky="e")
        loop_var = tk.BooleanVar(value=values[3] == "True")
        tk.Checkbutton(edit_window, variable=loop_var).grid(row=2, column=1, padx=padding, pady=padding, sticky="w")

        tk.Label(edit_window, text="Stop Other Sounds", font=label_font).grid(row=3, column=0, padx=padding, pady=padding, sticky="e")
        stop_var = tk.BooleanVar(value=values[4] == "True")
        tk.Checkbutton(edit_window, variable=stop_var).grid(row=3, column=1, padx=padding, pady=padding, sticky="w")

        tk.Label(edit_window, text="Volume (0-100)", font=label_font).grid(row=4, column=0, padx=padding, pady=padding, sticky="e")
        volume_var = tk.IntVar(value=int(values[5]))
        tk.Scale(edit_window, variable=volume_var, from_=0, to_=100, orient=tk.HORIZONTAL, length=200).grid(row=4, column=1, padx=padding, pady=padding, sticky="w")

        tk.Label(edit_window, text="Active", font=label_font).grid(row=5, column=0, padx=padding, pady=padding, sticky="e")
        active_var = tk.BooleanVar(value=values[6] == "True")
        tk.Checkbutton(edit_window, variable=active_var).grid(row=5, column=1, padx=padding, pady=padding, sticky="w")

        tk.Button(edit_window, text="Save", font=button_font, command=lambda: self.save_changes(item_id, key_var.get(), name_var.get(), loop_var, stop_var, volume_var, active_var, edit_window)).grid(row=6, column=0, columnspan=2, pady=padding)


    def save_changes(self, old_key, new_key, new_name, loop_var, stop_var, volume_var, active_var, edit_window):
        if old_key != new_key:
            if new_key in self.sounds:
                messagebox.showerror("Error", "The chosen shortcut is already in use!")
                return
            self.sounds[new_key] = self.sounds.pop(old_key)
            self.tree.delete(old_key)
            self.tree.insert("", "end", iid=new_key, text=new_key, values=(new_key, self.sounds[new_key].file, new_name, str(loop_var.get()), str(stop_var.get()), str(volume_var.get()), str(active_var.get())))
            keyboard.remove_hotkey(old_key)  
            keyboard.add_hotkey(new_key, lambda k=new_key: self.play_sound(k))  
        else:
            self.tree.item(old_key, values=(new_key, self.sounds[old_key].file, new_name, str(loop_var.get()), str(stop_var.get()), str(volume_var.get()), str(active_var.get())))

        sound = self.sounds[new_key]
        sound.name = new_name
        sound.loop = loop_var.get()
        sound.stop_others = stop_var.get()
        sound.volume = volume_var.get() / 100.0
        sound.active = active_var.get()
        sound.apply_settings()

        self.soundboard[new_key] = {
            "file": sound.file,
            "name": sound.name,
            "loop": sound.loop,
            "stop_others": sound.stop_others,
            "volume": sound.volume,
            "active": sound.active
        }

        if old_key != new_key:
            del self.soundboard[old_key]  

        save_config(self.soundboard)

        if edit_window:
            edit_window.destroy()

    def add_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        if file_path:
            key = os.path.basename(file_path)[0]
            if key in self.sounds:
                messagebox.showwarning("Warning", "The key is already assigned to a sound.")
                return

            sound = Sound(name=os.path.basename(file_path), file=file_path)
            self.sounds[key] = sound
            self.soundboard[key] = {
                "file": sound.file,
                "name": sound.name,
                "loop": sound.loop,
                "stop_others": sound.stop_others,
                "volume": sound.volume,
                "active": sound.active
            }
            save_config(self.soundboard)
            self.tree.insert("", "end", iid=key, text=key, values=(key, sound.file, sound.name, str(sound.loop), str(sound.stop_others), str(int(sound.volume * 100)), str(sound.active)))
            keyboard.add_hotkey(key, lambda k=key: self.play_sound(k))

    def remove_sound(self):
        selected_item = self.tree.selection()
        if selected_item:
            key = selected_item[0]
            del self.sounds[key]
            del self.soundboard[key]
            save_config(self.soundboard)
            self.tree.delete(key)
            keyboard.remove_hotkey(key)

    def setup_hotkeys(self):
        for key in self.sounds:
            keyboard.add_hotkey(key, lambda k=key: self.play_sound(k))
        keyboard.add_hotkey('e', lambda: pygame.mixer.stop())

    def play_sound(self, key):
        if self.shortcut_active.get() and key in self.sounds:
            self.sounds[key].play()

    def on_close(self):
        save_config(self.soundboard)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SoundboardApp(root)
    root.mainloop()