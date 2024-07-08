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
import render
from calls import SimScholarCalls as call
from ide import SimScholarIDE as ide
from ide import SimScholarResource as resource
from style import SimScholarStyling as style
from printdebug import printdebug


class frontend:
    def __init__(self) -> None:
        self.mode = "default"
        self.port = 8080
        self.backend_path = "/home/a599m019/Projects/Current/contributing/gem5"
        self.style = style()
        self.caller = call(self.port, self.backend_path)
        self.ide = ide()
        self.resource = resource()
        self.stat_obj = None
        self.boards = self.caller.opt["boards"]
        self.processors = self.caller.opt["processor"]
        self.memories = self.caller.opt["memory"]
        self.caches = self.caller.opt["cache"]

        self.caller.get_gem5_data()
        self.root_window()

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
        ss_version = 1.1
        root.title(f"SimScholar v{ss_version}")
        img = PhotoImage(file="assets/icon.png")
        root.iconphoto(True, img)
        self.style.apply_style("darkmode")

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

        stat_frames = self.stats_window(tab4, self.stat_obj)
        self.config_window(tab1, stat_frames)
        self.saved_window(tab2)
        self.code_window(tab3)
        self.options_window(tab5)
        root.mainloop()

    def configure_tabs(self, master):
        tabs = ttk.Notebook(master)
        tabs.pack(side="top", expand=True, fill="both")

        tab1 = render.render_section(tabs, self.boards, "board")
        tab2 = render.render_section(tabs, self.processors, "processor")
        tab3 = render.render_section(tabs, self.memories, "memory")
        tab4 = render.render_section(tabs, self.caches, "cache")

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
        hint = str("Hints: Some helpful information here")
        hint_bar = ttk.Label(
            bottom, text=hint, relief=tk.SUNKEN, anchor=tk.W, wraplength=0
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
                render.sections,
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
            command=lambda: self.sim_helper(
                hint_bar, sim_output, stats_frames, id_text_val.get()
            ),
            width=50,
        )
        simulate_button.pack(side="right", padx=2, pady=2)

    def resource_menu(self, master):
        # RESOURCE MANAGER
        gem5_resources = ["x86-hello64-static", "arm-hello64-static"]

        resource_type = tk.StringVar()
        resource_binary = tk.StringVar()
        resources = ttk.Frame(master)
        resources.pack(side="bottom", pady=10, expand=True, fill="both")
        ttk.Label(
            resources, text="Resource Manager", font=("TkDefaultFont", 10, "bold")
        ).pack(pady=(10, 5), padx=10, anchor="w")

        def show_resource(resource_type):
            global resource_selected
            r = resource_type.get()
            if r == "default":
                custom_button.pack_forget()
                resource_selected = ["default", gem5_resources[0]]
                menu.pack(pady=(10, 5), padx=10, anchor="se")
            elif r == "custom":
                menu.pack_forget()
                custom_button.pack(pady=(10, 5), padx=10, anchor="se")

        ttk.Radiobutton(
            master=resources,
            text="gem5 Binary",
            value="default",
            variable=resource_type,
            command=lambda s=resource_type: show_resource(s),
        ).pack(pady=(10, 5), padx=10, anchor="w")
        ttk.Radiobutton(
            master=resources,
            text="Custom Binary",
            value="custom",
            variable=resource_type,
            command=lambda s=resource_type: show_resource(s),
        ).pack(pady=(10, 5), padx=10, anchor="w")

        menu = tk.OptionMenu(
            resources,
            resource_binary,
            *gem5_resources,
            command=lambda t=resource_binary: self.resource.select_gem5_binary(t),
        )
        resource_binary.set(gem5_resources[0])

        custom_button = ttk.Button(
            resources, text="Select Binary", command=self.resource.select_custom_binary
        )

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

    def stats_window(self, stats, obj):
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

        # STAT NAME FRAME
        name_frame = ttk.Frame(stats_frame)
        name_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ttk.Label(name_frame, text="Name", font=("TkDefaultFont", 10, "bold")).pack()
        stats_name = tk.Canvas(
            name_frame, width=350, height=stats_height * 20, bg="lightgray"
        )
        stats_name.pack(fill="both", expand=True)

        # STAT VALUE FRAME
        value_frame = ttk.Frame(stats_frame)
        value_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ttk.Label(value_frame, text="Value", font=("TkDefaultFont", 10, "bold")).pack()
        stats_val = tk.Canvas(
            value_frame, width=100, height=stats_height * 20, bg="lightgray"
        )
        stats_val.pack(fill="both", expand=True)

        # STAT COMMENT FRAME
        comment_frame = ttk.Frame(stats_frame)
        comment_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        ttk.Label(
            comment_frame, text="Comment", font=("TkDefaultFont", 10, "bold")
        ).pack()
        stats_comment = tk.Canvas(
            comment_frame, width=400, height=stats_height * 20, bg="lightgray"
        )
        stats_comment.pack(fill="both", expand=True)

        frame = [stats_name, stats_val, stats_comment]

        # Button frame
        button_frame = ttk.Frame(stats)
        button_frame.pack(fill="x", padx=10, pady=5, side="bottom")

        refresh_button = ttk.Button(
            button_frame,
            text="Refresh",
            command=lambda t=frame: obj.parse_stats(t),
            width=10,
        )
        refresh_button.pack(side="right")
        diagram_button = ttk.Button(
            button_frame,
            text="View Configuration Diagram",
            command=lambda t=stats: obj.config_diagram_window(t),
            width=25,
        )
        diagram_button.pack(side="left")

        if self.mode == "all":
            prev_button = ttk.Button(
                button_frame,
                text="Previous",
                command=lambda t=frame: self.show_stats(t, False),
                width=20,
            )
            prev_button.pack(side="left", padx=10)

            next_button = ttk.Button(
                button_frame,
                text="Next",
                command=lambda t=frame: self.show_stats(t, True),
                width=20,
            )
            next_button.pack(side="right", padx=10)
        return frame

    def options_window(self, master):
        option_list = [tk.IntVar(master), tk.StringVar(master)]
        # Header label
        header_label = ttk.Label(
            master, text="Options", font=("TkDefaultFont", 16, "bold")
        )
        header_label.pack(pady=10, anchor="center")

        # PORT
        ttk.Label(master, text="Port", anchor=tk.W, wraplength=0).pack(padx=5, pady=5)
        option_list[0].set(str(self.port))
        ttk.Entry(
            master,
            width=10,
            textvariable=option_list[0],
        ).pack(padx=5, pady=5)

        # GEM5 PATH
        ttk.Label(master, text="Gem5 Path", anchor=tk.W, wraplength=0).pack(
            padx=5, pady=5
        )
        option_list[1].set(self.backend_path)
        ttk.Entry(
            master,
            width=100,
            textvariable=option_list[1],
        ).pack(padx=5, pady=5)

        # UPDATE BUTTON
        ttk.Button(
            master,
            text="Save",
            command=lambda: self.update_options(option_list),
            width=50,
        ).pack(side="bottom", padx=2, pady=2)

    def update_options(self, options: list):
        new_port = options[0].get()
        self.port = new_port
        print(f"Port updated to {new_port}.")

        new_path = options[1].get()
        self.backend_path = new_path
        print(f"Backend path updated to {new_path}.")

        self.caller = call(self.port, self.backend_path)

    def sim_helper(self, hint_bar, sim_output, stats_frames, id_text_val):
        self.stats_obj = self.caller.run_simulation(
                hint_bar, sim_output, stats_frames, id_text_val
            )


myfrontend = frontend()
