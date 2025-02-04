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
from tkinter import ttk, PhotoImage, messagebox
from .render import SimScholarRender
from .calls import SimScholarCalls
from .ide import SimScholarIDE
from .ide import SimScholarResource
from .stats import SimScholarStats
from main.utils.printdebug import printdebug


class SimScholarFrontend:
    def __init__(self, port: int, path: str) -> None:
        self.ss_configs = {
            "version": "1.1.2",
            "icon": "assets/icon.png",
            "mode": "default",
            "port": port,
            "path": path,
            "theme": "light",
            "hint": "Backend responses will display here."
        }
        self.render = SimScholarRender()
        self.ide = SimScholarIDE()
        self.resource = SimScholarResource()
        self.stat_handler = SimScholarStats(self.ss_configs["path"])
        self.caller = SimScholarCalls(
            self.stat_handler, self.ss_configs["port"], self.ss_configs["path"]
        )
        self.configurations = {
            "boards": self.caller.opt["boards"],
            "processors": self.caller.opt["processor"],
            "memories": self.caller.opt["memory"],
            "caches": self.caller.opt["cache"],
        }
        try:
            self.caller.get_gem5_data()
        except:
            raise ValueError(f"Failed to obtain gem5 data. Is the port correct?")
        self.root = self.root_window()
        self.root.mainloop()

    def verify(self, loc, sections, res, id):
        printdebug("[frontend] verifying resource")
        if len(res) == 0:
            messagebox.showerror("Error", "No Simulation Resource Selected!")
        elif id == None:
            messagebox.showerror("Error", "No Configuration ID!")
        else:
            self.caller.configure_simulation(loc, sections, res, id)

    def root_window(self):
        # Create the main window
        root = tk.Tk()
        root.title(f"SimScholar  v{self.ss_configs['version']}")
        img = PhotoImage(file=self.ss_configs["icon"])
        root.iconphoto(True, img)
        self.styler = SimScholarStyling(root, self.ss_configs["theme"])

        notebook = ttk.Notebook(root)
        notebook.pack(expand=1, fill="both")

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)
        tab5 = ttk.Frame(notebook)
        notebook.add(tab1, text="Configure")
        notebook.add(tab2, text="Saved")
        notebook.add(tab3, text="Code Editor")
        notebook.add(tab4, text="Statistics")
        notebook.add(tab5, text="Options")

        stat_frames = self.stats_window(tab4)
        self.config_window(tab1, stat_frames)
        self.saved_window(tab2)
        self.code_window(tab3)
        self.options_window(tab5)
        return root

    def configure_tabs(self, master):
        tabs = ttk.Notebook(master)
        tabs.pack(side="top", expand=True, fill="both")

        tab1 = self.render.render_section(tabs, self.configurations["boards"], "board")
        tab2 = self.render.render_section(
            tabs, self.configurations["processors"], "processor"
        )
        tab3 = self.render.render_section(
            tabs, self.configurations["memories"], "memory"
        )
        tab4 = self.render.render_section(tabs, self.configurations["caches"], "cache")

        tabs.add(tab1, text="Board")
        tabs.add(tab2, text="Processor")
        tabs.add(tab3, text="Memory")
        tabs.add(tab4, text="Cache Hierarchy")

    def config_window(self, master, stats_frames):
        # Header label
        header_label = ttk.Label(
            master,
            text="Simulation System Configurator",
            font=("TkDefaultFont", 16, "bold"),
        )
        header_label.pack(pady=10, anchor="center")

        # Main frame to hold both the configuration frame and the canvas
        main = ttk.Frame(master)
        main.pack(expand=True, fill="both", padx=10, pady=10)
        # Configuration frame on the left
        frame = ttk.Frame(main, width=300)
        frame.pack(side="left", fill="y", padx=(0, 10))
        # Configuration tabs and resource manager
        self.configure_tabs(frame)  # CONFIGURATION TABS
        self.resource_menu(frame)  # RESOURCE MANAGER
        # Canvas on the right
        sim_output = tk.Text(
            main,
            width=80,
            height=30,
            background="lightgray",
            foreground="black",
            state="disabled",
        )
        sim_output.pack(side="right", fill="both", expand=True)

        # Bottom frame for hint bar and buttons
        bottom = ttk.Frame(master)
        bottom.pack(side="bottom", fill="x", padx=5, pady=5)
        # HINT BAR
        hint_bar = ttk.Label(
            bottom, text=self.ss_configs['hint'], relief=tk.SUNKEN, anchor=tk.W, wraplength=0
        )
        hint_bar.pack(side="top", fill="x")
        # CONFIGURE ID
        id_text = ttk.Label(bottom, text="Config ID", anchor=tk.W, wraplength=0)
        id_text.pack(side="left", padx=5, pady=5)
        id_text_val = tk.IntVar(master)
        id_text_val.set(0)
        id_button = ttk.Entry(bottom, width=10, textvariable=id_text_val)
        id_button.pack(side="left", padx=5, pady=5)
        # CONFIGURE BUTTON
        configure_button = ttk.Button(
            bottom,
            text="Configure",
            command=lambda: self.verify(
                hint_bar,
                self.render.sections,
                self.resource.resource_selected,
                id_text_val.get(),
            ),
            width=30,
        )
        configure_button.pack(side="left", padx=5, pady=5)
        # SIMULATE BUTTON
        simulate_button = ttk.Button(
            bottom,
            text="Simulate",
            command=lambda: self.caller.run_simulation(
                hint_bar, sim_output, stats_frames, id_text_val.get()
            ),
            width=50,
        )
        simulate_button.pack(side="right", padx=2, pady=2)

    def resource_menu(self, master):
        # RESOURCE MANAGER
        resource_vars = [tk.StringVar(master), tk.StringVar(master)]
        resources = ttk.Frame(master)
        resources.pack(side="bottom", pady=10, expand=True, fill="both")
        ttk.Label(
            resources, text="Resource Manager", font=("TkDefaultFont", 10, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")

        resource_vars[1].set(self.resource.gem5_resources[0])
        self.resource.resource_selected = ["default", resource_vars[1].get()]
        menu = ttk.OptionMenu(
            resources,
            resource_vars[1],  # BINARY
            self.resource.gem5_resources[0],
            *self.resource.gem5_resources,
            command=lambda t=resource_vars[1]: self.resource.select_gem5_binary(t),
        )
        custom_button = ttk.Button(
            resources, text="Select Binary", command=self.resource.select_custom_binary
        )

        ttk.Radiobutton(
            master=resources,
            text="gem5 Binary",
            value="default",
            variable=resource_vars[0],  # TYPE
            command=lambda: self.resource.show_resource(
                menu, custom_button, resource_vars
            ),
        ).pack(pady=(10, 5), padx=10, anchor="w")
        ttk.Radiobutton(
            master=resources,
            text="Custom Binary",
            value="custom",
            variable=resource_vars[0],  # TYPE
            command=lambda: self.resource.show_resource(
                menu, custom_button, resource_vars
            ),
        ).pack(pady=(10, 5), padx=10, anchor="w")

    def saved_window(self, master):
        # Header label
        header_label = ttk.Label(
            master, text="Saved Configurations", font=("TkDefaultFont", 16, "bold")
        )
        header_label.pack(pady=10, anchor="center")

        # Main frame to hold both the configuration frame and the canvas
        main = ttk.Frame(master)
        main.pack(expand=True, fill="both", padx=10, pady=10)
        text = tk.Text(
            main,
            width=80,
            height=25,
            font="Courier",
            cursor="arrow",
            background="lightgray",
            foreground="black",
            wrap="none",
            state="disabled",
        )
        text.pack(side="top", fill="both", expand=True)
        button = ttk.Button(
            main, text="Refresh", command=lambda: self.caller.view_saved(text), width=50
        )
        button.pack(side="bottom", padx=2, pady=2)

    def code_window(self, tab):
        header_frame = ttk.Frame(tab)
        header_frame.pack(fill="x", pady=20, padx=20)

        header_label = ttk.Label(
            header_frame,
            text="Simulation Workload Editor",
            font=("TkDefaultFont", 16, "bold"),
        )
        header_label.pack()

        filebutton = tk.Menubutton(tab, text="File", relief=tk.RAISED)
        filebutton.pack(side="left", padx=10, pady=10)

        filemenu = tk.Menu(filebutton, tearoff=0)
        filebutton["menu"] = filemenu

        filemenu.add_command(
            label="Open", command=lambda: self.ide.open_file(text, update_line_numbers)
        )
        filemenu.add_command(label="Save", command=lambda: self.ide.save_file(text))
        filemenu.add_command(
            label="Save As", command=lambda: self.ide.save_as_file(text)
        )

        text_frame = ttk.Frame(tab)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        line_numbers = tk.Text(
            text_frame,
            width=4,
            padx=2,
            borderwidth=0,
            highlightthickness=0,
            background="lightgray",
            foreground="black",
            state=tk.DISABLED,
        )
        line_numbers.pack(side="left", fill="y")

        text = tk.Text(
            text_frame,
            width=80,
            height=15,
            font="Courier",
            cursor="arrow",
            bg="lightgray",
            fg="black",
            wrap="none",
        )
        text.pack(side="left", fill="both", expand=True)

        def update_line_numbers(event=None):
            lines = text.get("1.0", "end").count("\n")
            line_numbers.config(state="normal")
            line_numbers.delete("1.0", "end")
            for i in range(1, lines + 1):
                line_numbers.insert("end", f"{i}\n")
            line_numbers.config(state="disabled")

        text.bind("<MouseWheel>", update_line_numbers)
        text.bind("<Button-4>", update_line_numbers)
        text.bind("<Button-5>", update_line_numbers)
        text.bind("<Key>", update_line_numbers)

        button_frame = ttk.Frame(tab)
        button_frame.pack(fill="x", padx=10, pady=5)

        compile_button = ttk.Button(
            button_frame, text="Compile", command=lambda: self.ide.compile(), width=60
        )
        compile_button.pack(side="right")

    def stats_window(self, stats):
        stats_height = 20

        # Header frame and label
        header_frame = ttk.Frame(stats)
        header_frame.pack(fill="x", pady=20, padx=20)
        header_label = ttk.Label(
            header_frame, text="Simulation Stats", font=("TkDefaultFont", 16, "bold")
        )
        header_label.pack()

        # Create a frame to hold the stat canvases
        stats_frame = ttk.Frame(stats)
        stats_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(stats_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # STAT NAME FRAME
        name_frame = ttk.Frame(stats_frame)
        name_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ttk.Label(name_frame, text="Name", font=("TkDefaultFont", 10, "bold")).pack()
        stats_name = tk.Text(
            name_frame,
            width=50,
            height=stats_height,
            bg="lightgray",
            state="disabled",
            fg="black",
            yscrollcommand=scrollbar.set,
        )
        stats_name.pack(fill="both", expand=True)

        # STAT VALUE FRAME
        value_frame = ttk.Frame(stats_frame)
        value_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ttk.Label(value_frame, text="Value", font=("TkDefaultFont", 10, "bold")).pack()
        stats_val = tk.Text(
            value_frame,
            width=10,
            height=stats_height,
            bg="lightgray",
            state="disabled",
            fg="black",
            yscrollcommand=scrollbar.set,
        )
        stats_val.pack(fill="both", expand=True)

        # STAT COMMENT FRAME
        comment_frame = ttk.Frame(stats_frame)
        comment_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ttk.Label(
            comment_frame, text="Comment", font=("TkDefaultFont", 10, "bold")
        ).pack()
        stats_comment = tk.Text(
            comment_frame,
            width=75,
            height=stats_height,
            bg="lightgray",
            state="disabled",
            fg="black",
            yscrollcommand=scrollbar.set,
        )
        stats_comment.pack(fill="both", expand=True)

        frame = [stats_name, stats_val, stats_comment]

        scrollbar.config(command=lambda *args: sync_scroll(frame, *args))

        def sync_scroll(widgets, *args):
            for widget in widgets:
                widget.yview(*args)

        for text_widget in frame:
            text_widget.config(yscrollcommand=scrollbar.set)
            text_widget.bind(
                "<MouseWheel>",
                lambda event, widgets=frame: sync_scroll(
                    widgets, "scroll", -1 * int(event.delta / 120), "units"
                ),
            )

        # Button frame
        button_frame = ttk.Frame(stats)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=lambda t=frame: self.stat_handler.parse_stats(t),
            width=10,
        )
        refresh_button.pack(side="right")
        diagram_button = ttk.Button(
            button_frame,
            text="View Configuration Diagram",
            command=lambda t=stats: self.stat_handler.config_diagram_window(t),
            width=25,
        )
        diagram_button.pack(side="left")

        return frame

    def options_window(self, master):
        option_list = [
            tk.IntVar(master),  # PORT
            tk.StringVar(master),  # PATH
            tk.StringVar(master),  # STATS MODE
            tk.StringVar(master),  # THEME
        ]
        # Header label
        header_label = ttk.Label(
            master, text="Options", font=("TkDefaultFont", 16, "bold")
        )
        header_label.pack(pady=10, anchor="center")

        # PORT
        ttk.Label(master, text="Port", anchor=tk.W, wraplength=0).pack(padx=5, pady=5)
        option_list[0].set(str(self.ss_configs["port"]))
        ttk.Entry(
            master,
            width=10,
            textvariable=option_list[0],
        ).pack(padx=5, pady=5)

        # GEM5 PATH
        ttk.Label(master, text="Gem5 Path", anchor=tk.W, wraplength=0).pack(
            padx=5, pady=5
        )
        option_list[1].set(self.ss_configs["path"])
        ttk.Entry(
            master,
            width=100,
            textvariable=option_list[1],
        ).pack(padx=5, pady=5)

        # STATS MODE
        ttk.Label(master, text="Stats Mode", anchor=tk.W, wraplength=0).pack(
            padx=5, pady=5
        )
        option_list[2].set(self.ss_configs["mode"])
        ttk.Radiobutton(
            master=master, text="Default Mode", value="default", variable=option_list[2]
        ).pack(pady=(10, 5), padx=10, anchor="center")
        ttk.Radiobutton(
            master=master, text="All Mode", value="all", variable=option_list[2]
        ).pack(pady=(10, 5), padx=10, anchor="center")

        # THEME
        ttk.Label(master, text="Theme", anchor=tk.W, wraplength=0).pack(padx=5, pady=5)
        option_list[3].set(self.ss_configs["theme"])
        ttk.Radiobutton(
            master=master, text="Light", value="light", variable=option_list[3]
        ).pack(pady=(10, 5), padx=10, anchor="center")
        ttk.Radiobutton(
            master=master, text="Dark", value="dark", variable=option_list[3]
        ).pack(pady=(10, 5), padx=10, anchor="center")
        ttk.Radiobutton(
            master=master, text="Navy", value="navy", variable=option_list[3]
        ).pack(pady=(10, 5), padx=10, anchor="center")

        # SHUTDOWN BUTTON
        ttk.Button(
            master,
            text="Shutdown Backend",
            command=lambda: self.shutdown_helper(),
            width=17,
        ).pack(side="bottom", padx=2, pady=2, anchor="se")

        # UPDATE BUTTON
        ttk.Button(
            master,
            text="Save",
            command=lambda: self.update_options(option_list),
            width=50,
        ).pack(side="bottom", padx=2, pady=2)

    def shutdown_helper(self):
        warn = messagebox.askokcancel("Shutdown Backend", "Are you sure you want to terminate the backend server?")
        if warn:
            resp = self.caller.shutdown()
            messagebox.showwarning("Backend Response", resp.json()['message'] + "\nSimScholar will now exit...")
            self.root.destroy()


    def update_options(self, options: list):
        if options[0].get() != self.ss_configs["port"]:
            self.ss_configs["port"] = options[0].get()
            printdebug(f"[options] port updated to {self.ss_configs['port']}.")

        if options[1].get() != self.ss_configs["path"]:
            self.ss_configs["path"] = options[1].get()
            printdebug(f"[options] backend path updated to {self.ss_configs['path']}.")

        self.caller = SimScholarCalls(
            self.stat_handler, self.ss_configs["port"], self.ss_configs["path"]
        )

        if options[2].get() != self.ss_configs["mode"]:
            self.ss_configs["mode"] = options[2].get()
            self.stat_handler.update_mode(self.ss_configs["mode"])
            printdebug(f"[options] stat mode updated to {self.ss_configs['mode']}.")

        if options[3].get() != self.ss_configs["theme"]:
            self.ss_configs["theme"] = options[3].get()
            self.styler.update_theme(self.ss_configs["theme"])
            printdebug(f"[options] theme updated to {self.ss_configs['theme']} mode.")


class SimScholarStyling:
    def __init__(self, root, theme) -> None:
        self.root = root
        self.theme = theme
        self.root.tk.call("source", "assets/themes.tcl")
        self.apply_style()

    def update_theme(self, theme):
        self.theme = theme
        self.apply_style()

    def apply_style(self):
        style = ttk.Style()
        match self.theme:
            case "dark":
                style.theme_use("darkmode")
            case "light":
                style.theme_use("lightmode")
            case "navy":
                style.theme_use("navymode")
            case _:
                raise ValueError(f"Unrecognized theme: {self.theme}")
