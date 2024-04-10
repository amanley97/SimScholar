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
sections = {}

def render_section(master, opts, title):
    # Create a section frame
    section_frame = tk.Frame(master, background="darkgray")

    #Populate it!!
    sections[title] = populate_frame(section_frame, opts, title)
    return section_frame

def update_selected(title, key, newval):
    oldval = sections[title][key]
    if newval.get() != oldval:
        sections[title][key] = newval.get()

def populate_frame(frame, data, label=""):
    saved_opts = {}
    if label:  # If a label is provided, add a header
        ttk.Label(frame, text=label, font=('TkDefaultFont', 10, 'bold'), background="darkgray").pack(pady=(10, 5), padx=10, anchor='w')
    for key, value in data.items():
        row_frame = tk.Frame(frame, background="darkgray")
        row_frame.pack(fill='x', expand=True, padx=5, pady=5)
        ttk.Label(row_frame, text=key, background="darkgray").pack(side='left')
        if isinstance(value, list):
            var = tk.StringVar(row_frame)
            var.set(value[0])  # default value
            dropdown = tk.OptionMenu(row_frame, var, *value,
                                     command=lambda event=None, t=label, d=key, v=var: update_selected(t, d, v))
            dropdown.pack(side='right', fill='x', expand=True)
            saved_opts[key] = var.get()
        elif isinstance(value, int):
            intvar = tk.IntVar(row_frame)
            intvar.set(value)
            entry = tk.Entry(row_frame, textvariable=intvar)
            entry.pack(side='right', fill='x', expand=True)
            saved_opts[key] = intvar.get()
            entry.bind("<Return>", lambda event=None, t=label, d=key, v=intvar: update_selected(t, d, v))
    return saved_opts
