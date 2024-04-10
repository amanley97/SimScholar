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

def render_section(master, opts, title):
    # Create a section frame
    section_frame = tk.Frame(master, background="darkgray")

    #Populate it!!
    populate_frame(section_frame, opts, title)

    return section_frame

def populate_frame(frame, data, label=""):
        if label:  # If a label is provided, add a header
            ttk.Label(frame, text=label, font=('TkDefaultFont', 10, 'bold'), background="darkgray").pack(pady=(10, 5), padx=10, anchor='w')
        for key, value in data.items():
            if isinstance(value, dict):  # Recursively handle nested dictionaries
                sub_frame = tk.Frame(frame, background="darkgray")
                sub_frame.pack(fill='x', expand=True, padx=5, pady=5)
                populate_frame(sub_frame, value, label=key)
            else:
                row_frame = tk.Frame(frame, background="darkgray")
                row_frame.pack(fill='x', expand=True, padx=5, pady=5)
                ttk.Label(row_frame, text=key, background="darkgray").pack(side='left')
                if isinstance(value, list):
                    var = tk.StringVar(row_frame)
                    var.set(value[0])  # default value
                    dropdown = tk.OptionMenu(row_frame, var, *value)
                    dropdown.pack(side='right', fill='x', expand=True)
                elif isinstance(value, int):
                    intvar = tk.IntVar(row_frame)
                    intvar.set(value)
                    entry = tk.Entry(row_frame, textvariable=intvar)
                    entry.pack(side='right', fill='x', expand=True)
