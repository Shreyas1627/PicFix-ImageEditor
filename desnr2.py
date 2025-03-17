import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        self.mainlabel = tk.Label(self.root, text="Image Manipulator", font=("Arial", 24, "bold"), bg="blue", fg="white", width=90, anchor="w").pack(pady=20)

        self.introdetails = tk.Frame(self.root, bg="pink", width=600, height=400)
        tk.Label(self.introdetails, text="Please Enter The Following Details", font=("Arial", 10), bg="pink", fg="black").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self.introdetails, text="Name:", background="pink").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.introdetails).grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.introdetails, text="Phone Number:", background="pink").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.introdetails).grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.introdetails, text="Email:", background="pink").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.introdetails).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.introdetails, text="Proceed To Image Manipulator", bg="blue", fg="white", command=self.maininterface).grid(row=4, column=0, columnspan=2, pady=10)
        self.introdetails.place(relx=0.5, rely=0.5, anchor="center")
        
    def maininterface(self):
        self.introdetails.destroy()
        self.workingarea()

        self.sidepanel = tk.Frame(self.root, bg="grey68")
        self.sidepanel.place(relx=-0.3, rely=0.1, relwidth=0.2, relheight=0.9)
        self.sidepanel_startpos = -0.3
        self.sidepanel_endpos = 0
        self.sidepanel_pos = self.sidepanel_startpos
        self.sidepanel_in_startpos = True

        button_options = {
            "bg": "magenta3",
            "fg": "white",
            "font": ("Arial", 12),
            "width": 20,
            "relief": tk.GROOVE
        }

        tk.Button(self.sidepanel, text="Resize", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Rotate", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Crop", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Paste", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Transform", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Apply Filters", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Enhance", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Add Text", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Convert Mode", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Save Image", **button_options).pack(pady=15)
        tk.Button(self.sidepanel, text="Reset", **button_options).pack(pady=15)

        button = tk.Button(self.root, text="MENU", command=self.animate_sidepanel, background="grey26", fg="white")
        button.place(relx=0.03, rely=0.090, anchor="center", width=100, relheight=0.03)
        tk.Button(self.root, text="Open Image", command=self.openimage, bg="grey26", fg="white", font=("Arial", 12)).place(relx=0.15, rely=0.090, anchor="center", width=100, relheight=0.03)

    def animate_sidepanel(self):
        if self.sidepanel_in_startpos:
            self.animate_sidepanel_forward()
        else:
            self.animate_sidepanel_backwards()

    def animate_sidepanel_forward(self):
        if self.sidepanel_pos < self.sidepanel_endpos:
            self.sidepanel_pos += 0.008
            self.sidepanel.place(relx=self.sidepanel_pos, rely=0.1, relwidth=0.3, relheight=0.9)
            self.root.after(10, self.animate_sidepanel_forward)
        else:
            self.sidepanel_in_startpos = False

    def animate_sidepanel_backwards(self):
        if self.sidepanel_pos > self.sidepanel_startpos:
            self.sidepanel_pos -= 0.008
            self.sidepanel.place(relx=self.sidepanel_pos, rely=0.1, relwidth=0.3, relheight=0.9)
            self.root.after(10, self.animate_sidepanel_backwards)
        else:
            self.sidepanel_in_startpos = True

    
        

    def backround(self):
        self.backround = tk.Frame(self.root, bg="orange2")
        self.backround.place(relx=0, rely=0.1, relwidth=1.0, relheight=0.9)
    def openimage(self):
        self.filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not self.filename:
            return
        self.image = Image.open(self.filename)
        self.processed_image = self.image.copy()
        self.display_image()

    def display_image(self, preview=False):
        if preview:
            img_tk = ImageTk.PhotoImage(self.processed_image.resize((200, 200)))
            img_label = tk.Label(self.workingarea, image=img_tk, bg="#588BAE")
            img_label.image = img_tk
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
        else:
            img_tk = ImageTk.PhotoImage(self.processed_image)
            img_label = tk.Label(self.workingarea, image=img_tk, bg="#588BAE")
            img_label.image = img_tk
            img_label.pack(pady=10)

    def workingarea(self):
        self.workingarea = tk.Frame(self.root, bg="ivory2")
        self.workingarea.place(relx=0, rely=0.1, relwidth=1.0, relheight=0.9)




if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
