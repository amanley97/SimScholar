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

options = calls.get_gem5_data()
hint = str("Hints: Some helpful information here")

def run_simulation():
    hint = calls.simulate_action()
    bottom_bar.config(text=str(hint))

def exit():
    calls.exit_server()
    root.destroy()

def show_section(section):
    # Set weight for the selected section, making it larger
    selected_index = section_titles.index(section)
    for i in range(len(section_titles)):
        weight = 1 if i == selected_index else 0

        # Show or hide the dropdown based on the selected section
        if i == selected_index:
            section_dropdowns[i].grid(row=0, column=1, padx=5, pady=5)
        else:
            section_dropdowns[i].grid_remove()

        # Show a box around the selected section
        highlight_color = "black" if i == selected_index else root.cget("bg")
        section_frames[i].config(highlightthickness=weight*2, highlightbackground=highlight_color)

        # Show the selected option label on not selected sections
        if i != selected_index:
            selected_option_labels[i].grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
            selected_option_labels[i].config(text=f"       {section_selected_options[i].get()}")
        else:
            selected_option_labels[i].grid_remove()

    # Set weight for the selected section, making it larger
    for i in range(len(section_titles)):
        weight = 1 if i == selected_index else 0
        root.grid_rowconfigure(i*2 + 1, weight=weight)

    # Set the current selected section
    current_selected_section.set(section)

# Function to advance to the next section
def advance_section():
    current_index = section_titles.index(current_selected_section.get())

    # Save the selected option for the current section
    selected_section = current_selected_section.get()
    section_selected_options[current_index].set(section_dropdowns[current_index].get())

    # Advance to the next section
    next_index = (current_index + 1) % len(section_titles)
    show_section(section_titles[next_index])

# Create the main window
root = tk.Tk()
root.title("eager")

# Header label
header_label = tk.Label(root, text="Welcome to EAGER Gem5 GUI", font=('TkDefaultFont', 16, 'bold'))
header_label.grid(row=0, column=0, columnspan=3, pady=10)

# Define section titles
section_titles = ["Board Style", "Processor", "Cache Hierarchy", "Memory"]

# Create dropdown menus, labels, and variables
section_frames = []
section_dropdowns = []
selected_option_labels = []
section_selected_options = []  # Add this line to define the missing variable
current_selected_section = tk.StringVar()

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
    dropdown.bind("<<ComboboxSelected>>", lambda event=None, section=section_title: advance_section())
    dropdown.grid(row=0, column=1, padx=5, pady=5)
    section_dropdowns.append(dropdown)

    # Create a label to display the selected option
    selected_option_label = tk.Label(section_frame, text="", font=('TkDefaultFont', 10, 'normal'))
    selected_option_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    selected_option_labels.append(selected_option_label)

    # Create a variable to store the selected option
    section_selected_options.append(tk.StringVar())

# Add "Advance Section" button below left sections
advance_button = tk.Button(root, text="Advance Section", command=advance_section)
advance_button.grid(row=len(section_titles)*2 + 1, column=0, padx=10, pady=5, sticky=tk.W)

# Create a larger workspace with Canvas for graphics on the right
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.grid(row=1, column=1, padx=10, pady=10, rowspan=len(section_titles)*2 + 1, columnspan=2, sticky=tk.W)

# Draw a sample rectangle on the canvas
canvas.create_rectangle(50, 50, 200, 200, fill="blue")

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
show_section("Board Style")

# Run the GUI
root.mainloop()