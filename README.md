import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageOps, ImageChops, ImageFont

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="#588BAE")  # Set background color to blue

        # Variables
        self.image = None
        self.processed_image = None
        self.filename = None

        # Main Interface
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Create the welcome screen with a welcome message and a button to add an image."""
        self.clear_window()

        # Welcome message
        tk.Label(self.root, text="Welcome", font=("Arial", 24, "bold"), bg="#588BAE", fg="white").pack(pady=20)
        tk.Label(self.root, text="(This is the project of Muthusam, Shreyas, Nissim)", font=("Arial", 10), bg="#588BAE", fg="white").pack(pady=5)

        # Button to add an image
        tk.Button(self.root, text="Add Image from File/Device", command=self.open_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

    def create_main_interface(self):
        """Create the main interface with buttons for various image editing options."""
        self.clear_window()

        # Buttons for image editing options
        tk.Button(self.root, text="Resize", command=self.resize_options, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Rotate", command=self.rotate_options, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Crop", command=self.crop_options, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Paste", command=self.paste_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Transform", command=self.transform_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Apply Filters", command=self.filter_options, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Enhance", command=self.enhance_options, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Add Text", command=self.add_text, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Convert Mode", command=self.convert_mode, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Save Image", command=self.save_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Reset", command=self.reset_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

    def open_image(self):
        """Open an image from the user's device."""
        self.filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not self.filename:
            return
        
        self.image = Image.open(self.filename)
        self.processed_image = self.image.copy()
        self.create_main_interface()

    def display_image(self, preview=False):
        """Display the image in the Tkinter window."""
        if preview:
            img_tk = ImageTk.PhotoImage(self.processed_image.resize((200, 200)))
            img_label = tk.Label(self.root, image=img_tk, bg="#588BAE")
            img_label.image = img_tk  # Keep a reference
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
        else:
            self.clear_window()
            img_tk = ImageTk.PhotoImage(self.processed_image)
            img_label = tk.Label(self.root, image=img_tk, bg="#588BAE")
            img_label.image = img_tk  # Keep a reference
            img_label.pack(pady=10)
        
        tk.Button(self.root, text="Back to Features", command=self.create_main_interface, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

    def rotate_options(self):
        """Provide options for rotating the image."""
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return

        self.clear_window()
        tk.Label(self.root, text="Rotate Image", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=10)

        # Input for rotation angle
        tk.Label(self.root, text="Enter Rotation Angle:", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=5)
        self.rotate_angle = tk.Entry(self.root, width=10)
        self.rotate_angle.pack(pady=5)

        # Preview and Save buttons
        tk.Button(self.root, text="Preview", command=self.preview_rotate, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Save Rotated Image", command=self.save_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)

    def preview_rotate(self):
        """Preview the rotated image."""
        angle = self.rotate_angle.get()
        if not angle:
            messagebox.showerror("Error", "Please enter a rotation angle!")
            return
        
        try:
            angle = int(angle)
        except ValueError:
            messagebox.showerror("Error", "Invalid angle! Please enter a number.")
            return
        
        self.processed_image = self.image.copy().rotate(angle)
        self.display_image(preview=True)

    def save_image(self):
        """Save the processed image."""
        if not self.processed_image:
            messagebox.showerror("Error", "No image to save!")
            return

        save_filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
        if save_filename:
            self.processed_image.save(save_filename)
            messagebox.showinfo("Success", "Image saved successfully!")

    def reset_image(self):
        """Reset the image to the original."""
        if self.image:
            self.processed_image = self.image.copy()
            self.display_image()

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # Placeholder functions for other buttons (non-functional)
    def resize_options(self):
        messagebox.showinfo("Info", "Resize feature is not implemented yet.")

    def crop_options(self):
        messagebox.showinfo("Info", "Crop feature is not implemented yet.")

    def paste_image(self):
        messagebox.showinfo("Info", "Paste feature is not implemented yet.")

    def transform_image(self):
        messagebox.showinfo("Info", "Transform feature is not implemented yet.")

    def filter_options(self):
        messagebox.showinfo("Info", "Filter feature is not implemented yet.")

    def enhance_options(self):
        messagebox.showinfo("Info", "Enhance feature is not implemented yet.")

    def add_text(self):
        messagebox.showinfo("Info", "Add Text feature is not implemented yet.")

    def convert_mode(self):
        messagebox.showinfo("Info", "Convert Mode feature is not implemented yet.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()


