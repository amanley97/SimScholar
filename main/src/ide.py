import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
from main.utils.printdebug import printdebug


class SimScholarIDE:
    def __init__(self) -> None:
        self.file_info = {"file_path": None, "compile_path": None}

    def save_as_file(self, text):
        self.file_info["file_path"] = None
        self.file_info["compile_path"] = None
        printdebug(f"[ide] save file as")
        self.save_file(text)

    def save_file(self, text):
        if (
            "file_path" in self.file_info and self.file_info["file_path"]
        ):  # Check if there is a previously saved file
            printdebug(f"[ide] saving file: {self.file_info['file_path']}")
            with open(self.file_info["file_path"], "w") as file:
                text_content = text.get("1.0", "end-1c")
                file.write(text_content)
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".c",
                filetypes=[("C Program Files", "*.c"), ("All files", "*.*")],
                initialdir="./workloads",
            )
            printdebug(f"[ide] saving file: {file_path}")
            if file_path:
                with open(file_path, "w") as file:
                    text_content = text.get("1.0", "end-1c")
                    file.write(text_content)
                self.file_info["file_path"] = file_path  # Store the new file path

    def open_file(self, text, func):
        file_path = filedialog.askopenfilename(
            defaultextension=".c",
            filetypes=[("C Program Files", "*.c"), ("All files", "*.*")],
            initialdir="./workloads",
        )
        printdebug(f"[ide] opening file: {file_path}")
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read()
                text.delete("1.0", "end")
                text.insert("1.0", file_content)
            self.file_info["file_path"] = file_path  # Update the file path
            func()

    def compile(self):
        printdebug("[ide] compiling user program")

        if self.file_info["file_path"] is None:
            messagebox.showerror("Error", "File must be saved before compiling!")
        elif self.file_info["compile_path"] is None:
            messagebox.showerror("Error", "Please specify executable path!")
            self.file_info["compile_path"] = filedialog.asksaveasfilename(
                defaultextension="",
                filetypes=[("C Binary", "*.out")],
                initialdir="./workloads",
                title="Save Binary As",
            )

            srcname = self.file_info["file_path"]
            execpath = self.file_info["compile_path"]
            cmd = ["gcc", "-O2", srcname, "-o", execpath]
            p = subprocess.Popen(cmd)
            p.wait()
            messagebox.showinfo("Information", "Workload Compiled Successfully!")


class SimScholarResource:
    def __init__(self) -> None:
        self.resource_selected = []
        self.gem5_resources = ["x86-hello64-static", "arm-hello64-static"]

    def select_custom_binary(self):
        binary = filedialog.askopenfilename(
            defaultextension="",
            filetypes=[("Binaries", "*.out")],
            initialdir="./workloads",
            title="Select Custom Binary",
        )
        self.resource_selected = ["custom", binary]
        printdebug(f"[resource] selected: {self.resource_selected[1]}")

    def select_gem5_binary(self, binary):
        self.resource_selected = ["default", binary]
        printdebug(f"[resource] selected: {self.resource_selected[1]}")

    def show_resource(self, menu, button, resource):
        r = resource[0].get()
        if r == "default":
            button.pack_forget()
            self.resource_selected = ["default", self.gem5_resources[0]]
            menu.pack(pady=(10, 5), padx=10, anchor="se")
        elif r == "custom":
            menu.pack_forget()
            button.pack(pady=(10, 5), padx=10, anchor="se")
