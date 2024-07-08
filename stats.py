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
from tkinter import messagebox, Toplevel, Canvas
from printdebug import printdebug
import os
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class SimScholarStats:
    def __init__(self, path, sim_id, config_id) -> None:
        self.mode = "default"
        self.path = path
        self.sim_id = sim_id
        self.config_id = config_id
        self.names = []
        self.values = []
        self.comments = []
        self.stats_found = []
        self.default_stats = [
            "numcycles",
            "simseconds",
            "simticks",
            "finaltick",
            "siminsts",
            "simops",
            "overallhits::total",
            "overallmisses::total",
        ]
        self.line_range = [0, 10]

    def parse_stats(self, text):
        printdebug("[stats] Refreshing Stats")
        out_path = (
            self.path + f"/m5out/config_{self.config_id}_sim_{self.sim_id}/stats.txt"
        )
        if not os.path.exists(out_path):
            printdebug(f"[stats] file {out_path} not found.")
            messagebox.showerror("Error", "No Configuration Diagram found!")
            return
        self.names.clear()
        self.values.clear()
        self.comments.clear()

        # Flag to skip non-data lines
        data_started = False

        try:
            with open(out_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line.startswith(
                        "---------- Begin Simulation Statistics ----------"
                    ):
                        data_started = True
                        continue  # Skip the header line
                    if data_started and line:  # Process lines only after the header
                        if line.startswith("#"):  # Skip lines that start with '#'
                            continue
                        # Split the line into parts based on multiple spaces
                        parts = line.split(maxsplit=2)
                        if len(parts) >= 2:
                            self.names.append(parts[0].strip())
                            self.values.append(parts[1].strip())
                            # Some lines may not have comments, so check the length
                            if len(parts) == 3:
                                self.comments.append(parts[2].strip())
                            else:
                                self.comments.append(
                                    ""
                                )  # Append an empty string if no comment

        except FileNotFoundError:
            print("The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        if self.mode == "default":
            self.stats_found.clear()
            for term in self.default_stats:
                self.search_stats(self.names, term)
            printdebug(f"[stats] {len(self.stats_found)} stats found")
            if len(self.stats_found) > 0:
                self.show_stats(text)
            else:
                messagebox.showerror("Error", "No Stats file found!")
        else:
            line_range = [0, 10]
            self.show_stats(text)

    def show_stats(self, text):
        def display_stat(canvas, array, index, width, size):
            # Position to start drawing text
            x = 10
            y = 10
            for line in index:
                canvas.create_text(
                    x,
                    y,
                    text=array[line],
                    anchor="nw",
                    font=("Courier", size),
                    width=width,
                )
                y += 30  # Move to the next line position

        printdebug("[stats] displaying stats")
        name_text = text[0]
        value_text = text[1]
        comment_text = text[2]

        # Clear text boxes
        name_text.delete("all")
        value_text.delete("all")
        comment_text.delete("all")

        if self.mode == "default":
            display_stat(name_text, self.names, self.stats_found, 340, 11)
            display_stat(value_text, self.values, self.stats_found, 90, 12)
            display_stat(comment_text, self.comments, self.stats_found, 390, 9)

    def search_stats(self, list, term):
        search_substring_lower = term.lower()
        indices = [
            index
            for index, item in enumerate(list)
            if search_substring_lower in item.lower()
        ]
        for i in range(len(indices)):
            self.stats_found.append(indices[i])
        return self.stats_found

    def config_diagram_window(self, root, scale=0.6):
        svg_path = (
            self.path
            + f"/m5out/config_{self.config_id}_sim_{self.sim_id}/config.dot.svg"
        )
        if not os.path.exists(svg_path):
            printdebug(f"[stats] file {svg_path} not found.")
            messagebox.showerror("Error", "No Configuration Diagram found!")
            return

        drawing = svg2rlg(svg_path)
        image = renderPM.drawToPIL(drawing)
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

        top = Toplevel(root)
        top.title("Configuration Diagram")

        canvas = Canvas(top, width=image.width, height=image.height)
        canvas.pack()
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.image = photo
