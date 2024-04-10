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

def rsrc_menu(master):
# RESOURCE MANAGER

    gem5_resources = ["x86-hello-static", 'arm-hello-static']

    resource_type = tk.StringVar()
    resource_binary = tk.StringVar()
    resources = tk.Frame(master, background="darkgray")
    resources.grid(row=2, rowspan=10, column=0, pady=10, sticky="nsew")
    ttk.Label(resources, text="Resource Manager", font=('TkDefaultFont', 10, 'bold'), background="darkgray").pack(pady=(10, 5), padx=10, anchor='w')

    def show_resource():
        r = resource_type.get()
        print(r)
        if r == 'default':
            custom_button.pack_forget()
            menu.pack(pady=(10, 5), padx=10, anchor='se')
        else:
            menu.pack_forget()
            custom_button.pack(pady=(10, 5), padx=10, anchor='se')

    def select_custom_binary(res):
        res = filedialog.askopenfilename(defaultextension="", filetypes=[("Binaries", "*")], initialdir="./workloads", title="Select Custom Binary")
        print(res)

    tk.Radiobutton(master=resources, 
                    text="gem5 Binary", 
                    value='default', 
                    variable=resource_type, 
                    bg="darkgray", 
                    fg="black", 
                    command = show_resource,
                    borderwidth=0).pack(pady=(10, 5), padx=10, anchor='w')
    tk.Radiobutton(master=resources, 
                    text="Custom Binary", 
                    value='custom', 
                    variable=resource_type, 
                    bg="darkgray", 
                    fg="black", 
                    command = show_resource,
                    borderwidth=0).pack(pady=(10, 5), padx=10, anchor='w')
    
    menu = ttk.OptionMenu(resources,
                   resource_binary,
                   *gem5_resources)
    
    custom_button = tk.Button(resources, 
                              text="Select Binary", 
                              command=lambda d=resource_binary: select_custom_binary(d))
