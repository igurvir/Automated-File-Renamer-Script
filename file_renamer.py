import os
import datetime
import re
import tkinter as tk
from tkinter import filedialog, messagebox
import logging

# Set up logging
logging.basicConfig(filename='rename_log.txt', level=logging.INFO)

# Global dictionary to store renamed files
renamed_files = {}

def rename_files():
    directory = filedialog.askdirectory()
    if not directory:
        return

    # Retrieve user inputs
    prefix = prefix_var.get()
    suffix = suffix_var.get()
    replace_spaces = replace_spaces_var.get()
    add_date = add_date_var.get()
    sequential = sequential_var.get()
    regex_pattern = regex_pattern_var.get()
    replacement_text = replacement_text_var.get()

    try:
        files = os.listdir(directory)
        count = 1

        for file_name in files:
            if os.path.isfile(os.path.join(directory, file_name)):
                file_name_without_ext, file_extension = os.path.splitext(file_name)
                new_name = file_name_without_ext

                # Apply regex pattern if provided
                if regex_pattern:
                    new_name = re.sub(regex_pattern, replacement_text, new_name)

                if prefix:
                    new_name = prefix + new_name
                if suffix:
                    new_name = new_name + suffix
                if replace_spaces:
                    new_name = new_name.replace(" ", "_")
                if add_date:
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    new_name = f"{new_name}_{current_date}"
                if sequential:
                    new_name = f"{new_name}_{count:03d}"
                    count += 1

                new_name += file_extension
                old_file_path = os.path.join(directory, file_name)
                new_file_path = os.path.join(directory, new_name)

                # Store renamed files for undo functionality
                renamed_files[new_file_path] = old_file_path

                # Rename the file
                os.rename(old_file_path, new_file_path)

                # Log the renaming action
                logging.info(f"Renamed '{file_name}' to '{new_name}' at {datetime.datetime.now()}")

        messagebox.showinfo("Success", "All files renamed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during renaming: {str(e)}")

def undo_rename():
    try:
        for new_name, old_name in renamed_files.items():
            os.rename(new_name, old_name)
        renamed_files.clear()
        messagebox.showinfo("Undo Success", "Files have been reverted to their original names.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during undo: {str(e)}")

def setup_gui():
    global root, prefix_var, suffix_var, replace_spaces_var, add_date_var, sequential_var
    global regex_pattern_var, replacement_text_var

    root = tk.Tk()
    root.title("Advanced File Renamer")

    # Input fields and variables
    tk.Label(root, text="Prefix:").grid(row=0, column=0, sticky='e')
    prefix_var = tk.StringVar()
    tk.Entry(root, textvariable=prefix_var).grid(row=0, column=1)

    tk.Label(root, text="Suffix:").grid(row=1, column=0, sticky='e')
    suffix_var = tk.StringVar()
    tk.Entry(root, textvariable=suffix_var).grid(row=1, column=1)

    replace_spaces_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Replace spaces with underscores", variable=replace_spaces_var).grid(row=2, columnspan=2)

    add_date_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Add current date", variable=add_date_var).grid(row=3, columnspan=2)

    sequential_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Rename sequentially", variable=sequential_var).grid(row=4, columnspan=2)

    tk.Label(root, text="Regex Pattern:").grid(row=5, column=0, sticky='e')
    regex_pattern_var = tk.StringVar()
    tk.Entry(root, textvariable=regex_pattern_var).grid(row=5, column=1)

    tk.Label(root, text="Replacement Text:").grid(row=6, column=0, sticky='e')
    replacement_text_var = tk.StringVar()
    tk.Entry(root, textvariable=replacement_text_var).grid(row=6, column=1)

    tk.Button(root, text="Select Folder and Rename", command=rename_files).grid(row=7, columnspan=2, pady=5)
    tk.Button(root, text="Undo Last Rename", command=undo_rename).grid(row=8, columnspan=2)

    # Add padding to all widgets
    for widget in root.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()
