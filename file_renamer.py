import os
import datetime

# Function to rename files
def rename_files(directory, prefix=None, suffix=None, replace_spaces=False, add_date=False, sequential=False):
    try:
        # Get a list of all files in the directory
        files = os.listdir(directory)
        count = 1  # For sequential renaming if needed
        
        # Loop through each file in the directory
        for file_name in files:
            # Only process files (ignore folders)
            if os.path.isfile(os.path.join(directory, file_name)):
                # Split the file name into name and extension
                file_name_without_ext, file_extension = os.path.splitext(file_name)
                
                # Modify file name based on user inputs
                new_name = file_name_without_ext
                
                if prefix:
                    new_name = prefix + new_name  # Add prefix if provided
                
                if suffix:
                    new_name = new_name + suffix  # Add suffix if provided
                
                if replace_spaces:
                    new_name = new_name.replace(" ", "_")  # Replace spaces with underscores
                
                if add_date:
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Get current date
                    new_name = f"{new_name}_{current_date}"  # Append the date
                
                if sequential:
                    new_name = f"{new_name}_{count:03d}"  # Add sequential numbers
                    count += 1
                
                # Add the original file extension to the new name
                new_name += file_extension
                
                # Form the full old and new file paths
                old_file_path = os.path.join(directory, file_name)
                new_file_path = os.path.join(directory, new_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {file_name} -> {new_name}")
                
        print("\nAll files renamed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")

# Function to get user input and apply renaming
def main():
    # Get the directory path where files are located
    directory = input("Enter the directory path of files to rename: ")
    
    # Check if directory exists
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return
    
    # Get user preferences for renaming
    prefix = input("Enter a prefix to add (leave blank for none): ")
    suffix = input("Enter a suffix to add (leave blank for none): ")
    replace_spaces = input("Replace spaces with underscores? (y/n): ").lower() == 'y'
    add_date = input("Add the current date to the file names? (y/n): ").lower() == 'y'
    sequential = input("Rename files with sequential numbers? (y/n): ").lower() == 'y'
    
    # Call the rename function with user inputs
    rename_files(directory, prefix, suffix, replace_spaces, add_date, sequential)

# Run the script
if __name__ == "__main__":
    main()
