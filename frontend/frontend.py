# ----------------------------------------------------------------------------
# NOTICE: This code is the exclusive property of University of Kansas
#         Architecture Research and is strictly confidential.
#
#         Unauthorized distribution, reproduction, or use of this code, in
#         whole or in part, is strictly prohibited. This includes, but is
#         not limited to, any form of public or private distribution,
#         publication, or replication.
#
# For inquiries or access requests, please contact:
#         Alex Manley (amanley97@ku.edu)
#         Mahmudul Hasan (m.hasan@ku.edu)
# ----------------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk
import calls

# Create the main window
root = tk.Tk()
root.title("eager")

# Obtain gem5 data
options = calls.get_gem5_data()

# Define section titles
section_titles = ["Board Style", "Processor", "Cache Hierarchy", "Memory"]

# Create dropdown menus, labels, and variables
section_frames = []
section_dropdowns = []
selected_option_labels = []
section_selected_options = [] 
current_selected_section = tk.StringVar()
hint = str("Hints: Some helpful information here")

def run_simulation():
    hint = calls.http_request("run-simulation", "PUT")
    bottom_bar.config(text=str(hint.text))

def exit():
    calls.http_request("shutdown", "PUT")
    root.destroy()

def edit():
    advance_section(True)
    edit_button.grid_remove()

def print_selected(list, label):
    result_dict = {}
    for label, stringvar in zip(label, list):
        value = stringvar.get()
        result_dict[label] = value
    data_test = calls.http_request("user-data", "PUT", result_dict)
    print(data_test.text)

def show_section(section, done):
    # Set weight for the selected section, making it larger
    selected_index = section_titles.index(section) if not done else len(section_titles) + 1
    for i in range(len(section_titles)):
        weight = 1 if i == selected_index else 0
        root.grid_rowconfigure(i*2 + 1, weight=weight)

        # Show or hide the dropdown based on the selected section
        if i == selected_index:
            section_dropdowns[i].grid(row=0, column=1, padx=5, pady=5)
            selected_option_labels[i].grid_remove()
            highlight_color = "black"
        else:
            section_dropdowns[i].grid_remove()
            selected_option_labels[i].grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
            selected_option_labels[i].config(text=f"       {section_selected_options[i].get()}")
            highlight_color = root.cget("bg")
        
        section_frames[i].config(highlightthickness=weight*2, highlightbackground=highlight_color)                    

    # Set the current selected section
    current_selected_section.set(section)

# Function to advance to the next section
def advance_section(reset):
    current_index = section_titles.index(current_selected_section.get())
    index_count = 0 if reset else current_index + 1

    # Save the selected option for the current section
    section_selected_options[current_index].set(section_dropdowns[current_index].get())
    # Advance to the next section
    next_index = (current_index + 1) % len(section_titles)
    if index_count == len(section_titles):
        show_section(section_titles[current_index], True)
        edit_button.grid(row=len(section_titles)*2 + 1, column=0, padx=10, pady=5, sticky=tk.W)
        print_selected(section_selected_options, section_titles)
    else:
        show_section(section_titles[next_index], False)

# Header label
header_label = tk.Label(root, text="Welcome to EAGER Gem5 GUI", font=('TkDefaultFont', 16, 'bold'))
header_label.grid(row=0, column=0, columnspan=3, pady=10)

for i, section_title in enumerate(section_titles):
    # Create a section frame
    section_frame = tk.Frame(root, highlightthickness=0, relief=tk.RIDGE)
    section_frame.grid(row=i*2 + 1, column=0, padx=10, pady=5, sticky=tk.W)
    section_frames.append(section_frame)

    # Add section title to the frame
    label = tk.Label(section_frame, text=section_title, font=('TkDefaultFont', 12, 'normal'))
    label.grid(row=0, column=0, padx=5, pady=5)

    # Create a dropdown menu
    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(section_frame, textvariable=dropdown_var, values=options[i])
    dropdown.bind("<<ComboboxSelected>>", lambda event=None, : advance_section(False))
    dropdown.grid(row=0, column=1, padx=5, pady=5)
    section_dropdowns.append(dropdown)

    # Create a label to display the selected option
    selected_option_label = tk.Label(section_frame, text="", font=('TkDefaultFont', 10, 'normal'))
    selected_option_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    selected_option_labels.append(selected_option_label)

    # Create a variable to store the selected option
    section_selected_options.append(tk.StringVar())

# Testing Edit Button
edit_button = tk.Button(root, text="Edit", command=edit)
edit_button.grid_remove()

# Create a larger workspace with Canvas for graphics on the right
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.grid(row=1, column=1, padx=10, pady=10, rowspan=len(section_titles)*2 + 1, columnspan=2, sticky=tk.W)

# Create a bottom bar with hints and buttons
bottom_bar = tk.Label(root, text=hint, bd=1, relief=tk.SUNKEN, anchor=tk.W)
bottom_bar.grid(row=len(section_titles)*2 + 2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

# Add "Simulate" button to the far right below the hint
simulate_button = tk.Button(root, text="Simulate", command=run_simulation, width=60)
simulate_button.grid(row=len(section_titles)*2 + 3, column=1, padx=10, pady=5, sticky=tk.E)

# Add "Exit" button to the far right below the hint
exit_button = tk.Button(root, text="Exit", command=exit)
exit_button.grid(row=len(section_titles)*2 + 3, column=2, padx=20, pady=5, sticky=tk.E)

# Show Section 1 by default
show_section("Board Style", False)

# Run the GUI
root.mainloop()