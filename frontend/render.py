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
from tkinter import ttk

def render_frame(master, row_offset):
    section_frame = tk.Frame(master, highlightthickness=0, relief=tk.RIDGE)
    section_frame.grid(row=row_offset*2 + 1, column=0, padx=10, pady=5, sticky=tk.W)
    return section_frame

def render_label(master, text, row, column, font_size, wraplen=None):
    label = tk.Label(master, 
                     text=text, 
                     font=('TkDefaultFont', font_size, 'normal'), 
                     wraplength=wraplen)
    label.grid(row=row, column=column, padx=5, pady=5, sticky=tk.W)
    return label

def render_dropdown(master, values):
    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(master, textvariable=dropdown_var, values=values)
    dropdown.grid(row=0, column=1, padx=5, pady=5)
    return dropdown, dropdown_var

def render_subopts(master, sub_option, row):
    sub_option_label = render_label(master, sub_option, row+2, 0, 10)

    textbox_var = tk.StringVar()
    textbox = tk.Entry(master, textvariable=textbox_var)
    textbox.grid(row=row + 2, column=1, padx=5, pady=5)
    return sub_option_label, textbox, textbox_var

def render_section(master, row_offset, title, opts, func, subopts):
    # Create a section frame
    section_frame = render_frame(master=master, row_offset=row_offset)

    # Add section title to the frame
    title_label = render_label(section_frame, title, row=0, column=0, font_size=12)

    # Create a dropdown menu
    dropdown, dropdown_value = render_dropdown(section_frame, opts)
    
    # Create a label to display the selected option
    selected_option_label = render_label(section_frame, "", row=0, column=1, font_size=10)

    section_frame_info=dict(frame_obj=section_frame, 
                            frame_row=section_frame.grid_info()["row"], 
                            frame_column=section_frame.grid_info()["column"]
                            )
    section_type_info=dict(title=str(title_label.cget("text")),
                           title_obj=title_label,
                           title_row=title_label.grid_info()["row"],
                           title_column=title_label.grid_info()["column"],
                           dropdown_obj=dropdown, 
                           dropdown_row=dropdown.grid_info()["row"], 
                           dropdown_column=dropdown.grid_info()["column"], 
                           dropdown_value=dropdown_value.get(),
                           selection_label=selected_option_label.cget("text"),
                           selection_obj=selected_option_label,
                           selection_row=selected_option_label.grid_info()["row"], 
                           selection_column=selected_option_label.grid_info()["column"]
                           )
    section_info = dict(frame=section_frame_info,
                        main=section_type_info,
                        )
    
    # Create textboxes for sub-options
    if subopts != None:
        for j, sub_option in enumerate(subopts):
            label, textbox, textbox_value = render_subopts(section_frame, sub_option, j)
            section_subopt_info = dict(option=str(label.cget("text")),
                                    option_obj=label,
                                    option_row=label.grid_info()["row"],
                                    option_column=label.grid_info()["column"],
                                    textbox_obj=textbox, 
                                    textbox_row=textbox.grid_info()["row"], 
                                    textbox_column=textbox.grid_info()["column"], 
                                    textbox_value=textbox_value.get()
                                    )
            section_info.update({f"suboption {j}" : section_subopt_info})
    
    if func != None:
        dropdown.bind("<<ComboboxSelected>>", lambda event,selected=dropdown_value, section_info=section_info: func(section_info, selected.get()))

    return section_info

def hide_section(section, section_list):
    for frame_idx in range(len(section_list)):
        if section_list[frame_idx]["main"]["title"] == section:
            section_to_hide = section_list[frame_idx]["frame"]["frame_obj"]
            section_to_hide.grid_remove()
            print(f"section {section} found")
            break
        else:
            section_to_hide = None
    if section_to_hide == None:
        print(f"section {section} not found!")
    else:
        print(f"section {section} hidden.")

def show_section(section, section_list):
    for frame_idx in range(len(section_list)):
        if section_list[frame_idx]["main"]["title"] == section:
            section_to_show = section_list[frame_idx]["frame"]["frame_obj"]
            print(f"section {section} found")
            section_to_show.grid()
            break
        else:
            section_to_show = None
    if section_to_show == None:
        print(f"section {section} not found!")
    else:
        print(f"section {section} shown.")

    # def show_section(section, done):
    #     # Set weight for the selected section, making it larger
    #     selected_index = list(section_menu.keys()).index(section) if not done else len(section_menu) + 1
    #     for i in range(len(section_menu)):
    #         weight = 1 if i == selected_index else 0
    #         root.grid_rowconfigure(i*2 + 1, weight=weight)

    #         # Show or hide the dropdown based on the selected section
    #         if i == selected_index:
    #             # section_frames[i].grid(row=2, column=0, padx=5, pady=5)
    #             section_dropdowns[i].grid(row=0, column=1, padx=5, pady=5)
    #             selected_option_labels[i].grid_remove()
    #             highlight_color = "black"
    #         else:
    #             # section_frames[i].grid_remove()
    #             section_dropdowns[i].grid_remove()
    #             selected_option_labels[i].grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    #             selected_option_labels[i].config(text=f"       {section_selected_options[i].get()}")
    #             highlight_color = root.cget("bg")
            
    #         section_frames[i].config(highlightthickness=weight*2, highlightbackground=highlight_color)                    

    #     # Set the current selected section
    #     current_selected_section.set(section)

    # # Function to advance to the next section
    # def advance_section(reset):
    #     current_index = list(section_menu.keys()).index(current_selected_section.get())
    #     index_count = 0 if reset else current_index + 1

    #     # Save the selected option for the current section
    #     section_selected_options[current_index].set(section_dropdowns[current_index].get())
    #     # Advance to the next section
    #     next_index = (current_index + 1) % len(section_menu)
    #     if index_count == len(section_menu):
    #         show_section(list(section_menu.keys())[current_index], True)
    #         edit_button.grid(row=len(section_menu)*2 + 1, column=0, padx=10, pady=5, sticky=tk.W)
    #         calls.print_selected(section_selected_options, section_menu)
    #     else:
    #         show_section(list(section_menu.keys())[next_index], False)