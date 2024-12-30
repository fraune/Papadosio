import os
import shutil

def clean_raw_folder():
    # Define the raw folder path
    raw_folder_path = os.path.join(os.path.dirname(__file__), '..', 'raw')
    
    # Normalize the path for the OS
    raw_folder_path = os.path.normpath(raw_folder_path)
    
    # Delete the folder if it exists
    if os.path.exists(raw_folder_path):
        print(f"Deleting folder: {raw_folder_path}")
        shutil.rmtree(raw_folder_path)
    else:
        print(f"Folder does not exist: {raw_folder_path}")
    
    # Recreate the folder
    print(f"Creating folder: {raw_folder_path}")
    os.makedirs(raw_folder_path, exist_ok=True)
    print("Folder cleaned successfully.")

if __name__ == "__main__":
    clean_raw_folder()
