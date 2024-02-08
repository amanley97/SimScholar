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
import render
debug_open = False

def open_debug(root, sections):
    global debug_open, debug_sub_window
    if debug_open:
        debug_sub_window.destroy()
        debug_open=False
    else:
        debug_sub_window = debug_window(root, sections)
        debug_open=True

def debug_window(root, sections):
    # Create the main window
    debug = tk.Toplevel(root)
    debug.title("debug")
    debug.configure(background="gray")

    header_label = tk.Label(debug, text="EAGER Debugger", font=('TkDefaultFont', 16, 'bold'))
    header_label.grid(row=0, column=0, columnspan=3, pady=10)

    def debug_selection(value):
        global current_section 
        current_section = value.get()
        # title=current_section["main"]["title"]
        print(current_section)

    var = tk.StringVar()
    option = []
    for section_idx in range(len(sections)):
        sec_ttl = sections[section_idx]["main"]["title"]
        # Create selector buttons
        opt = tk.Radiobutton(debug, text=f"Frame {section_idx}: {sec_ttl}", 
                             variable=var, value=sec_ttl, command=lambda value=var: debug_selection(value))
        opt.grid(row=section_idx+2, column=0, padx=5, pady=5, columnspan=2)
        option.append(opt)

    # SHOW FRAME
    show_button = tk.Button(debug, text="Hide Frame", command=lambda: render.hide_section(current_section, sections))
    show_button.grid(row=7, column=0, padx=20, pady=5, sticky=tk.E)

    # HIDE BUTTON
    hide_button = tk.Button(debug, text="Show Frame", command=lambda: render.show_section(current_section, sections))
    hide_button.grid(row=7, column=1, padx=20, pady=5, sticky=tk.E)
    return debug