import tkinter as tk
from tkinter import filedialog, messagebox
import os
import datetime
import re
import logging
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES  # Using TkinterDnD2 for drag-and-drop support

# Set up logging
logging.basicConfig(filename='rename_log.txt', level=logging.INFO)

# Global dictionary to store renamed files
renamed_files = {}
directory = None  # Global variable to store the dragged directory path

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

# Function to check if file already exists, handling case sensitivity
def file_exists_ignore_case(new_file_path, directory):
    # Get a list of all files in the directory
    existing_files = os.listdir(directory)
    # Normalize case for comparison
    existing_files_lower = [f.lower() for f in existing_files]
    # Compare in a case-insensitive way
    return os.path.basename(new_file_path).lower() in existing_files_lower

# Function to filter files based on user input file extensions
def filter_files(files, filter_extensions):
    if not filter_extensions:  # If no filter, return all files
        return files
    valid_extensions = [ext.strip().lower() for ext in filter_extensions.split(',')]  # Split user input
    return [f for f in files if os.path.splitext(f)[1].lower() in valid_extensions]

# Function to rename files (running on a separate thread)
def rename_files():
    global directory
    if not directory:
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
    find_text = find_var.get()  # Get the text to find
    replace_text = replace_var.get()  # Get the replacement text
    filter_extensions = file_filter_var.get()  # Get the file extension filter

    count = 0  # Counter for renamed files

    try:
        files = os.listdir(directory)
        file_count = len([f for f in files if os.path.isfile(os.path.join(directory, f))])

        # Apply the file filter
        files = filter_files(files, filter_extensions)

        for file_name in files:
            if os.path.isfile(os.path.join(directory, file_name)):

                # Skip hidden files (those that start with a dot, e.g., .DS_Store)
                if file_name.startswith('.'):
                    continue

                file_name_without_ext, file_extension = os.path.splitext(file_name)
                new_name = file_name_without_ext

                # Apply Find and Replace first
                if find_text and replace_text:
                    new_name = new_name.replace(find_text, replace_text)

                # Apply predefined regex if selected
                new_name = apply_predefined_regex(new_name, regex_option)

                # Apply prefix and suffix
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

                # Check if the new file name already exists to prevent overwriting (case-insensitive)
                if file_exists_ignore_case(new_file_path, directory):
                    messagebox.showwarning("Warning", f"The file '{new_name}' already exists. Skipping.")
                    continue  # Skip this file to avoid overwriting

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

# Threaded function to prevent blocking the GUI
def start_renaming_thread():
    threading.Thread(target=rename_files).start()

# Undo function to rename files back to their original names
def undo_rename():
    try:
        for new_name, old_name in renamed_files.items():
            # Skip hidden files (those that start with a dot, e.g., .DS_Store)
            if os.path.basename(new_name).startswith('.'):
                continue
            os.rename(new_name, old_name)
        renamed_files.clear()
        messagebox.showinfo("Undo Success", "Files have been reverted to their original names.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during undo: {str(e)}")

# Drag-and-drop handler for directory
def on_drop(event):
    global directory
    directory = event.data.strip('{}')  # Strip the curly braces from the dropped path
    dropped_dir_label.config(text=f"Folder selected: {directory}")
    rename_button.config(text="Rename")  # Change button text to 'Rename'
    remove_folder_button.grid(row=13, columnspan=2, pady=5)  # Show the 'Remove Folder' button

# Remove selected folder
def remove_folder():
    global directory
    directory = None  # Reset the directory variable
    dropped_dir_label.config(text="Drag a folder here or select it using the button above")
    rename_button.config(text="Select Folder and Rename")  # Revert button text to 'Select Folder and Rename'
    remove_folder_button.grid_forget()  # Hide the 'Remove Folder' button

# Create the GUI
def setup_gui():
    global root, prefix_var, suffix_var, replace_spaces_var, add_date_var, sequential_var
    global regex_option_var, modified_files_var, dropped_dir_label, rename_button, remove_folder_button
    global find_var, replace_var, file_filter_var  # Variables for find and replace, and file filter

    root = TkinterDnD.Tk()  # Initialize TkinterDnD root window
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

    # Find and replace inputs
    tk.Label(root, text="Find:").grid(row=6, column=0, sticky='e')
    find_var = tk.StringVar()
    tk.Entry(root, textvariable=find_var).grid(row=6, column=1)

    tk.Label(root, text="Replace with:").grid(row=7, column=0, sticky='e')
    replace_var = tk.StringVar()
    tk.Entry(root, textvariable=replace_var).grid(row=7, column=1)

    # File filter input
    tk.Label(root, text="File Filter (e.g., .txt, .png):").grid(row=8, column=0, sticky='e')
    file_filter_var = tk.StringVar()
    tk.Entry(root, textvariable=file_filter_var).grid(row=8, column=1)

    # Label to show the number of modified files
    modified_files_var = tk.StringVar(value="0 files modified")
    tk.Label(root, textvariable=modified_files_var).grid(row=10, columnspan=2)

    # Rename button
    rename_button = tk.Button(root, text="Select Folder and Rename", command=start_renaming_thread)
    rename_button.grid(row=9, columnspan=2, pady=5)

    # Undo button
    tk.Button(root, text="Undo Last Rename", command=undo_rename).grid(row=11, columnspan=2)

    # Label to display the dropped directory
    dropped_dir_label = tk.Label(root, text="Drag a folder here or select it using the button above")
    dropped_dir_label.grid(row=12, columnspan=2, pady=10)

    # 'Remove Folder' button (initially hidden)
    remove_folder_button = tk.Button(root, text="Remove Folder", command=remove_folder)
    remove_folder_button.grid_forget()  # Hide this button initially

    # Add padding to all widgets
    for widget in root.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    # Bind the drop event to the root window
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    setup_gui()
