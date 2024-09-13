# File Renamer Script

This Python script automates the process of renaming files in a directory based on user-defined rules. The script provides a user-friendly interface with advanced options like adding prefixes, suffixes, replacing text, appending dates, and sequential renaming. It also supports drag-and-drop functionality, regex-based renaming, file filtering by extension, and undoing the renaming action.

## Features

### 1. Add Prefix or Suffix
You can easily add a custom prefix or suffix to all file names in a folder. This is useful when you want to organize files by adding specific labels at the beginning or end of file names.

### 2. Replace Spaces with Underscores
Automatically replace all spaces in file names with underscores for better readability or compliance with naming conventions that don't allow spaces.

### 3. Find and Replace Text
Specify a portion of the file name to be replaced with something else. For example, replace "image" with "photo" in all file names.

### 4. Append Date
Add the current date (YYYY-MM-DD) to the file names. This is helpful for organizing files based on when they were modified or processed.

### 5. Sequential Renaming
Automatically number files in the directory sequentially. Ideal for when you have multiple files and want them ordered numerically.

### 6. Predefined Regex Options
The script offers regex-based renaming with pre-configured options such as:
- **Remove Numbers**: Strip numbers from file names.
- **Replace Spaces with Underscores**: Automatically replaces spaces with underscores.
- **Remove Special Characters**: Removes special characters like `!`, `@`, `#`, etc.
- **Append `_updated`**: Adds `_updated` before the file extension.

### 7. File Extension Filtering
Filter which files get renamed based on file type (e.g., `.txt`, `.jpg`). You can specify multiple file types separated by commas.

### 8. Drag-and-Drop Folder Selection
You can simply drag and drop a folder into the interface, making it easy to select directories for renaming.

### 9. Undo Renaming
If you make a mistake, the "Undo" feature lets you revert the renamed files back to their original names.

## User Guide

### Step-by-Step Instructions

1. **Clone the Repository**
   - Run the following command to clone the repository:
   ```bash
   git clone https://github.com/your-repository-url.git
   ```
### Install Dependencies
You need tkinter and tkinterdnd2 for the GUIand drag-and-drop functionality. Install dependencies using pip:
```
bash
Copy code
pip install tkinter tkinterdnd2
```
### Run the Script
Navigate to the directory where the script is stored and run:
```
bash
Copy code
python file_renamer.py
```
### How to Use the Features
***Prefix and Suffix:*** Enter the text you want to add at the start (prefix) or end (suffix) of each file name in the respective input fields.
***Replace Spaces with Underscores:*** Check the box labeled "Replace spaces with underscores" to automatically replace spaces in the file names with underscores.
***Find and Replace:*** In the "Find" field, enter the text you want to replace, and in the "Replace with" field, specify the text to replace it with. The script will search for the given text in the file names and replace it accordingly.
***Append Date:*** Check the box labeled "Add current date" to append today's date in the format YYYY-MM-DD to each file name.
***Sequential Renaming:*** Check the "Rename sequentially" box to number the files in ascending order, such as file_001, file_002, etc.
***Predefined Regex Options:***
Remove numbers: Removes any digits from the file name.
Replace spaces with underscores: Replaces all spaces with underscores.
Remove special characters: Removes any special characters (e.g., !, @, #, etc.).
Append '_updated' before extension: Adds the suffix _updated to the file name before the extension (e.g., file_updated.txt).
***File Extension Filtering:*** In the "File Filter" field, specify the file extensions of files you want to rename (e.g., .txt, .jpg). If left empty, the script will rename all files in the directory.
***Drag-and-Drop Folder Selection:*** You can drag a folder into the interface, and the path will automatically appear. You can also select the folder manually by clicking the "Select Folder" button.
***Undo Last Rename:*** If you've renamed files but need to revert the changes, click the "Undo Last Rename" button to restore the original file names.
Example Usage

Drag a folder into the app or select a folder manually.
Specify the prefix and/or suffix, select regex options, and enable any other renaming options like adding the date or renaming sequentially.
Click "Rename" to apply the changes.
To undo the renaming, click "Undo Last Rename."

### Contributions

Feel free to fork this project and submit pull requests if you want to add features or improve existing functionality.
```
vbnet
Copy code

This version is in proper Markdown format for your GitHub repository. You can copy and paste this into your `README.md` file. Let me know if you need further adjustments
```
