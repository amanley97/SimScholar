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