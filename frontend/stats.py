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
names = []
values = []
comments = []
line_range = [0, 10]

def parse_stats(text):
    global line_range, names, values, comments
    print("[stats] Refreshing Stats")
    file_path = './m5out/stats.txt'
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

    line_range = [0, 10]
    show_stats(text, True)

def show_stats(text, forward):
    global line_range
    name_text = text[0]
    value_text = text[1]
    comment_text = text[2]

    # Clear text boxes
    name_text.delete("1.0", "end")
    value_text.delete("1.0", "end")
    comment_text.delete("1.0", "end")

    if not forward:
        if line_range[0] > 0:
            line_range[0] -= 10
            line_range[1] -= 10

        for line in range(line_range[0], line_range[1]):
            name_text.insert("1.0", f"{names[line]}\n")
            value_text.insert("1.0", f"{values[line]}\n")
            comment_text.insert("1.0", f"{comments[line]}\n")

    else:
        for line in range(line_range[0], line_range[1]):
            name_text.insert("1.0", f"{names[line]}\n")
            value_text.insert("1.0", f"{values[line]}\n")
            comment_text.insert("1.0", f"{comments[line]}\n")

        line_range[0] += 10
        line_range[1] += 10

    print(line_range) 

def stats_window(stats):
    stats_height = 20
    header_label = tk.Label(stats, text="Simulation Stats", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="black")
    header_label.grid(row=0, column=0, columnspan=3, pady=10, padx=20)

    tk.Label(stats, text="Name", font=('TkDefaultFont', 10, 'bold'), bg="gray", fg="black").grid(row=1, column=0, pady=20, padx=20)
    stats_name = tk.Text(stats, 
                   width=30, 
                   height=stats_height, 
                   font="Courier", 
                   cursor="arrow", 
                   bg="lightgray", 
                   fg="black", 
                   wrap="word")
    stats_name.grid(row=2, column=0, sticky="we", padx=20, pady=10)

    tk.Label(stats, text="Value", font=('TkDefaultFont', 10, 'bold'), bg="gray", fg="black").grid(row=1, column=1, pady=20, padx=20)
    stats_val = tk.Text(stats, 
                   width=10, 
                   height=stats_height, 
                   font="Courier", 
                   cursor="arrow", 
                   bg="lightgray", 
                   fg="black", 
                   wrap="word")
    stats_val.grid(row=2, column=1, sticky="we", padx=20, pady=10)

    tk.Label(stats, text="Comment", font=('TkDefaultFont', 10, 'bold'), bg="gray", fg="black").grid(row=1, column=2, pady=20, padx=20)
    stats_comment = tk.Text(stats, 
                   width=40, 
                   height=stats_height, 
                   font="Courier", 
                   cursor="arrow", 
                   bg="lightgray", 
                   fg="black", 
                   wrap="word")
    stats_comment.grid(row=2, column=2, sticky="we", padx=20, pady=10)

    frame = [stats_name, stats_val, stats_comment]

    refresh_button = tk.Button(stats, text="Refresh", command=lambda t=frame: parse_stats(t), width=10)
    refresh_button.grid(row=0, column=2, padx=10, pady=5, sticky="e")

    prev_button = tk.Button(stats, text="Previous", command=lambda t=frame: show_stats(t, False), width=20)
    prev_button.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    next_button = tk.Button(stats, text="Next", command=lambda t=frame: show_stats(t, True), width=20)
    next_button.grid(row=3, column=2, padx=10, pady=5, sticky="e")

    stats.grid_rowconfigure(1, weight=1)
    stats.grid_columnconfigure(0, weight=1)