import tkinter as tk
import render
debug_open = False

def open_debug(root, sections):
    global debug_open, debug_sub_window
    if debug_open:
        debug_sub_window.destroy()
        debug_open=False
    else:
        debug_sub_window = debug_window(root, sections)
        debug_open=True

def debug_window(root, sections):
    # Create the main window
    debug = tk.Toplevel(root)
    debug.title("debug")
    debug.configure(background="gray")

    header_label = tk.Label(debug, text="EAGER Debugger", font=('TkDefaultFont', 16, 'bold'))
    header_label.grid(row=0, column=0, columnspan=3, pady=10)

    def select_frame(section, selection):
        global current_section
        current_section = section["main"]["title_obj"].cget("text")
        print(current_section)

    var = tk.StringVar()
    option = []
    for section_idx in range(len(sections)):
        sec_ttl = sections[section_idx]["main"]["title"]
        # Create selector buttons
        opt = tk.Radiobutton(debug, text=f"Frame {section_idx}: {sec_ttl}", 
                             variable=var, value=sections[section_idx], command=lambda value=sec_ttl: print(value))
        opt.grid(row=section_idx+2, column=0, padx=5, pady=5, columnspan=2)
        option.append(opt)

    # SHOW FRAME
    show_button = tk.Button(debug, text="Show Frame", command=lambda: render.hide_section(sections, current_section["main"]["title"]))
    show_button.grid(row=7, column=0, padx=20, pady=5, sticky=tk.E)

    # HIDE BUTTON
    hide_button = tk.Button(debug, text="Hide Frame", command=lambda: render.show_section(sections, current_section["main"]["title"]))
    hide_button.grid(row=7, column=1, padx=20, pady=5, sticky=tk.E)
    return debug