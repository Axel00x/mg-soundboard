import os
import pygame
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import keyboard
import pyaudio
from pytube import YouTube
import webbrowser

from dep.config import *
from dep.settings import *

pygame.mixer.init()

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
        self.channel = None
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
            self.channel = self.sound.play(-1)
        else:
            self.channel = self.sound.play()

    def stop(self):
        if self.sound:
            self.sound.stop()
            self.channel = None

class SoundboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"mg-soundboard (v{program_version})")
        self.root.configure(bg="#e6e6e6")
        self.soundboard = load_config()
        self.sounds = {key: Sound(**settings) for key, settings in self.soundboard.items()}
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=('Arial', 10), padding=5)
        style.configure("TLabel", font=('Arial', 10), background="#e6e6e6")
        style.configure("Treeview", foreground="black", background="white", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#cccccc", foreground="black")
        self.tree = ttk.Treeview(root, columns=("Key", "File", "Name", "Loop", "Stop Others", "Volume", "Active", "Action"), show='headings')
        self.tree.heading("Key", text="Key")
        self.tree.heading("File", text="File")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Loop", text="Loop")
        self.tree.heading("Stop Others", text="Stop Others")
        self.tree.heading("Volume", text="Volume")
        self.tree.heading("Active", text="Active")
        self.tree.heading("Action", text="Play")
        self.tree.column("Action", width=50, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.tag_configure("playing", background="#d1ffd1", foreground="blue")
        for key, sound in self.sounds.items():
            self.tree.insert("", "end", iid=key, text=key, values=(key, sound.file, sound.name, str(sound.loop), str(sound.stop_others), str(int(sound.volume * 100)), str(sound.active), "Play"))
        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.tree.bind("<Button-1>", self.on_treeview_click)
        self.shortcut_active = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text="Shortcut", variable=self.shortcut_active, bg="#e6e6e6", font=('Arial', 10)).pack(pady=(0,10))
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        pa = pyaudio.PyAudio()
        self.audio_devices = []
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if info.get('maxOutputChannels', 0) > 0:
                self.audio_devices.append(info.get('name'))
        pa.terminate()
        if not self.audio_devices:
            self.audio_devices = ["Default"]
        self.device_var = tk.StringVar()
        self.device_var.set(self.audio_devices[0])
        ttk.Label(top_frame, text="Audio Output Device:").pack(side=tk.LEFT, padx=(0, 5))
        self.device_combo = ttk.Combobox(top_frame, textvariable=self.device_var, values=self.audio_devices, state="readonly")
        self.device_combo.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(top_frame, text="Set Audio Device", command=self.set_audio_device).pack(side=tk.LEFT, padx=(0, 5))
        button_frame = ttk.Frame(self.root)
        button_frame.pack(padx=10, pady=5)
        ttk.Button(button_frame, text="Add Sound", command=self.add_sound).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Sound", command=self.remove_sound).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Import from YouTube", command=self.import_from_youtube).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Site", command=self.open_site).pack(side=tk.LEFT, padx=5)
        self.setup_hotkeys()
        self.auto_apply_settings()
        self.check_playing_status()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def auto_apply_settings(self):
        for key in self.sounds.keys():
            sound = self.sounds[key]
            self.save_changes(key, key, sound.name, tk.BooleanVar(value=sound.loop), tk.BooleanVar(value=sound.stop_others), tk.IntVar(value=int(sound.volume * 100)), tk.BooleanVar(value=sound.active), None)

    def check_playing_status(self):
        for item in self.tree.get_children():
            sound = self.sounds[item]
            playing = sound.channel is not None and sound.channel.get_busy()
            if playing:
                self.tree.item(item, tags=("playing",))
            else:
                self.tree.item(item, tags=())
        self.root.after(500, self.check_playing_status)

    def on_treeview_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            if col == "#8":
                item_id = self.tree.identify_row(event.y)
                if item_id:
                    self.play_sound(item_id)

    def on_item_double_click(self, event):
        item_id = self.tree.selection()[0]
        sound = self.sounds[item_id]
        item = self.tree.item(item_id)
        values = item['values']
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Modify {item_id}")
        edit_window.columnconfigure(0, weight=1)
        edit_window.columnconfigure(1, weight=2)
        for i in range(7):
            edit_window.rowconfigure(i, weight=1)
        label_font = ('Arial', 10, 'bold')
        entry_font = ('Arial', 10)
        padding = 10
        ttk.Label(edit_window, text="Name", font=label_font).grid(row=0, column=0, padx=padding, pady=padding, sticky="e")
        name_var = tk.StringVar(value=sound.name)
        ttk.Entry(edit_window, textvariable=name_var, font=entry_font).grid(row=0, column=1, padx=padding, pady=padding, sticky="w")
        ttk.Label(edit_window, text="Shortcut", font=label_font).grid(row=1, column=0, padx=padding, pady=padding, sticky="e")
        key_var = tk.StringVar(value=item_id)
        ttk.Entry(edit_window, textvariable=key_var, font=entry_font).grid(row=1, column=1, padx=padding, pady=padding, sticky="w")
        ttk.Label(edit_window, text="Loop", font=label_font).grid(row=2, column=0, padx=padding, pady=padding, sticky="e")
        loop_var = tk.BooleanVar(value=values[3] == "True")
        ttk.Checkbutton(edit_window, variable=loop_var).grid(row=2, column=1, padx=padding, pady=padding, sticky="w")
        ttk.Label(edit_window, text="Stop Other Sounds", font=label_font).grid(row=3, column=0, padx=padding, pady=padding, sticky="e")
        stop_var = tk.BooleanVar(value=values[4] == "True")
        ttk.Checkbutton(edit_window, variable=stop_var).grid(row=3, column=1, padx=padding, pady=padding, sticky="w")
        ttk.Label(edit_window, text="Volume (0-100)", font=label_font).grid(row=4, column=0, padx=padding, pady=padding, sticky="e")
        volume_var = tk.IntVar(value=int(values[5]))
        ttk.Scale(edit_window, variable=volume_var, from_=0, to=100, orient=tk.HORIZONTAL).grid(row=4, column=1, padx=padding, pady=padding, sticky="w")
        ttk.Label(edit_window, text="Active", font=label_font).grid(row=5, column=0, padx=padding, pady=padding, sticky="e")
        active_var = tk.BooleanVar(value=values[6] == "True")
        ttk.Checkbutton(edit_window, variable=active_var).grid(row=5, column=1, padx=padding, pady=padding, sticky="w")
        ttk.Button(edit_window, text="Save", command=lambda: self.save_changes(item_id, key_var.get(), name_var.get(), loop_var, stop_var, volume_var, active_var, edit_window)).grid(row=6, column=0, columnspan=2, pady=padding)

    def save_changes(self, old_key, new_key, new_name, loop_var, stop_var, volume_var, active_var, edit_window):
        if old_key != new_key:
            if new_key in self.sounds:
                messagebox.showerror("Error", "The chosen shortcut is already in use!")
                return
            self.sounds[new_key] = self.sounds.pop(old_key)
            self.tree.delete(old_key)
            self.tree.insert("", "end", iid=new_key, text=new_key, values=(new_key, self.sounds[new_key].file, new_name, str(loop_var.get()), str(stop_var.get()), str(volume_var.get()), str(active_var.get()), "Play"))
            keyboard.remove_hotkey(old_key)
            keyboard.add_hotkey(new_key, lambda k=new_key: self.play_sound(k))
        else:
            self.tree.item(old_key, values=(new_key, self.sounds[old_key].file, new_name, str(loop_var.get()), str(stop_var.get()), str(volume_var.get()), str(active_var.get()), "Play"))
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
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
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
            self.tree.insert("", "end", iid=key, text=key, values=(key, sound.file, sound.name, str(sound.loop), str(sound.stop_others), str(int(sound.volume * 100)), str(sound.active), "Play"))
            keyboard.add_hotkey(key, lambda k=key: self.play_sound(k))

    def remove_sound(self):
        selected_item = self.tree.selection()
        if selected_item:
            key = selected_item[0]
            if not messagebox.askyesno("Confirm", "Are you sure you want to remove this sound?"):
                return
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

    def set_audio_device(self):
        selected_device = self.device_var.get()
        pygame.mixer.quit()
        
        try:
            pygame.mixer.init(devicename=selected_device)
            print(f"Audio device successfully set: {selected_device}")
        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Failed to set audio device '{selected_device}'. Reverting to default.\nError: {e}"
            )
            try:
                pygame.mixer.init()
                if self.audio_devices:
                    self.device_var.set(self.audio_devices[0])  
                print("Reverted to default audio device.")
            except Exception as e:
                messagebox.showerror("Critical Error", f"Could not initialize the mixer. {e}")
                return 
        
        for key, sound in self.sounds.items():
            try:
                sound.sound = pygame.mixer.Sound(sound.file)  
                sound.apply_settings()  
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reload sound {sound.file}.\nError: {e}")
        
        print("All sounds have been successfully reloaded.")


    def import_from_youtube(self):
        url = simpledialog.askstring("YouTube URL", "Enter YouTube video URL:")
        if not url:
            return
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            if not os.path.exists("downloads"):
                os.makedirs("downloads")
            file_path = stream.download(output_path="downloads")
            key = simpledialog.askstring("Shortcut Key", "Enter shortcut key for this sound:")
            if not key:
                key = os.path.basename(file_path)[0]
            if key in self.sounds:
                messagebox.showerror("Error", "The chosen shortcut is already in use!")
                return
            sound = Sound(name=yt.title, file=file_path)
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
            self.tree.insert("", "end", iid=key, text=key, values=(key, sound.file, sound.name, str(sound.loop), str(sound.stop_others), str(int(sound.volume * 100)), str(sound.active), "Play"))
            keyboard.add_hotkey(key, lambda k=key: self.play_sound(k))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import from YouTube: {str(e)}")
    
    def open_site(self):
        webbrowser.open_new_tab("file:///"+ os.getcwd() + '/' + "src/site/index.htm")
    
    def on_close(self):
        save_config(self.soundboard)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SoundboardApp(root)
    root.mainloop()
