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
from printdebug import printdebug
sections = {}
cache_entries = []

def render_section(master, opts, title):
    # Create a section frame
    section_frame = tk.Frame(master, background="darkgray")

    #Populate it!!
    printdebug(f"[render] rendering section {title}")
    sections[title] = populate_frame(section_frame, opts, title)

    return section_frame

def update_selected(title, key, newval):
    oldval = sections[title][key]
    if newval.get() != oldval:
        sections[title][key] = newval.get()
    if title == "Cache Configuration":
        cache_select(key)

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
            entry = ttk.Entry(row_frame, textvariable=intvar)
            entry.pack(side='right', fill='x', expand=True)
            saved_opts[key] = intvar.get()
            entry.bind("<Return>", lambda event=None, t=label, d=key, v=intvar: update_selected(t, d, v))
            if label == "Cache Configuration":
                entry.config(state='disabled')
                cache_entries.append(entry)
    return saved_opts

def cache_select(type):
    cache_type = sections['Cache Configuration'][type]
    l1d_size = cache_entries[0]
    l1i_size = cache_entries[1]
    l2_size = cache_entries[2]
    l1d_assoc = cache_entries[3]
    l1i_assoc = cache_entries[4]
    l2_assoc = cache_entries[5]

    if cache_type == 'NoCache':
        printdebug("[render] selected no cache")
        l1d_size.config(state='disabled') # disable L1I size
        l1i_size.config(state='disabled') # disable L1D size
        l2_size.config(state='disabled') # disable L2 size
        l1d_assoc.config(state='disabled')
        l1i_assoc.config(state='disabled')
        l2_assoc.config(state='disabled')
    elif cache_type == 'PrivateL1CacheHierarchy':
        printdebug("[render] selected L1 only")
        l1d_size.config(state='normal') # enable L1I size
        l1i_size.config(state='normal') # enable L1D size
        l2_size.config(state='disabled') # disable L2 size
        l1d_assoc.config(state='disabled')
        l1i_assoc.config(state='disabled')
        l2_assoc.config(state='disabled')
    elif cache_type == 'PrivateL1PrivateL2CacheHierarchy':
        printdebug("[render] selected L1 and L2")
        l1d_size.config(state='normal') # enable L1I size
        l1i_size.config(state='normal') # enable L1D size
        l2_size.config(state='normal') # enable L2 size
        l1d_assoc.config(state='disabled')
        l1i_assoc.config(state='disabled')
        l2_assoc.config(state='disabled')
    elif cache_type == 'PrivateL1SharedL2CacheHierarchy':
        printdebug("[render] selected L1 and shared L2")
        l1d_size.config(state='normal') # enable L1I size
        l1i_size.config(state='normal') # enable L1D size
        l2_size.config(state='normal') # enable L2 size
        l1d_assoc.config(state='normal')
        l1i_assoc.config(state='normal')
        l2_assoc.config(state='normal')