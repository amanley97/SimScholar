import tkinter as tk
from tkinter import messagebox, Toplevel
from main.utils.printdebug import printdebug
import os
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class SimScholarStats:
    def __init__(self, path) -> None:
        self.mode = "default"
        self.path = path
        self.sim_id = 0
        self.config_id = 0
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

    def _show_stats(self, text_widgets):
        def display_stat(text_widget, array):
            for line in array:
                text_widget.insert(tk.END, line + "\n")

        printdebug("[stats] displaying stats")
        name_text, value_text, comment_text = text_widgets

        # Temporarily enable text boxes
        for text_widget in text_widgets:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete("1.0", tk.END)

        # Display stats
        if self.mode == "default":
            display_stat(name_text, [self.names[i] for i in self.stats_found])
            display_stat(value_text, [self.values[i] for i in self.stats_found])
            display_stat(comment_text, [self.comments[i] for i in self.stats_found])
        elif self.mode == "all":
            display_stat(name_text, self.names)
            display_stat(value_text, self.values)
            display_stat(comment_text, self.comments)

        # Disable text boxes
        for text_widget in text_widgets:
            text_widget.config(state=tk.DISABLED)

    def _search_stats(self, list, term):
        search_substring_lower = term.lower()
        indices = [
            index
            for index, item in enumerate(list)
            if search_substring_lower in item.lower()
        ]
        for i in range(len(indices)):
            self.stats_found.append(indices[i])
        return self.stats_found

    def update_id(self, sim_id, config_id):
        self.sim_id = sim_id
        self.config_id = config_id

    def update_mode(self, mode):
        if mode == "default":
            self.mode = "default"
        elif mode == "all":
            self.mode = "all"
        else:
            printdebug("[error] invalid stats mode.")

    def parse_stats(self, text_widgets):
        out_path = (
            self.path + f"/m5out/config_{self.config_id}_sim_{self.sim_id}/stats.txt"
        )
        printdebug(f"[stats] Refreshing Stats: {out_path}")
        if not os.path.exists(out_path):
            printdebug(f"[stats] file {out_path} not found.")
            messagebox.showerror("Error", "No Stats file found!")
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
                                self.comments.append("")
        except FileNotFoundError:
            print("The file was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        if self.mode == "default":
            self.stats_found.clear()
            for term in self.default_stats:
                self._search_stats(self.names, term)
            printdebug(f"[stats] {len(self.stats_found)} stats found")
            if len(self.stats_found) > 0:
                self._show_stats(text_widgets)
            else:
                messagebox.showerror("Error", "No Stats file found!")
        else:
            self._show_stats(text_widgets)

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
        top.title(f"Configuration Diagram: config_{self.config_id}_sim_{self.sim_id}")

        canvas = tk.Canvas(top, width=image.width, height=image.height)
        canvas.pack()
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.image = photo


# Example usage:
# root = tk.Tk()
# name_text = tk.Text(root, width=50, height=10).pack()
# value_text = tk.Text(root, width=20, height=10).pack()
# comment_text = tk.Text(root, width=50, height=10).pack()

# sim_stats = SimScholarStats("/path/to/stats")
# sim_stats.update_mode("all")  # or "default" based on requirement
# sim_stats.parse_stats((name_text, value_text, comment_text))

# root.mainloop()
