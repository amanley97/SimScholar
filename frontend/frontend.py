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
import calls, image, render, debug, json
sections = []

def root_window(en_debug=False):
    # Create the main window
    root = tk.Tk()
    root.title("eager")

    # Obtain gem5 data
    options = calls.get_gem5_data()

    # Define section titles
    # section_menu = {"Board Style" : options[0], 
    #                 "Processor" : ["CPU Type", "Number of Cores"], 
    #                 "Cache Hierarchy" : ["L1 Size"], 
    #                 "Memory" : ["Size"]
    #                 }
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
        chosen_board=section_menu[str(input)].items()
        for i, (main_option, sub_options) in enumerate(chosen_board):
            # Create each section
            section = render.render_section(master=root,  
                                            row_offset=i, 
                                            title=main_option,
                                            opts=options[i],
                                            func= update_select,
                                            subopts=sub_options
                                            )
            sections.append(section)

    def edit():
        # advance_section(True)
        edit_button.grid_remove()

    # Header label
    header_label = tk.Label(root, text="Welcome to EAGER Gem5 GUI", font=('TkDefaultFont', 16, 'bold'))
    header_label.grid(row=0, column=0, columnspan=3, pady=10)
    
    boards = list(section_menu.keys())
    render.render_section(master=root,
                          row_offset=0,
                          title="Board Style",
                          opts=boards,
                          func=render_board_opts,
                          subopts=None
                          )

    # EDIT BUTTON
    edit_button = tk.Button(root, text="Edit", command=edit)
    edit_button.grid_remove()

    # CANVAS
    canvas = tk.Canvas(root, width=600, height=400, bg="white")
    canvas.grid(row=1, column=1, padx=10, pady=10, rowspan=len(section_menu)*2 + 1, columnspan=2, sticky=tk.W)

    # HINT BAR
    bottom_bar = tk.Label(root, text=hint, bd=1, relief=tk.SUNKEN, anchor=tk.W)
    bottom_bar.grid(row=len(section_menu)*2 + 2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

    if en_debug:
        # DEBUG BUTTON
        debug_button = tk.Button(root, text="debug", command=lambda: debug.open_debug(root, sections))
        debug_button.grid(row=len(section_menu)*2 + 3, column=0, padx=5, pady=5)

    # SIMULATE BUTTON
    simulate_button = tk.Button(root, text="Simulate", command=lambda: calls.run_simulation(bottom_bar), width=60)
    simulate_button.grid(row=len(section_menu)*2 + 3, column=1, padx=10, pady=5, sticky=tk.E)

    # EXIT BUTTON
    exit_button = tk.Button(root, text="Exit", command=lambda: calls.exit(root=root))
    exit_button.grid(row=len(section_menu)*2 + 3, column=2, padx=20, pady=5, sticky=tk.E)

    # DEFAULTS
    canvas.delete("all")
    root.mainloop()

root_window(en_debug=True)