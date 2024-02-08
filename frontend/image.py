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
from PIL import Image, ImageTk
import os

cwd = os.getcwd()
image_path = f"{cwd}/frontend/img/"

def render_image(canvas, file, xoffset, yoffset, scale):
    
    path = f"{image_path}{file}"
    original_image = Image.open(path)

    width, height = original_image.size
    resized_image = original_image.resize((int(width * scale), int(height * scale)), Image.ANTIALIAS)
    xpos = ((canvas.winfo_reqwidth() - width * scale) /2) + xoffset
    ypos = ((canvas.winfo_reqheight() - height * scale) /2) + yoffset

    photo = ImageTk.PhotoImage(resized_image)
    canvas.create_image(xpos, ypos, anchor=tk.NW, image=photo)
    canvas.image = photo