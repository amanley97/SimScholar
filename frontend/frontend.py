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

options = {
    'boards' : {
        'type' : ['Simple', 'x86', 'ARM'],
        'clk' : 0
    },
    'processor' : {
        'isa' : ['x86', 'ARM'],
        'type' : ['atomic', 'o3', 'minor'],
        'ncores' : 0
    },
    'memory' : {
        'type' : ['SingleChannelDDR3_1600',
                  'SingleChannelDDR4_2400',
                  'DualChannelDDR4_2400'],
        'size' : 0
    },
    'cache' : {
        'type' : ['NoCache',
                  'PrivateL1CacheHierarchy',
                  'PrivateL1PrivateL2CacheHierarchy',
                  'PrivateL1SharedL2CacheHierarchy'],
        'l1d' : 0,
        'l1i' : 0
    }
}


boards = options['boards']
processors = options['processor']
memories = options['memory']
caches = options['cache']

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
    root.mainloop()

def cfg_tabs(master):
    tabs = ttk.Notebook(master)
    tabs.grid(row=1, rowspan= 1, column=0, sticky="nsew")

    tab1 = render.render_section(tabs, boards, "Board Configuration")
    tab2 = render.render_section(tabs, processors, "Processor Configuration")
    tab3 = render.render_section(tabs, memories, "Memory Configuration")
    tab4 = render.render_section(tabs, caches, "Cache Configuration")

    tabs.add(tab1, text="Board")
    tabs.add(tab2, text="Processor")
    tabs.add(tab3, text="Memory")
    tabs.add(tab4, text="Cache Hierarchy")


def cfg_window(tab1):
    # Obtain gem5 data
    options = calls.get_gem5_data()
    # print(options)
    section_menu = options[0]

    # Create dropdown menus, labels, and variables
    hint = str("Hints: Some helpful information here")

    # Header label
    header_label = tk.Label(tab1, text="Gem5 System Config", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="Black")
    header_label.grid(row=0, column=0, columnspan=3, pady=10)
    
    cfg_tabs(tab1)

    # RESOURCE MANAGER
    resources = tk.Frame(tab1, background="darkgray")
    resources.grid(row=2, rowspan=2, column=0, pady=10, sticky="nsew")
    ttk.Label(resources, text="Resource Manager", font=('TkDefaultFont', 10, 'bold'), background="darkgray").pack(pady=(10, 5), padx=10, anchor='w')
    
    # CANVAS
    canvas = tk.Canvas(tab1, width=600, height=400, bg="lightgray")
    canvas.grid(row=1, column=1, padx=10, pady=10, rowspan=len(section_menu)*2 + 1, columnspan=2, sticky=tk.W)

    # HINT BAR
    bottom_bar = tk.Label(tab1, text=hint, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="lightgray", fg="Black")
    bottom_bar.grid(row=len(section_menu)*3 + 2, column=0, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)

    # SIMULATE BUTTON
    simulate_button = tk.Button(tab1, text="Simulate", command=lambda: calls.run_simulation(bottom_bar), width=60)
    simulate_button.grid(row=len(section_menu)*3 + 3, column=1, padx=10, pady=5, sticky=tk.E)

    # DEFAULTS
    canvas.delete("all")

root_window()