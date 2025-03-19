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
                  relief=tk.GROOVE).place(relx=0.9, rely=0.1)
        
        tk.Button(self.root, text="Send Email",command=self.sendemail,bg="grey4",
                  fg="white",
                  font=("Arial", 12),
                  width=10,
                  relief=tk.GROOVE).place(relx=0.8, rely=0.2)
        



        self.introdetails = tk.Frame(self.root, bd=9, relief="ridge", width=700, height=700)
        tk.Label(self.introdetails, text="Please Enter The Following Details", font=("Arial", 10)).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(self.introdetails, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.name_entry = tk.Entry(self.introdetails)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.introdetails, text="Phone Number:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.phone_entry = tk.Entry(self.introdetails)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.introdetails, text="Email:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = tk.Entry(self.introdetails)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.introdetails, text="Password:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(self.introdetails)
        self.password_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.introdetails, text="Receiver Email:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
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

            ob.login(self.email_entry.get(), self.password_entry.get())
            subject = "Image"
            body = "This is the image"
            message = "Subject:{}\n\n{}".format(subject, body)
            ob.sendmail(self.email_entry.get(), self.email_entryRE.get(), message)
            messagebox.showinfo("Success", "Email has been sent")
            ob.quit()
        except Exception as e:
            messagebox.showinfo("Error", f"Email not sent: {e}")

    def menuinterface(self):
        self.introdetails.destroy()

        self.menuframe = tk.Frame(self.root)
        self.menuframe.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.9)

        tk.Button(self.menuframe, text="Resize", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Rotate", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Crop", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Paste", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Transform", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Apply Filters", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Enhance", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Add Text", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Convert Mode", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Save Image", **self.button_options).pack(pady=15)
        tk.Button(self.menuframe, text="Reset", **self.button_options).pack(pady=15)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()