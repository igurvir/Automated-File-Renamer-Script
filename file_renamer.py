import tkinter as tk
from tkinter import filedialog, messagebox
import os
import datetime
import re
import logging

# Set up logging
logging.basicConfig(filename='rename_log.txt', level=logging.INFO)

# Global dictionary to store renamed files
renamed_files = {}

# Function to apply regex based on user selection
def apply_predefined_regex(file_name, regex_option):
    if regex_option == "Remove numbers":
        return re.sub(r'\d+', '', file_name)
    elif regex_option == "Replace spaces with underscores":
        return re.sub(r'\s+', '_', file_name)
    elif regex_option == "Remove special characters":
        return re.sub(r'[^\w\s]', '', file_name)
    elif regex_option == "Append '_updated' before extension":
        return re.sub(r'(.*)', r'\1_updated', file_name)
    return file_name

# Function to rename files
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
    regex_option = regex_option_var.get()  # Get selected regex option

    count = 0  # Counter for renamed files

    try:
        files = os.listdir(directory)
        file_count = len([f for f in files if os.path.isfile(os.path.join(directory, f))])

        for file_name in files:
            if os.path.isfile(os.path.join(directory, file_name)):
                file_name_without_ext, file_extension = os.path.splitext(file_name)
                new_name = file_name_without_ext

                # Apply predefined regex if selected
                new_name = apply_predefined_regex(new_name, regex_option)

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
                    new_name = f"{new_name}_{count + 1:03d}"

                new_name += file_extension
                old_file_path = os.path.join(directory, file_name)
                new_file_path = os.path.join(directory, new_name)

                # Store renamed files for undo functionality
                renamed_files[new_file_path] = old_file_path

                # Rename the file
                os.rename(old_file_path, new_file_path)
                logging.info(f"Renamed '{file_name}' to '{new_name}' at {datetime.datetime.now()}")

                count += 1

        messagebox.showinfo("Success", f"{count} files renamed successfully.")
        modified_files_var.set(f"{count} out of {file_count} files modified")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during renaming: {str(e)}")

# Undo function to rename files back to their original names
def undo_rename():
    try:
        for new_name, old_name in renamed_files.items():
            os.rename(new_name, old_name)
        renamed_files.clear()
        messagebox.showinfo("Undo Success", "Files have been reverted to their original names.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during undo: {str(e)}")

# Create the GUI
def setup_gui():
    global root, prefix_var, suffix_var, replace_spaces_var, add_date_var, sequential_var
    global regex_option_var, replacement_text_var, modified_files_var

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

    # Predefined regex options
    tk.Label(root, text="Predefined Regex Options:").grid(row=5, column=0, sticky='e')
    regex_option_var = tk.StringVar(value="None")
    regex_options = ["None", "Remove numbers", "Replace spaces with underscores", "Remove special characters", "Append '_updated' before extension"]
    tk.OptionMenu(root, regex_option_var, *regex_options).grid(row=5, column=1)

    # Label to show the number of modified files
    modified_files_var = tk.StringVar(value="0 files modified")
    tk.Label(root, textvariable=modified_files_var).grid(row=7, columnspan=2)

    # Buttons
    tk.Button(root, text="Select Folder and Rename", command=rename_files).grid(row=6, columnspan=2, pady=5)
    tk.Button(root, text="Undo Last Rename", command=undo_rename).grid(row=8, columnspan=2)

    # Add padding to all widgets
    for widget in root.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    setup_gui()
