
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import queue
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ffmpeg Audio Converter")

        # --- Set Icon ---
        try:
            icon_path = resource_path('app_icon.ico')
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")

        self.root.geometry("700x600")

        self.input_files = []
        self.output_dir = ""
        self.output_format = tk.StringVar(value="mp3")
        self.quality_var = tk.StringVar(value="192 kbps")
        self.queue = queue.Queue()

        # --- Main Frame ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Input Selection ---
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.select_files_btn = ttk.Button(input_frame, text="1. Select Audio Files", command=self.select_files)
        self.select_files_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.files_listbox = tk.Listbox(main_frame, height=8, selectmode=tk.EXTENDED)
        self.files_listbox.pack(fill=tk.X, pady=5)

        # --- Output Selection ---
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=10)

        self.select_dir_btn = ttk.Button(output_frame, text="2. Select Output Directory", command=self.select_output_dir)
        self.select_dir_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.output_dir_label = ttk.Label(output_frame, text="No directory selected...")
        self.output_dir_label.pack(side=tk.LEFT)

        # --- Format and Quality Frame ---
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)

        # --- Format Selection ---
        format_label = ttk.Label(options_frame, text="3. Output Format:")
        format_label.pack(side=tk.LEFT, padx=(0, 10))

        self.format_menu = ttk.Combobox(options_frame, textvariable=self.output_format, state="readonly",
                                      values=["mp3", "aac", "ogg", "m4a", "wav", "flac"])
        self.format_menu.pack(side=tk.LEFT, padx=(0, 20))
        self.format_menu.bind("<<ComboboxSelected>>", self.on_format_change)

        # --- Quality Selection ---
        quality_label = ttk.Label(options_frame, text="Quality:")
        quality_label.pack(side=tk.LEFT, padx=(10, 10))

        self.quality_menu = ttk.Combobox(options_frame, textvariable=self.quality_var, state="readonly",
                                       values=["Best (VBR)", "320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps"])
        self.quality_menu.pack(side=tk.LEFT)

        # --- Conversion Button ---
        self.convert_btn = ttk.Button(main_frame, text="4. Convert", command=self.start_conversion_thread)
        self.convert_btn.pack(pady=10)

        # --- Status/Log Area ---
        log_label = ttk.Label(main_frame, text="Conversion Log:")
        log_label.pack(fill=tk.X, pady=(10, 0))

        self.log_area = tk.Text(main_frame, height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.on_format_change() # Set initial state of quality menu
        self.root.after(100, self.process_queue)

    def on_format_change(self, event=None):
        # Enable quality menu only for formats that typically use bitrate settings
        selected_format = self.output_format.get()
        if selected_format in ["mp3", "aac", "ogg", "m4a"]:
            self.quality_menu.config(state="readonly")
        else: # For lossless like wav, flac
            self.quality_menu.config(state="disabled")

    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=(("All Supported", "*.m4a *.mp3 *.wav *.ogg *.flac *.aac *.avi *.mp4 *.mkv"),
                       ("All files", "*.*"))
        )
        if files:
            self.input_files.extend(files)
            self.update_files_listbox()

    def update_files_listbox(self):
        self.files_listbox.delete(0, tk.END)
        for f in self.input_files:
            self.files_listbox.insert(tk.END, os.path.basename(f))

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir = directory
            self.output_dir_label.config(text=self.output_dir)

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_conversion_thread(self):
        if not self.input_files:
            messagebox.showerror("Error", "No input files selected.")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "No output directory selected.")
            return

        self.convert_btn.config(state=tk.DISABLED)
        self.select_files_btn.config(state=tk.DISABLED)
        self.select_dir_btn.config(state=tk.DISABLED)

        self.log("--- Starting Conversion ---")
        thread = threading.Thread(target=self.convert_files, daemon=True)
        thread.start()

    def convert_files(self):
        try:
            for i, input_file in enumerate(self.input_files):
                base_name = os.path.basename(input_file)
                file_name_no_ext = os.path.splitext(base_name)[0]
                output_format = self.output_format.get()
                quality = self.quality_var.get()
                output_file = os.path.join(self.output_dir, f"{file_name_no_ext}.{output_format}")

                self.queue.put(f"({i+1}/{len(self.input_files)}) Converting '{base_name}'...")

                command = [
                    'ffmpeg',
                    '-i', input_file,
                    '-y',      # Overwrite output file
                    '-vn',    # No video
                ]

                # --- Add Codec and Quality Flags ---
                if output_format == 'mp3':
                    command.extend(['-c:a', 'libmp3lame'])
                    if 'VBR' in quality:
                        command.extend(['-q:a', '0']) # Highest quality VBR
                    else:
                        bitrate = quality.split(' ')[0] + 'k'
                        command.extend(['-b:a', bitrate])
                elif output_format == 'aac':
                    command.extend(['-c:a', 'aac'])
                    if 'VBR' in quality:
                        command.extend(['-q:a', '2']) # High quality VBR for AAC
                    else:
                        bitrate = quality.split(' ')[0] + 'k'
                        command.extend(['-b:a', bitrate])
                elif output_format == 'ogg':
                    command.extend(['-c:a', 'libvorbis'])
                    if 'VBR' in quality:
                        command.extend(['-q:a', '6']) # Quality level 6/10 for Vorbis
                    else:
                        bitrate = quality.split(' ')[0] + 'k'
                        command.extend(['-b:a', bitrate])
                elif output_format == 'm4a':
                    command.extend(['-c:a', 'aac'])
                    if 'VBR' in quality:
                        command.extend(['-q:a', '2'])
                    else:
                        bitrate = quality.split(' ')[0] + 'k'
                        command.extend(['-b:a', bitrate])
                elif output_format == 'wav':
                    command.extend(['-c:a', 'pcm_s16le']) # No quality settings for WAV
                elif output_format == 'flac':
                    command.extend(['-c:a', 'flac']) # No quality settings for FLAC

                command.append(output_file)
                
                startupinfo = None
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo, encoding='utf-8', errors='replace')
                
                # Capture and log stderr for progress, but don't block
                for line in iter(process.stderr.readline, ''):
                    self.queue.put(line.strip())
                
                process.wait()

                if process.returncode == 0:
                    self.queue.put(f"SUCCESS: Converted to '{os.path.basename(output_file)}'")
                else:
                    # Reread stderr in case of error
                    error_output = process.stderr.read()
                    self.queue.put(f"ERROR converting '{base_name}':\n{error_output}")

            self.queue.put("--- Conversion Complete ---")
        except Exception as e:
            self.queue.put(f"An unexpected error occurred: {e}")
        finally:
            self.queue.put("DONE")

    def process_queue(self):
        try:
            while True:
                message = self.queue.get_nowait()
                if message == "DONE":
                    self.convert_btn.config(state=tk.NORMAL)
                    self.select_files_btn.config(state=tk.NORMAL)
                    self.select_dir_btn.config(state=tk.NORMAL)
                    self.input_files = []
                    self.update_files_listbox()
                else:
                    self.log(message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)


if __name__ == "__main__":
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        messagebox.showerror("ffmpeg Not Found", 
                             "ffmpeg is not installed or not in your system's PATH.\n"
                             "Please install ffmpeg to use this application.")
        exit()

    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
