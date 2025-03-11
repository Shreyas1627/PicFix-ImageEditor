import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageDraw, ImageOps, ImageChops, ImageFont

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Image Editor")
        self.root.geometry("800x600")
        self.root.configure(bg="#588BAE")

        self.image = None
        self.processed_image = None
        self.filename = None

        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Welcome", font=("Arial", 24, "bold"), bg="#588BAE", fg="white").pack(pady=20)
        tk.Label(self.root, text="(This is the project of Muthusam, Shreyas, Nissim)", font=("Arial", 10), bg="#588BAE", fg="white").pack(pady=5)
        tk.Button(self.root, text="Add Image from File/Device", command=self.open_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=20)

    def create_main_interface(self):
        self.clear_window()
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
        self.filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not self.filename:
            return
        self.image = Image.open(self.filename)
        self.processed_image = self.image.copy()
        self.create_main_interface()

    def display_image(self, preview=False):
        if preview:
            img_tk = ImageTk.PhotoImage(self.processed_image.resize((200, 200)))
            img_label = tk.Label(self.root, image=img_tk, bg="#588BAE")
            img_label.image = img_tk
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
        else:
            self.clear_window()
            img_tk = ImageTk.PhotoImage(self.processed_image)
            img_label = tk.Label(self.root, image=img_tk, bg="#588BAE")
            img_label.image = img_tk
            img_label.pack(pady=10)
        tk.Button(self.root, text="Back to Features", command=self.create_main_interface, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

    def resize_options(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.clear_window()
        tk.Label(self.root, text="Choose Resize Option:", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="3:4", command=lambda: self.resize_image(3, 4), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="4:3", command=lambda: self.resize_image(4, 3), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="16:9", command=lambda: self.resize_image(16, 9), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="9:16", command=lambda: self.resize_image(9, 16), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Custom", command=self.custom_resize, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)

    def resize_image(self, width_ratio, height_ratio):
        width, height = self.processed_image.size
        new_width = int(width * (width_ratio / height_ratio))
        new_height = int(height * (height_ratio / width_ratio))
        self.processed_image = self.processed_image.resize((new_width, new_height))
        self.display_image()

    def custom_resize(self):
        width = simpledialog.askinteger("Resize", "Enter width:")
        height = simpledialog.askinteger("Resize", "Enter height:")
        if width is None or height is None:
            return
        self.processed_image = self.processed_image.resize((width, height))
        self.display_image()

    def rotate_options(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.clear_window()
        tk.Label(self.root, text="Rotate Image", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Label(self.root, text="Enter Rotation Angle:", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=5)
        self.rotate_angle = tk.Entry(self.root, width=10)
        self.rotate_angle.pack(pady=5)
        tk.Button(self.root, text="Preview", command=self.preview_rotate, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Save Rotated Image", command=self.save_image, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)

    def preview_rotate(self):
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

    def crop_options(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.clear_window()
        tk.Label(self.root, text="Choose Crop Option:", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Custom Crop", command=self.custom_crop, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)

    def custom_crop(self):
        left = simpledialog.askinteger("Crop", "Enter left:")
        top = simpledialog.askinteger("Crop", "Enter top:")
        right = simpledialog.askinteger("Crop", "Enter right:")
        bottom = simpledialog.askinteger("Crop", "Enter bottom:")
        if None in [left, top, right, bottom]:
            return
        self.processed_image = self.processed_image.crop((left, top, right, bottom))
        self.display_image()

    def paste_image(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        paste_filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not paste_filename:
            return
        paste_image = Image.open(paste_filename)
        position = simpledialog.askstring("Paste", "Enter position (x,y):")
        if position is None:
            return
        x, y = map(int, position.split(','))
        self.processed_image.paste(paste_image, (x, y))
        self.display_image()

    def transform_image(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.processed_image = self.processed_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.display_image()

    def filter_options(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.clear_window()
        tk.Label(self.root, text="Choose Filter:", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Blur", command=lambda: self.apply_filter(ImageFilter.GaussianBlur(radius=5)), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Sharpen", command=lambda: self.apply_filter(ImageFilter.SHARPEN), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Edge Enhance", command=lambda: self.apply_filter(ImageFilter.EDGE_ENHANCE), bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=5)

    def apply_filter(self, filter):
        self.processed_image = self.processed_image.filter(filter)
        self.display_image()

    def enhance_options(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.clear_window()
        adjustment_frame = tk.Frame(self.root, bg="#588BAE")
        adjustment_frame.pack(side=tk.LEFT, padx=20, pady=20)
        self.display_image(preview=True)
        tk.Label(adjustment_frame, text="Brightness", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=5)
        self.brightness_scale = tk.Scale(adjustment_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.enhance_brightness, bg="#588BAE", fg="white", font=("Arial", 12))
        self.brightness_scale.set(1.0)
        self.brightness_scale.pack(pady=5)
        tk.Label(adjustment_frame, text="Contrast", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=5)
        self.contrast_scale = tk.Scale(adjustment_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.enhance_contrast, bg="#588BAE", fg="white", font=("Arial", 12))
        self.contrast_scale.set(1.0)
        self.contrast_scale.pack(pady=5)
        tk.Label(adjustment_frame, text="Sharpness", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=5)
        self.sharpness_scale = tk.Scale(adjustment_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.enhance_sharpness, bg="#588BAE", fg="white", font=("Arial", 12))
        self.sharpness_scale.set(1.0)
        self.sharpness_scale.pack(pady=5)
        tk.Label(adjustment_frame, text="Color", bg="#588BAE", fg="white", font=("Arial", 12)).pack(pady=5)
        self.color_scale = tk.Scale(adjustment_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.enhance_color, bg="#588BAE", fg="white", font=("Arial", 12))
        self.color_scale.set(1.0)
        self.color_scale.pack(pady=5)

    def enhance_brightness(self, value):
        enhancer = ImageEnhance.Brightness(self.processed_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image(preview=True)

    def enhance_contrast(self, value):
        enhancer = ImageEnhance.Contrast(self.processed_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image(preview=True)

    def enhance_sharpness(self, value):
        enhancer = ImageEnhance.Sharpness(self.processed_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image(preview=True)

    def enhance_color(self, value):
        enhancer = ImageEnhance.Color(self.processed_image)
        self.processed_image = enhancer.enhance(float(value))
        self.display_image(preview=True)

    def add_text(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        text = simpledialog.askstring("Add Text", "Enter text:")
        if text is None:
            return
        draw = ImageDraw.Draw(self.processed_image)
        font = ImageFont.load_default()
        draw.text((10, 10), text, fill="white", font=font)
        self.display_image()

    def convert_mode(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return
        mode = simpledialog.askstring("Convert Mode", "Enter mode (e.g., 'L', 'RGB', 'CMYK'):")
        if mode is None:
            return
        self.processed_image = self.processed_image.convert(mode)
        self.display_image()

    def save_image(self):
        if not self.processed_image:
            messagebox.showerror("Error", "No image to save!")
            return
        save_filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
        if save_filename:
            self.processed_image.save(save_filename)
            messagebox.showinfo("Success", "Image saved successfully!")

    def reset_image(self):
        if self.image:
            self.processed_image = self.image.copy()
            self.display_image()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
