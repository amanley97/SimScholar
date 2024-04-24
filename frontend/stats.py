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

import os
import tkinter as tk
from tkinter import messagebox
from printdebug import printdebug
snap_dir = os.getenv('SNAP_USER_COMMON')
stats_dir = os.path.join(snap_dir, 'm5out', 'stats.txt')

mode = 'default'
names = []
values = []
comments = []
stats_found = []
default_stats = [
    "numcycles", 
    "simseconds", 
    "simticks", 
    "siminsts", 
    "simops", 
    "overallhits::total", 
    "overallmisses::total"
]
line_range = [0, 10]

def parse_stats(text):
    global line_range, names, values, comments
    printdebug("[stats] Refreshing Stats")
    file_path = stats_dir
    names.clear()
    values.clear()
    comments.clear()

    # Flag to skip non-data lines
    data_started = False

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("---------- Begin Simulation Statistics ----------"):
                    data_started = True
                    continue  # Skip the header line
                if data_started and line:  # Process lines only after the header
                    if line.startswith("#"):  # Skip lines that start with '#'
                        continue
                    # Split the line into parts based on multiple spaces
                    parts = line.split(maxsplit=2)
                    if len(parts) >= 2:
                        names.append(parts[0].strip())
                        values.append(parts[1].strip())
                        # Some lines may not have comments, so check the length
                        if len(parts) == 3:
                            comments.append(parts[2].strip())
                        else:
                            comments.append("")  # Append an empty string if no comment

    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    if mode == 'default':
        stats_found.clear()
        for term in default_stats:
            search_stats(names, term)
        printdebug(f"[stats] {len(stats_found)} stats found")
        if len(stats_found) > 0:
            show_stats(text)
        else:
            messagebox.showerror("Error", "No Stats file found!")
    else:
        line_range = [0, 10]
        show_stats(text)

def show_stats(text):

    def display_stat(canvas, array, index, width, size):
        # Position to start drawing text
        x = 10
        y = 10
        for line in index:
            canvas.create_text(x, y, text=array[line], anchor='nw', font=('Courier', size), width=width)
            y += 30  # Move to the next line position 

    printdebug("[stats] displaying stats")
    global line_range
    name_text = text[0]
    value_text = text[1]
    comment_text = text[2]

    # Clear text boxes
    name_text.delete("all")
    value_text.delete("all")
    comment_text.delete("all")

    if mode == 'default':
        display_stat(name_text, names, stats_found, 340, 11)
        display_stat(value_text, values, stats_found, 90, 12)
        display_stat(comment_text, comments, stats_found, 390, 9)

def search_stats(list, term):
    global stats_found
    search_substring_lower = term.lower()
    indices = [index for index, item in enumerate(list) if search_substring_lower in item.lower()]
    for i in range(len(indices)):
        stats_found.append(indices[i])
    return stats_found

def stats_window(stats):
    stats_height = 20
    header_label = tk.Label(stats, text="Simulation Stats", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="black")
    header_label.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky="we")

    tk.Label(stats, text="Name", font=('TkDefaultFont', 10, 'bold'), bg="gray", fg="black").grid(row=1, column=0, pady=5, padx=20)
    stats_name = tk.Canvas(stats, width=350, height=stats_height*20, bg="lightgray")
    stats_name.grid(row=2, column=0, sticky="we", padx=10, pady=5)

    tk.Label(stats, text="Value", font=('TkDefaultFont', 10, 'bold'), bg="gray", fg="black").grid(row=1, column=1, pady=5, padx=20)
    stats_val = tk.Canvas(stats, width=100, height=stats_height*20, bg="lightgray")
    stats_val.grid(row=2, column=1, sticky="we", padx=10, pady=5)

    tk.Label(stats, text="Comment", font=('TkDefaultFont', 10, 'bold'), bg="gray", fg="black").grid(row=1, column=2, pady=5, padx=20)
    stats_comment = tk.Canvas(stats, width=400, height=stats_height*20, bg="lightgray")
    stats_comment.grid(row=2, column=2, sticky="we", padx=10, pady=5)
    frame = [stats_name, stats_val, stats_comment]

    refresh_button = tk.Button(stats, text="Refresh", command=lambda t=frame: parse_stats(t), width=10)
    refresh_button.grid(row=3, column=2, padx=10, pady=5, sticky="e")

    if mode == 'all':
        prev_button = tk.Button(stats, text="Previous", command=lambda t=frame: show_stats(t, False), width=20)
        prev_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        next_button = tk.Button(stats, text="Next", command=lambda t=frame: show_stats(t, True), width=20)
        next_button.grid(row=3, column=2, padx=10, pady=5, sticky="e")

    # stats.grid_rowconfigure(1, weight=1)
    # stats.grid_columnconfigure(0, weight=1)