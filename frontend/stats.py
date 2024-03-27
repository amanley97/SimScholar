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

def stats_window(stats):

    header_label = tk.Label(stats, text="Simulation Stats Visualizer", font=('TkDefaultFont', 16, 'bold'), bg="gray", fg="black")
    header_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

    stats.grid_rowconfigure(1, weight=1)
    stats.grid_columnconfigure(0, weight=1)