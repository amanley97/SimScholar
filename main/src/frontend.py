import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox
from tkinter import Toplevel
import os
import requests
import webbrowser

from .render import SimScholarRender
from .calls import SimScholarCalls
from .ide import SimScholarIDE
from .ide import SimScholarResource
from .stats import SimScholarStats
from main.utils.printdebug import printdebug
<<<<<<< Updated upstream
from subprocess import Popen
import time
=======
from main.utils.activity_logger import log_activity

>>>>>>> Stashed changes


class SimScholarFrontend:
    def __init__(self, port: int, path: str, process: Popen) -> None:
        self.ss_configs = {
            "version": "1.1.2",
            "icon": "main/assets/icon.png",
            "mode": "default",
            "port": port,
            "path": path,
            "theme": "light"
        }
        self.render = SimScholarRender()
        self.ide = SimScholarIDE()
        self.resource = SimScholarResource()
        self.stat_handler = SimScholarStats()
        self.caller = SimScholarCalls(
            self.stat_handler, self.ss_configs["port"], self.ss_configs["path"]
        )
        self.configurations = {
            "boards": self.caller.opt["boards"],
            "processors": self.caller.opt["processor"],
            "memories": self.caller.opt["memory"],
            "caches": self.caller.opt["cache"],
        }
        self.process = process
        self.start_output_thread()

        try:
            self.caller.get_gem5_data()
        except:
            raise ValueError(f"Failed to obtain gem5 data. Is the port correct?")
        self.root = self.root_window()
        self.add_ai_assistant(self.root)
        self.root.mainloop()

    # def update_wraplength(event=None):
    #     hint_bar.config(wraplength=bottom.winfo_width())

    def start_output_thread(self):
        import threading
        """Starts a background thread to capture gem5 output without freezing the UI."""
        threading.Thread(target=self.update_output, daemon=True).start()

    def verify(self, sections, res, id):
        printdebug("[frontend] verifying resource")
        if len(res) == 0:
            messagebox.showerror("Error", "No Simulation Resource Selected!")
        elif id == None:
            messagebox.showerror("Error", "No Configuration ID!")
        else:
            self.caller.configure_simulation(sections, res, id)

    def root_window(self) -> tk.Tk:
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

        notebook.bind("<<NotebookTabChanged>>", self.on_tab_switch)


        stat_frames = self.stats_window(tab4)
        self.config_window(tab1, stat_frames)
        self.saved_window(tab2)
        self.code_window(tab3)
        self.options_window(tab5)
        return root

<<<<<<< Updated upstream
    def configure_tabs(self, master: ttk.Frame):
=======
    def on_tab_switch(self, event):
        tab = event.widget.tab(event.widget.select(), "text")
        log_activity("clicked_main_tab", tab_name=tab)

    def configure_tabs(self, master):
>>>>>>> Stashed changes
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

    def update_output(self):
        """Reads stdout line by line and updates the Tkinter Text widget without blocking."""
        while self.process.poll() is None:  # Process is still running
            line = self.process.stdout.readline()
            if line:  # Only update if there is new output
                self.root.after(0, self.append_output, line)  # Schedule UI update

        self.process.stdout.close()
        time.sleep(0.1)

    def append_output(self, line):
        """Updates the Text widget with new gem5 output."""
        self.sim_output.config(state="normal")
        self.sim_output.insert(tk.END, line)
        self.sim_output.see(tk.END)  # Auto-scroll
        self.sim_output.config(state="disabled")
    
    def clear_output_and_sim(self, config_id):
        """Clears the simulation output textbox."""
        self.sim_output.config(state="normal")  # Enable editing
        self.sim_output.delete("1.0", tk.END)  # Delete all text
        self.sim_output.config(state="disabled")  # Disable editing

        self.caller.run_simulation(config_id)

    def config_window(self, master: ttk.Frame, stats_frames: ttk.Frame):
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
        self.sim_output = tk.Text(
            main,
            width=80,
            height=30,
            background="lightgray",
            foreground="black",
            state="disabled",
        )
        self.sim_output.pack(side="right", fill="both", expand=True)

        # Bottom frame for hint bar and buttons
        bottom = ttk.Frame(master)
        bottom.pack(side="bottom", fill="x", padx=5, pady=5)

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
<<<<<<< Updated upstream
            command=lambda: self.verify(
=======
            command=lambda: self.configure_and_log(
                hint_bar,
>>>>>>> Stashed changes
                self.render.sections,
                self.resource.resource_selected,
                id_text_val.get(),
            ),
            width=30,
        ).pack(side="left", padx=5, pady=5)

        # SIMULATE BUTTON
        simulate_button = ttk.Button(
            bottom,
            text="Simulate",
<<<<<<< Updated upstream
            command=lambda: self.clear_output_and_sim(id_text_val.get()),
=======
            command=lambda: self.simulate_and_log(
                hint_bar, sim_output, stats_frames, id_text_val.get()
            ),
>>>>>>> Stashed changes
            width=50,
        ).pack(side="right", padx=2, pady=2)

        def simulate_and_log(self, hint_bar, sim_output, stats_frames, config_id):
            log_activity("run_simulation", config_id=config_id)
            self.caller.run_simulation(hint_bar, sim_output, stats_frames, config_id)

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

    def toggle_ai_window(self):
        if self.ai_chat_win.state() == "withdrawn":
            self.ai_chat_win.deiconify()
        else:
            self.ai_chat_win.withdraw()

    
    def add_ai_assistant(self, master):
        # Floating button
        ai_button = tk.Button(
            master,
            text="💬",
            font=("Arial", 14),
            command=self.toggle_ai_window,
            bg="#4CAF50",
            fg="white",
            bd=0,
            relief=tk.RAISED
        )
        ai_button.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)

        # Chat popup
        self.ai_chat_win = tk.Toplevel(master)
        self.ai_chat_win.title("Gem5 AI Assistant")
        self.ai_chat_win.geometry("400x550")
        self.ai_chat_win.withdraw()
        self.ai_chat_win.protocol("WM_DELETE_WINDOW", self.toggle_ai_window)

        # Chat display
        self.chat_text = tk.Text(self.ai_chat_win, state="disabled", wrap="word", bg="white", fg="black")
        self.chat_text.pack(side="top", fill="both", expand=True, padx=10, pady=(10, 0))

        # Input bar
        input_frame = tk.Frame(self.ai_chat_win)
        input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.chat_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.chat_entry.pack(side="left", fill="x", expand=True)

        send_button = tk.Button(input_frame, text="Send", command=self.send_to_ai)
        send_button.pack(side="right", padx=(10, 0))


    def send_to_ai(self):
        from main.utils.activity_logger import log_activity

        msg = self.chat_entry.get().strip()
        if not msg:
            return

        self.chat_entry.delete(0, tk.END)

        # Log the user's question
        log_activity("ai_query", question=msg)

        self.chat_text.config(state="normal")
        self.chat_text.insert(tk.END, f"You: {msg}\n")
        self.chat_text.config(state="disabled")

        try:
            response = requests.post("http://localhost:5000/ask", json={"question": msg})
            data = response.json()
            explanation = data.get("explanation", "[No explanation returned]")
            graph_url = data.get("graph_url", None)

            # ✅ Log the response itself
            log_activity(
                "ai_chat",
                question=msg,
                response=explanation.strip() if explanation else "[empty response]"
            )

        except Exception as e:
            explanation = f"[Error] Failed to connect to AI: {e}"
            graph_url = None
            log_activity("ai_chat", question=msg, response=explanation)

        if explanation == "__TABLE__" and isinstance(data.get("metrics"), list):
            self.show_ai_table(data["metrics"])
        else:
            self.chat_text.config(state="normal")
            self.chat_text.insert(tk.END, f"AI: {explanation}\n")
            self.chat_text.config(state="disabled")

        if graph_url:
            try:
                import webbrowser
                graph_path = os.path.abspath("static/graph.png")
                self.chat_text.config(state="normal")
                self.chat_text.insert(tk.END, "[Graph generated — opening in viewer]\n")
                self.chat_text.config(state="disabled")
                webbrowser.open(f"file://{graph_path}")
            except Exception as e:
                self.chat_text.config(state="normal")
                self.chat_text.insert(tk.END, f"[Error opening graph: {e}]\n")
                self.chat_text.config(state="disabled")

        self.chat_text.config(state="normal")
        self.chat_text.insert(tk.END, "\n")
        self.chat_text.config(state="disabled")
        self.chat_text.see(tk.END)

    def show_ai_table(self, metrics):
        table_win = tk.Toplevel(self.root)
        table_win.title("Simulation Analysis")

        columns = ["Metric", "Value", "Meaning", "Interpretation"]
        tree = ttk.Treeview(table_win, columns=columns, show="headings")

        # Set column headers
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        # Insert data into the tree
        for m in metrics:
            tree.insert("", "end", values=(
                m.get('name', ''),
                m.get('value', ''),
                m.get('meaning', ''),
                m.get('interpretation', '')
            ))

        tree.pack(expand=True, fill="both")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def render_metrics_table(self, data):
        # Clear existing chat box contents
        for widget in self.chat_text.winfo_children():
            widget.destroy()
        self.chat_text.pack_forget()

        # Create Treeview table
        table = ttk.Treeview(self.ai_chat_win, columns=("Metric", "Value", "Meaning", "Interpretation"), show="headings", height=10)
        table.heading("Metric", text="Metric")
        table.heading("Value", text="Value")
        table.heading("Meaning", text="Meaning")
        table.heading("Interpretation", text="Interpretation")

        table.column("Metric", width=120)
        table.column("Value", width=80)
        table.column("Meaning", width=200)
        table.column("Interpretation", width=120)

        # Insert data
        for metric in data:
            table.insert("", "end", values=(
                metric["name"],
                metric["value"],
                metric["meaning"],
                metric["interpretation"]
            ))

        table.pack(expand=True, fill="both", padx=10, pady=10)

    def simulate_and_log(self, hint_bar, sim_output, stats_frames, config_id):
        # Simple event
        log_activity("clicked_button", button_id="Simulate", config_id=config_id)

        # Detailed run metadata
        log_activity("run_simulation", config_id=config_id)

        self.caller.run_simulation(hint_bar, sim_output, stats_frames, config_id)

    def configure_and_log(self, hint_bar, sections, resource, config_id):
        
            # Simple event
        log_activity("clicked_button", button_id="Configure", config_id=config_id)

        # Rich, detailed config
        log_activity("configure_sim", config_id=config_id, sections=sections, resource=resource)

        self.verify(hint_bar, sections, resource, config_id)

class SimScholarStyling:
    def __init__(self, root, theme) -> None:
        self.root = root
        self.theme = theme
        self.root.tk.call("source", "main/assets/themes.tcl")
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
