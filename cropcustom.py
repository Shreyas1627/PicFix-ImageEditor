import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")

        self.image = None
        self.tk_image = None
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.handles = []
        self.start_x = None
        self.start_y = None
        self.active_handle = None

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.crop_button = tk.Button(root, text="Crop", command=self.crop_image)
        self.crop_button.pack()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
            self.create_crop_rectangle()

    def create_crop_rectangle(self):
        if self.image:
            width, height = self.image.size
            self.rect = self.canvas.create_rectangle(width // 4, height // 4, 3 * width // 4, 3 * height // 4, outline="red")
            self.create_handles()

    def create_handles(self):
        if self.rect:
            coords = self.canvas.coords(self.rect)
            handle_size = 5

            self.handles = []
            # Corners
            self.handles.append(self.canvas.create_rectangle(coords[0] - handle_size, coords[1] - handle_size, coords[0] + handle_size, coords[1] + handle_size, fill="blue"))
            self.handles.append(self.canvas.create_rectangle(coords[2] - handle_size, coords[1] - handle_size, coords[2] + handle_size, coords[1] + handle_size, fill="blue"))
            self.handles.append(self.canvas.create_rectangle(coords[2] - handle_size, coords[3] - handle_size, coords[2] + handle_size, coords[3] + handle_size, fill="blue"))
            self.handles.append(self.canvas.create_rectangle(coords[0] - handle_size, coords[3] - handle_size, coords[0] + handle_size, coords[3] + handle_size, fill="blue"))

            # Midpoints
            self.handles.append(self.canvas.create_rectangle((coords[0] + coords[2]) / 2 - handle_size, coords[1] - handle_size, (coords[0] + coords[2]) / 2 + handle_size, coords[1] + handle_size, fill="blue"))
            self.handles.append(self.canvas.create_rectangle(coords[2] - handle_size, (coords[1] + coords[3]) / 2 - handle_size, coords[2] + handle_size, (coords[1] + coords[3]) / 2 + handle_size, fill="blue"))
            self.handles.append(self.canvas.create_rectangle((coords[0] + coords[2]) / 2 - handle_size, coords[3] - handle_size, (coords[0] + coords[2]) / 2 + handle_size, coords[3] + handle_size, fill="blue"))
            self.handles.append(self.canvas.create_rectangle(coords[0] - handle_size, (coords[1] + coords[3]) / 2 - handle_size, coords[0] + handle_size, (coords[1] + coords[3]) / 2 + handle_size, fill="blue"))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        for i, handle in enumerate(self.handles):
            coords = self.canvas.coords(handle)
            if coords[0] <= event.x <= coords[2] and coords[1] <= event.y <= coords[3]:
                self.active_handle = i
                return

        rect_coords = self.canvas.coords(self.rect)
        if rect_coords[0] <= event.x <= rect_coords[2] and rect_coords[1] <= event.y <= rect_coords[3]:
            self.active_handle = "rect"

    def on_motion(self, event):
        if self.active_handle is not None:
            if self.active_handle == "rect":
                dx = event.x - self.start_x
                dy = event.y - self.start_y
                self.canvas.move(self.rect, dx, dy)
                for handle in self.handles:
                    self.canvas.move(handle, dx, dy)
                self.start_x = event.x
                self.start_y = event.y
            else:
                coords = self.canvas.coords(self.rect)
                handle_size = 5
                new_coords = list(coords)

                if self.active_handle in [0, 1, 2, 3]: #corners
                    if self.active_handle in [0, 3]: new_coords[0] = event.x
                    if self.active_handle in [1, 2]: new_coords[2] = event.x
                    if self.active_handle in [0, 1]: new_coords[1] = event.y
                    if self.active_handle in [2, 3]: new_coords[3] = event.y
                else: #midpoints
                    if self.active_handle == 4: new_coords[1] = event.y
                    if self.active_handle == 5: new_coords[2] = event.x
                    if self.active_handle == 6: new_coords[3] = event.y
                    if self.active_handle == 7: new_coords[0] = event.x

                self.canvas.coords(self.rect, new_coords)
                self.canvas.delete(*self.handles)
                self.create_handles()

    def on_button_release(self, event):
        self.active_handle = None

    def crop_image(self):
        if self.image and self.rect:
            coords = self.canvas.coords(self.rect)
            left = int(coords[0])
            top = int(coords[1])
            right = int(coords[2])
            bottom = int(coords[3])

            cropped_image = self.image.crop((left, top, right, bottom))
            self.image = cropped_image
            self.tk_image = ImageTk.PhotoImage(cropped_image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
            self.create_crop_rectangle()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCropper(root)
    root.mainloop()
