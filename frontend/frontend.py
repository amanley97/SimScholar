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
import calls, image, render, debug, json, ide, stats
sections = []

def root_window():
    # Create the main window
    root = tk.Tk()
    root.title("eager    ->    the all-in-one gem5 environment")

    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")

    tab1 = tk.Frame(notebook, background="gray")
    tab2 = tk.Frame(notebook, background="gray")
    tab3 = tk.Frame(notebook, background="gray")
    notebook.add(tab1, text="Configure")
    notebook.add(tab2, text="Code Editor")
    notebook.add(tab3, text="Statistics")
    
    cfg_window(tab1)
    ide.code_window(tab2)
    stats.stats_window(tab3)
    # debug.debug_window(tab3)
    root.mainloop()

def cfg_window(tab1):
    # Obtain gem5 data
    options = calls.get_gem5_data()

    section_menu = options[0]

    # Create dropdown menus, labels, and variables
    hint = str("Hints: Some helpful information here")

    def update_select(section, selection):
        idx = sections.index(section)
        current_section = sections[idx]
        current_section["main"]["dropdown_value"] = selection
        render.hide_section("Cache Hierarchy", sections)
        render.show_section("Cache Hierarchy", sections)
        print(current_section)

    def render_board_opts(n, input):
        chosen_board=list(section_menu[str(input)].items())
        for i, (main_option, sub_options) in enumerate(chosen_board[1:]):
            # Create each section
            section = render.render_section(master=tab1,  
                                            row_offset=i+1, 
                                            title=main_option,
                                            opts=options[i+1],
                                            func= update_select,
                                            subopts=sub_options
                                            )
            sections.append(section)

    def edit():
        # advance_section(True)
        edit_button.grid_remove()

    # Header label
    header_label = tk.Label(tab1, text="Gem5 System Config", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="Black")
    header_label.grid(row=0, column=0, columnspan=3, pady=10)
    
    boards = list(section_menu.keys())
    render.render_section(master=tab1,
                          row_offset=1,
                          title="Board",
                          opts=boards,
                          func=render_board_opts,
                          subopts=section_menu[boards[0]]["clk_freq"]
                          )

    # EDIT BUTTON
    edit_button = tk.Button(tab1, text="Edit", command=edit)
    edit_button.grid_remove()

    # CANVAS
    canvas = tk.Canvas(tab1, width=600, height=400, bg="lightgray")
    canvas.grid(row=1, column=1, padx=10, pady=10, rowspan=len(section_menu)*2 + 1, columnspan=2, sticky=tk.W)

    # HINT BAR
    bottom_bar = tk.Label(tab1, text=hint, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="lightgray", fg="Black")
    bottom_bar.grid(row=len(section_menu)*3 + 2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

    # SIMULATE BUTTON
    simulate_button = tk.Button(tab1, text="Simulate", command=lambda: calls.run_simulation(bottom_bar), width=60)
    simulate_button.grid(row=len(section_menu)*3 + 3, column=1, padx=10, pady=5, sticky=tk.E)

    # EXIT BUTTON
    # exit_button = tk.Button(tab1, text="Exit", command=lambda: calls.exit(root=tab1))
    # exit_button.grid(row=len(section_menu)*3 + 3, column=2, padx=20, pady=5, sticky=tk.E)

    # DEFAULTS
    canvas.delete("all")

root_window()