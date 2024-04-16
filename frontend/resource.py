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
from tkinter import ttk, filedialog
from printdebug import printdebug
resource_selected = []

def select_custom_binary():
    global resource_selected
    binary = filedialog.askopenfilename(defaultextension="", filetypes=[("Binaries", "*.out")], initialdir="./workloads", title="Select Custom Binary")
    resource_selected = ['custom', binary]
    printdebug(f'[resource] {resource_selected[1]}')

def select_gem5_binary(binary):
    global resource_selected
    resource_selected = ['default', binary]
    printdebug(f'[resource] {resource_selected}')

def rsrc_menu(master):
# RESOURCE MANAGER
    gem5_resources = ["x86-hello64-static", 'arm-hello64-static']

    resource_type = tk.StringVar()
    resource_binary = tk.StringVar()
    resources = tk.Frame(master, background="darkgray")
    resources.grid(row=2, rowspan=10, column=0, pady=10, sticky="nsew")
    ttk.Label(resources, text="Resource Manager", font=('TkDefaultFont', 10, 'bold'), background="darkgray").pack(pady=(10, 5), padx=10, anchor='w')

    def show_resource(resource_type):
        r = resource_type.get()
        if r == 'default':
            custom_button.pack_forget()
            menu.pack(pady=(10, 5), padx=10, anchor='se')
        elif r == 'custom':
            menu.pack_forget()
            custom_button.pack(pady=(10, 5), padx=10, anchor='se')

    tk.Radiobutton(master=resources, 
                    text="gem5 Binary", 
                    value='default', 
                    variable=resource_type, 
                    bg="darkgray", 
                    fg="black", 
                    command = lambda s=resource_type: show_resource(s),
                    borderwidth=0).pack(pady=(10, 5), padx=10, anchor='w')
    tk.Radiobutton(master=resources, 
                    text="Custom Binary", 
                    value='custom', 
                    variable=resource_type, 
                    bg="darkgray", 
                    fg="black", 
                    command = lambda s=resource_type: show_resource(s),
                    borderwidth=0).pack(pady=(10, 5), padx=10, anchor='w')
    
    menu = tk.OptionMenu(resources,
                   resource_binary,
                   *gem5_resources,
                   command=lambda t=resource_binary: select_gem5_binary(t))
    
    custom_button = tk.Button(resources, 
                              text="Select Binary", 
                              command=select_custom_binary)
