import tkinter as tk
from tkinter import filedialog, messagebox
import os
import datetime
import re
import logging
import threading
from tkinterdnd2 import TkinterDnD, DND_FILES  # Adding drag-and-drop support for folders

# Set up logging to save the renaming process in a file
logging.basicConfig(filename='rename_log.txt', level=logging.INFO)

# Dictionary to keep track of renamed files (for undo)
renamed_files = {}
directory = None  # This will hold the folder path we are working with

# Function to handle different renaming options chosen by the user (e.g., remove numbers)
def apply_predefined_regex(file_name, regex_option):
    if regex_option == "Remove numbers":
        return re.sub(r'\d+', '', file_name)  # Remove all numbers from the file name
    elif regex_option == "Replace spaces with underscores":
        return re.sub(r'\s+', '_', file_name)  # Replace spaces with underscores
    elif regex_option == "Remove special characters":
        return re.sub(r'[^\w\s]', '', file_name)  # Remove special characters (e.g., !, @, #)
    elif regex_option == "Append '_updated' before extension":
        return re.sub(r'(.*)', r'\1_updated', file_name)  # Add '_updated' to the end of the file name
    return file_name  # Return the original file name if no option was selected

# Function to check if a file with the new name already exists (ignores uppercase/lowercase differences)
def file_exists_ignore_case(new_file_path, directory):
    existing_files = os.listdir(directory)  # Get all the files in the folder
    existing_files_lower = [f.lower() for f in existing_files]  # Convert file names to lowercase
    return os.path.basename(new_file_path).lower() in existing_files_lower  # Check if the new name exists

# Function to filter files based on the extension types the user specified (e.g., .txt, .png)
def filter_files(files, filter_extensions):
    if not filter_extensions:  # If no file type was provided, return all files
        return files
    valid_extensions = [ext.strip().lower() for ext in filter_extensions.split(',')]  # Split and clean extensions
    return [f for f in files if os.path.splitext(f)[1].lower() in valid_extensions]  # Return files with valid types

# Function to rename files in a separate thread so the program doesn't freeze
def rename_files():
    global directory
    if not directory:  # Ask the user to select a folder if no folder was dragged
        directory = filedialog.askdirectory()
    if not directory:  # If no folder was selected, exit the function
        return

    # Get the user inputs from the form
    prefix = prefix_var.get()
    suffix = suffix_var.get()
    replace_spaces = replace_spaces_var.get()
    add_date = add_date_var.get()
    sequential = sequential_var.get()
    regex_option = regex_option_var.get()  # Get the renaming option
    find_text = find_var.get()  # Text to find and replace
    replace_text = replace_var.get()  # Text to replace with
    filter_extensions = file_filter_var.get()  # Get the file types the user specified

    count = 0  # Keep track of how many files were renamed

    try:
        files = os.listdir(directory)  # List all files in the selected folder
        file_count = len([f for f in files if os.path.isfile(os.path.join(directory, f))])  # Count the files

        # Apply the file type filter (only keep files with the chosen extensions)
        files = filter_files(files, filter_extensions)

        for file_name in files:
            if os.path.isfile(os.path.join(directory, file_name)):

                # Skip hidden files (files that start with a dot, like .DS_Store)
                if file_name.startswith('.'):
                    continue

                file_name_without_ext, file_extension = os.path.splitext(file_name)  # Separate name and extension
                new_name = file_name_without_ext

                # Apply "find and replace" if the user has entered any
                if find_text and replace_text:
                    new_name = new_name.replace(find_text, replace_text)

                # Apply the selected renaming option (like removing numbers)
                new_name = apply_predefined_regex(new_name, regex_option)

                # Add the prefix and suffix to the new file name
                if prefix:
                    new_name = prefix + new_name
                if suffix:
                    new_name = new_name + suffix
                if replace_spaces:
                    new_name = new_name.replace(" ", "_")  # Replace spaces with underscores
                if add_date:
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    new_name = f"{new_name}_{current_date}"  # Add the current date to the file name
                if sequential:
                    new_name = f"{new_name}_{count + 1:03d}"  # Add a sequential number (e.g., 001, 002)

                new_name += file_extension  # Reattach the file extension
                old_file_path = os.path.join(directory, file_name)
                new_file_path = os.path.join(directory, new_name)

                # Check if the new file name already exists, skip if it does
                if file_exists_ignore_case(new_file_path, directory):
                    messagebox.showwarning("Warning", f"The file '{new_name}' already exists. Skipping.")
                    continue  # Skip renaming this file

                # Store the renamed file in the dictionary so it can be undone later
                renamed_files[new_file_path] = old_file_path

                # Rename the file
                os.rename(old_file_path, new_file_path)
                logging.info(f"Renamed '{file_name}' to '{new_name}' at {datetime.datetime.now()}")

                count += 1  # Increment the count of renamed files

        # Show a success message and update the file count
        messagebox.showinfo("Success", f"{count} files renamed successfully.")
        modified_files_var.set(f"{count} out of {file_count} files modified")
    except Exception as e:  # Show an error message if something goes wrong
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during renaming: {str(e)}")

# Run the renaming in a separate thread to keep the app responsive
def start_renaming_thread():
    threading.Thread(target=rename_files).start()

# Undo the renaming (rename files back to their original names)
def undo_rename():
    try:
        for new_name, old_name in renamed_files.items():
            # Skip hidden files (files that start with a dot, like .DS_Store)
            if os.path.basename(new_name).startswith('.'):
                continue
            os.rename(new_name, old_name)  # Rename files back to their original names
        renamed_files.clear()  # Clear the undo list after undoing
        messagebox.showinfo("Undo Success", "Files have been reverted to their original names.")
    except Exception as e:  # Show an error message if something goes wrong
        messagebox.showerror("Error", str(e))
        logging.error(f"Error during undo: {str(e)}")

# Handle the folder drag-and-drop event
def on_drop(event):
    global directory
    directory = event.data.strip('{}')  # Get the dropped folder path
    dropped_dir_label.config(text=f"Folder selected: {directory}")  # Update the label with the folder name
    rename_button.config(text="Rename")  # Change the button text to "Rename"
    remove_folder_button.grid(row=13, columnspan=2, pady=5)  # Show the "Remove Folder" button

# Remove the selected folder
def remove_folder():
    global directory
    directory = None  # Clear the folder path
    dropped_dir_label.config(text="Drag a folder here or select it using the button above")  # Update the label
    rename_button.config(text="Select Folder and Rename")  # Change the button text back
    remove_folder_button.grid_forget()  # Hide the "Remove Folder" button

# Set up the graphical interface
def setup_gui():
    global root, prefix_var, suffix_var, replace_spaces_var, add_date_var, sequential_var
    global regex_option_var, modified_files_var, dropped_dir_label, rename_button, remove_folder_button
    global find_var, replace_var, file_filter_var  # Variables for renaming options and file filters

    root = TkinterDnD.Tk()  # Create the main window with drag-and-drop support
    root.title("Advanced File Renamer")

    # Input fields and variables for renaming options
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

    # Predefined renaming options
    tk.Label(root, text="Predefined Regex Options:").grid(row=5, column=0, sticky='e')
    regex_option_var = tk.StringVar(value="None")
    regex_options = ["None", "Remove numbers", "Replace spaces with underscores", "Remove special characters", "Append '_updated' before extension"]
    tk.OptionMenu(root, regex_option_var, *regex_options).grid(row=5, column=1)

    # Find and replace input fields
    tk.Label(root, text="Find:").grid(row=6, column=0, sticky='e')
    find_var = tk.StringVar()
    tk.Entry(root, textvariable=find_var).grid(row=6, column=1)

    tk.Label(root, text="Replace with:").grid(row=7, column=0, sticky='e')
    replace_var = tk.StringVar()
    tk.Entry(root, textvariable=replace_var).grid(row=7, column=1)

    # File filter input field
    tk.Label(root, text="File Filter (e.g., .txt, .png):").grid(row=8, column=0, sticky='e')
    file_filter_var = tk.StringVar()
    tk.Entry(root, textvariable=file_filter_var).grid(row=8, column=1)

    # Label to show how many files were renamed
    modified_files_var = tk.StringVar(value="0 files modified")
    tk.Label(root, textvariable=modified_files_var).grid(row=10, columnspan=2)

    # Rename button
    rename_button = tk.Button(root, text="Select Folder and Rename", command=start_renaming_thread)
    rename_button.grid(row=9, columnspan=2, pady=5)

    # Undo button
    tk.Button(root, text="Undo Last Rename", command=undo_rename).grid(row=11, columnspan=2)

    # Label for showing the selected folder
    dropped_dir_label = tk.Label(root, text="Drag a folder here or select it using the button above")
    dropped_dir_label.grid(row=12, columnspan=2, pady=10)

    # Button to remove the selected folder (initially hidden)
    remove_folder_button = tk.Button(root, text="Remove Folder", command=remove_folder)
    remove_folder_button.grid_forget()  # Hide this button initially

    # Add some padding to make the interface look nicer
    for widget in root.winfo_children():
        widget.grid_configure(padx=5, pady=5)

    # Enable drag-and-drop functionality
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', on_drop)

    root.mainloop()

# Run the graphical interface
if __name__ == "__main__":
    setup_gui()
