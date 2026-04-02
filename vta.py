import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from pathlib import Path

from modules.logger import log
from modules.ffmpeg_config import init_ffmpeg_path
from modules.converter import batch_convert


def choose_input_mode():
    result = {"choice": None}

    root = tk.Tk()
    root.title("Select input type")
    root.geometry("300x90")
    root.resizable(False, False)

    def select_file():
        result["choice"] = "file"
        root.destroy()

    def select_folder():
        result["choice"] = "folder"
        root.destroy()

    tk.Label(root, text="What would you like to convert?").pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()

    tk.Button(
        btn_frame, 
        text="File", 
        width=10, 
        command=select_file
    ).pack(side="left", padx=10)

    tk.Button(
        btn_frame, 
        text="Folder", 
        width=10, 
        command=select_folder
    ).pack(side="right", padx=10)

    root.mainloop()
    return result["choice"]


def pick_input():
    mode = choose_input_mode()

    if mode is None:
        log("No selection made. Operation cancelled.")
        return None

    root = tk.Tk()
    root.withdraw()

    if mode == "file":
        log("FILE input mode chosen.")

        log("Opening file picker. Select input file.")

        file_choice = filedialog.askopenfilename(
            title="Select video file"
        )

        if file_choice:
            log(f"File selected: {file_choice}")
            return Path(file_choice)

        log("No file selected. Cancelled.")
        return None

    elif mode == "folder":
        log("FOLDER input mode chosen.")

        log("Opening folder picker. Select input directory.")

        folder_choice = filedialog.askdirectory(
            title="Select input folder"
        )

        if folder_choice:
            log(f"Folder selected: {folder_choice}")
            return Path(folder_choice)

        log("No folder selected. Cancelled.")
        return None
    

def pick_output():
    root = tk.Tk()
    root.withdraw()

    log("Opening folder picker. Select output directory.")
    choice = filedialog.askdirectory(title="Select output folder")

    if choice:
        log(f"Output folder selected: {choice}")
        return Path(choice)

    log("No output folder selected. Operation cancelled.")
    return None


def main():
    log("VTA Start")

    init_ffmpeg_path()

    try:
        input_path = pick_input()
        if not input_path:
            return

        output_dir = pick_output()
        if not output_dir:
            return

        codec = "mp3"

        log("")

        log("Beginning conversion...")
        log(f"  Input:  {input_path}")
        log(f"  Output: {output_dir}")
        log(f"  Format: {codec}")

        results = batch_convert(
            input_path=input_path,
            output_dir=output_dir,
            codec=codec
        )

        files_word = "file" if len(results) == 1 else "files"

        log("")
        log(f"Conversion complete. {len(results)} {files_word} processed.")

        messagebox.showinfo(
            "Done",
            f"Converted {len(results)} {files_word} to {codec}"
        )

        log("")
        log("VTA End")

    except Exception as e:
        log(f"ERROR: {type(e).__name__}: {e}")
        messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    main()