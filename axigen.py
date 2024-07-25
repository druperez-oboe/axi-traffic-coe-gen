import tkinter as tk
from tkinter import filedialog
import os

# File to save and load text
text_file = "saved_text.txt"

def clear_status_labels():
    save_status_label.config(text="")
    write_status_label.config(text="")

def save_text():
    text = text_entry.get("1.0", tk.END).strip()
    
    if not text:
        save_status_label.config(text="Error: No text to save.")
        root.after(2000, clear_status_labels)
        return

    try:
        # Save the current text to the .txt file
        with open(text_file, "w") as file:
            file.write(text)
        save_status_label.config(text="Text saved successfully.")
        root.after(2000, clear_status_labels)
    except Exception as e:
        save_status_label.config(text=f"Error: {e}")
        root.after(2000, clear_status_labels)

def write_to_files():
    folder = folder_var.get()
    text = text_entry.get("1.0", tk.END).strip()
    
    if not folder or not text:
        write_status_label.config(text="Error: Folder or text missing.")
        root.after(2000, clear_status_labels)
        return

    # Ensure the folder exists
    if not os.path.isdir(folder):
        write_status_label.config(text="Error: Folder does not exist.")
        root.after(2000, clear_status_labels)
        return

    files = [
        ["addr.coe", "memory_initialization_radix = 16;\nmemory_initialization_vector = \n"],
        ["data.coe", "memory_initialization_radix = 16;\nmemory_initialization_vector = \n"],
        ["mask.coe", "memory_initialization_radix = 16;\nmemory_initialization_vector = \n"],
        ["ctrl.coe", "memory_initialization_radix = 16;\nmemory_initialization_vector = \n"]
    ]

    line_num = 0
    for line in text.split("\n"):
        line_num += 1
        line = line.split(" ")

        # Convert ascii and decimal entries into hex
        for i in range(len(line)):
            if(line[i][0:2] == "a:"):
                line[i] = ''.join(format(ord(c), 'x') for c in line[i][2:])
            elif(line[i][0:2] == "d:"):
                line[i] = hex(int(line[i][2:]))[2:]

        if(len(line) == 2): # Read command
            files[3][1] += hex(131072 + line_num*257)[2:].upper().zfill(8) + "\n"
            files[0][1]  += line[1].zfill(8)[:8] + "\n"
            files[1][1]  += "00000000\n"
            files[2][1]  += "FFFFFFFF\n"
        elif(len(line) == 3): # Write command
            files[3][1]  += hex(196608 + line_num*257)[2:].upper().zfill(8) + "\n"
            files[0][1]  += line[1].zfill(8)[:8] + "\n"
            files[1][1]  += line[2].zfill(8)[:8] + "\n"
            files[2][1]  += "FFFFFFFF\n"
        else:
            print("ERROR: ", line)

    try:
        # Save the current text to the .txt file
        save_text()
        
        # Write to all .coe files
        for filename, text in files:
            file_path = os.path.join(folder, filename)
            with open(file_path, "w") as file:
                file.write(text)
                file.write("FFFFFFFF")

                
        write_status_label.config(text="Files written successfully.")
        root.after(2000, clear_status_labels)
    except Exception as e:
        write_status_label.config(text=f"Error: {e}")
        root.after(2000, clear_status_labels)

def select_folder():
    folder = filedialog.askdirectory(initialdir=folder_var.get())
    if folder:
        folder_var.set(folder)
        folder_display_label.config(text=f"Selected Folder: {folder}")

def load_text():
    if os.path.exists(text_file):
        with open(text_file, "r") as file:
            return file.read()
    else:
        # If the file does not exist, create it with default text
        default_text = "w 0 a:oboe\nr 0\nr 200\n"
        with open(text_file, "w") as file:
            file.write(default_text)
        return default_text

# Create the main window
root = tk.Tk()
root.title("AXI Traffic COE Generator")

# Set the default folder to the current working directory
default_folder = os.getcwd()

# Load text for the text entry box
loaded_text = load_text()

# Folder selection
folder_var = tk.StringVar(value=default_folder)
folder_label = tk.Label(root, text="Folder:")
folder_label.pack(pady=5)

folder_button = tk.Button(root, text="Browse", command=select_folder)
folder_button.pack(pady=5)

# Display selected folder
folder_display_label = tk.Label(root, text=f"Selected Folder: {default_folder}")
folder_display_label.pack(pady=5)

# Text entry
text_label = tk.Label(root, text="Format: \n w addr data \n r addr \n All in hex unless a: or d: prefix is added")
text_label.pack(pady=5)

text_entry = tk.Text(root, height=20, width=30)
text_entry.pack(pady=5)

# Insert loaded text into the text entry box
text_entry.insert(tk.END, loaded_text)

# Save Text button and status label
save_button = tk.Button(root, text="Save Text", command=save_text)
save_button.pack(pady=5)

save_status_label = tk.Label(root, text="")
save_status_label.pack(pady=5)

# Write button and status label
write_button = tk.Button(root, text="Write coe files", command=write_to_files)
write_button.pack(pady=5)

write_status_label = tk.Label(root, text="")
write_status_label.pack(pady=5)

# Run the application
root.mainloop()
