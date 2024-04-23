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
from tkinter import Toplevel, Canvas
from PIL import Image, ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def open_svg_popup(svg_path, root, scale=0.6):
    messagebox.showerror("Error", "No Stats file found!")
    # Convert SVG to an image
    drawing = svg2rlg(svg_path)
    image = renderPM.drawToPIL(drawing)

    # Scale the image if scale is not 1.0
    if scale != 1.0:
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Use a Toplevel widget to create a new window
    top = Toplevel(root)
    top.title("Configuration Diagram")

    # Create a canvas to hold the image
    canvas = Canvas(top, width=image.width, height=image.height)
    canvas.pack()

    # Convert the PIL image to a Tkinter PhotoImage using ImageTk
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=photo, anchor="nw")

    # Keep the reference of the photo (important to prevent garbage-collection)
    canvas.image = photo

# Example usage:
# root = tk.Tk()  # This would typically be created in your main application code
# open_svg_popup("path_to_your_svg_file.svg", root, scale=0.5)  # Scale to 50%
# root.mainloop()  # This starts the Tkinter event loop
