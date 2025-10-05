# This code is generated using PyUIbuilder: https://pyuibuilder.com
import os
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from pyuiWidgets.imageLabel import ImageLabel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

main = tk.Tk()
main.title("Master Of Style")
main.config(bg="#ffffff")
main.geometry("700x370")


style = ttk.Style(main)
style.theme_use("clam")

menu = tk.Menu(main)
main.config(menu=menu)
menu_0 = tk.Menu(menu, tearoff=0)
menu_0.add_command(label="Administrador", command=lambda: print("Administrador clicked"))
menu_0.add_command(label="Salir", command=lambda: print("Salir clicked"))
menu.add_cascade(label="Opciones", menu=menu_0)

style.configure("button.TButton", background="#000000", foreground="#ffffff")
style.map("button.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

button = ttk.Button(master=main, text="CONSULTAR PRODUCTOS", style="button.TButton")
button.place(x=56, y=114, width=175, height=48)

style.configure("button1.TButton", background="#000000", foreground="#ffffff")
style.map("button1.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

button1 = ttk.Button(master=main, text="CONSULTAR CITAS", style="button1.TButton")
button1.place(x=55, y=40, width=175, height=48)

style.configure("button2.TButton", background="#000000", foreground="#ffffff")
style.map("button2.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

button2 = ttk.Button(master=main, text="SERVICIOS", style="button2.TButton")
button2.place(x=56, y=255, width=175, height=48)

style.configure("button3.TButton", background="#000000", foreground="#ffffff")
style.map("button3.TButton", background=[("active", "#E4E2E2")], foreground=[("active", "#000")])

button3 = ttk.Button(master=main, text="VENDER", style="button3.TButton")
button3.place(x=54, y=182, width=175, height=48)

style.configure("label.TLabel", background="#E4E2E2", foreground="#000", anchor="center")
label = ImageLabel(master=main, image_path=os.path.join(BASE_DIR, "assets", "images", "470003012_122127259964547018_3132964216531262546_n.jpg"), text="Label", compound=tk.TOP, mode="cover")
label.configure(anchor="center")
label.place(x=279, y=15, width=403, height=319)


main.mainloop()