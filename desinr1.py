import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText    

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        self.root.geometry("800x600")

        self.mainlabel = tk.Label(self.root, text="Image Manipulator", font=("Arial", 24, "bold"), width=90, anchor="w")
        self.mainlabel.pack(pady=20)
        tk.Button(self.root, text="Theme", command=self.toggle_theme, bg="grey4",
                  fg="white",
                  font=("Arial", 12),
                  width=10,
                  relief=tk.GROOVE).place(relx=0.9, rely=0.03)

        tk.Button(self.root, text="Send Email",command=self.sendemail,bg="grey4",
                  fg="white",
                  font=("Arial", 12),
                  width=10,
                  relief=tk.GROOVE).place(relx=0.8, rely=0.03)


        self.introdetails = tk.Frame(self.root, bd=9, relief="ridge", width=7000, height=7000)
        tk.Label(self.introdetails, text="Please Enter The Following Details", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self.introdetails, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(self.introdetails)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.introdetails, text="Email:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.email_entryRE = tk.Entry(self.introdetails)
        self.email_entryRE.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self.introdetails, text="Proceed To Image Manipulator", command=self.menuinterface).grid(row=6, column=0, columnspan=2, pady=20)

        self.introdetails.place(relx=0.5, rely=0.5, anchor="center")

        self.dark_theme = True
        self.set_theme()

    def set_theme(self):
        if self.dark_theme:
            self.root.configure(bg="#282828")
            self.mainlabel.configure(bg="#E0E0E0", fg="grey3")
            self.introdetails.configure(bg="#202020")
            self.button_options = {
                "bg": "grey4",
                "fg": "white",
                "font": ("Arial", 12),
                "width": 20,
                "relief": tk.GROOVE
            }
        else:
            self.root.configure(bg="#FFFFFF")
            self.mainlabel.configure(bg="#000000", fg="#FFFFFF")
            self.introdetails.configure(bg="#F0F0F0")
            self.button_options = {
                "bg": "#DDDDDD",
                "fg": "black",
                "font": ("Arial", 12),
                "width": 20,
                "relief": tk.GROOVE
            }

    def toggle_theme(self):
        self.dark_theme = not self.dark_theme
        self.set_theme()

    def sendemail(self):
        try:
            ob = smtplib.SMTP("smtp.gmail.com", 587)
            ob.starttls()

            ob.login('ethanaoic@gmail.com', 'bmndngjntzgegemr')
            subject = "Image"
            body = "This is the image"
            message = "Subject:{}\n\n{}".format(subject, body)
            ob.sendmail('ethanaoic@gmail.com', self.email_entryRE.get(), message)
            messagebox.showinfo("Success", "Email has been sent")
            ob.quit()
        except Exception as e:
            messagebox.showinfo("Error", f"Email not sent: {e}")

    def menuinterface(self):
        self.introdetails.destroy()
        

        self.menuframe = tk.Frame(self.root)
        self.menuframe.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.9)
        tk.Button(self.menuframe, text="Resize", command=self.resize_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Rotate", command=self.rotate_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Crop", command=self.crop_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Paste", command=self.paste_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Transform", command=self.transform_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Apply Filters", command=self.apply_filters, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Enhance", command=self.enhance_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Add Text", command=self.add_text, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Convert Mode", command=self.convert_mode, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Save Image", command=self.save_image, **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Reset", command=self.reset_image, **self.button_options).pack(pady=15)
       
        # button = tk.Button(self.root, text="MENU", command=self.animate_sidepanel, background="grey26", fg="white")
        # button.place(relx=0.03, rely=0.090, anchor="center", width=100, relheight=0.03)
       

        self.canvas = tk.Canvas(self.root, bg="grey")
        self.canvas.place(relx=0.25, rely=0.1, relwidth=0.6, relheight=0.9)

        self.image = None
        self.image_path = None
        self.image_tk = None

        self.menuframe.bind("<Button-1>", self.load_image)

        self.sidepanel = tk.Frame(self.root, bg="grey68")
        self.sidepanel.place(relx=1.0, rely=0.1, relwidth=0.2, relheight=0.9)
        self.sidepanel_startpos = 1.0
        self.sidepanel_endpos = 0.86
        self.sidepanel_pos = self.sidepanel_startpos
        self.sidepanel_in_startpos = True

    def animate_sidepanel(self):

        if self.sidepanel_in_startpos:
            self.animate_sidepanel_forward()
        else:
            self.animate_sidepanel_backwards()

    def animate_sidepanel_forward(self):
            if self.sidepanel_pos > self.sidepanel_endpos:
                self.sidepanel_pos -= 0.008
                self.sidepanel.place(relx=self.sidepanel_pos, rely=0.1, relwidth=0.2, relheight=0.9)
                self.root.after(10, self.animate_sidepanel_forward)
            else:
                self.sidepanel_in_startpos = False

    def animate_sidepanel_backwards(self):
                
            if self.sidepanel_pos < self.sidepanel_startpos:
                self.sidepanel_pos += 0.008
                self.sidepanel.place(relx=self.sidepanel_pos, rely=0.1, relwidth=0.2, relheight=0.9)
                self.root.after(10, self.animate_sidepanel_backwards)
            else:
                self.sidepanel_in_startpos = True
        
    def load_image(self, event):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = Image.open(self.image_path)
            self.image.thumbnail((800, 600))
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.image_tk, anchor="nw")

        self.menuframe.unbind("<Button-1>")

    def resize_image(self):
        self.animate_sidepanel()
    
    

    def rotate_image(self):
        self.animate_sidepanel()
        

    def crop_image(self):
        pass

    def paste_image(self):
        pass

    def transform_image(self):
        pass

    def apply_filters(self):
        pass

    def enhance_image(self):
        pass

    def add_text(self):
        pass

    def convert_mode(self):
        pass

    def save_image(self):
        pass

    def reset_image(self):
        pass


    

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
