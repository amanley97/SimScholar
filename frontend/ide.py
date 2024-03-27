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
from tkinter import filedialog
from tkinter import ttk

# Function to save the text to a file
def save_file(text):
    file_path = filedialog.asksaveasfilename(defaultextension=".c", 
                                             filetypes=[("C Program Files", "*.c"), ("All files", "*.*")],
                                             initialdir="./test-progs")
    if file_path:
        with open(file_path, "w") as file:
            text_content = text.get("1.0", "end-1c")  # Get the content of the text widget
            file.write(text_content)

# Function to open a file
def open_file(text, func):
    file_path = filedialog.askopenfilename(filetypes=[("C Program Files", "*.c"), ("All files", "*.*")],
                                           initialdir="./test-progs")
    if file_path:
        with open(file_path, "r") as file:
            file_content = file.read()
            text.delete("1.0", "end")
            text.insert("1.0", file_content)
    func()

def code_window(code):

    header_label = tk.Label(code, text="Simulation Workload Editor", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="black")
    header_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

    notebook = ttk.Notebook(code)
    notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")

    tab1 = tk.Frame(notebook, background="darkgray")
    tab2 = tk.Frame(notebook, background="darkgray")

    notebook.add(tab1, text="Code")
    notebook.add(tab2, text="File")

    # Text widget for displaying line numbers
    line_numbers = tk.Text(tab1, width=4, padx=4, borderwidth=0, highlightthickness=0, background="gray", foreground="white")
    line_numbers.grid(row=0, column=0, sticky="nsew")

    text = tk.Text(tab1, 
                   width=80, 
                   height=20,
                   font="Courier",
                   cursor="arrow", 
                   bg="lightgray",
                   fg="black",
                   wrap="none")  # disable text wrapping
    text.grid(row=0, column=1, sticky="nsew")

    padd = tk.Text(tab1, width=4, padx=4, borderwidth=0, highlightthickness=0, background="gray", foreground="white")
    padd.grid(row=0, column=2, sticky="nsew")

    # Function to update line numbers
    def update_line_numbers(event=None):
        lines = text.get("1.0", "end").count("\n")
        line_numbers.config(state="normal")
        line_numbers.delete("1.0", "end")
        for i in range(1, lines + 1):
            line_numbers.insert("end", f"{i}\n")
        line_numbers.config(state="disabled")

    # Bind scrollbar movements to update line numbers
    text.bind("<MouseWheel>", update_line_numbers)
    text.bind("<Button-4>", update_line_numbers)
    text.bind("<Button-5>", update_line_numbers)
    text.bind("<Key>", update_line_numbers)

    save_button = tk.Button(tab2, text="Save", command=lambda: save_file(text))
    save_button.grid(row=0, column=0, padx=5, pady=10)

    open_button = tk.Button(tab2, text="Open", command=lambda: open_file(text, update_line_numbers))
    open_button.grid(row=0, column=1, padx=5, pady=10)

    code.bind("<Control-s>", lambda event: save_file(text))
    code.bind("<Control-o>", lambda event: open_file(text, update_line_numbers))

    code.grid_rowconfigure(1, weight=1)
    code.grid_columnconfigure(0, weight=1)

# code_window()
