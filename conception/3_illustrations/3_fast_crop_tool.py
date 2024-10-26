import os
from PIL import Image, ImageTk
from PIL.Image import Resampling
import tkinter as tk
from tkinter import messagebox

# Directory where your friend images are stored
IMAGE_DIR = './friend_images'
OUTPUT_DIR = './cropped_images'

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

class ImageCropper(tk.Tk):
    def __init__(self, image_list):
        super().__init__()

        self.image_list = image_list
        self.image_index = 0

        # Initialize window
        self.title("Friend Image Cropper")

        # Get screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Initialize canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Instructions
        instructions = tk.Label(self, text="Drag to move, Shift+Drag to resize, or use the buttons below")
        instructions.pack()

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side="bottom", fill="x")

        # Movement buttons
        move_frame = tk.Frame(button_frame)
        move_frame.pack(side="left")

        tk.Button(move_frame, text="↑", command=self.move_up).grid(row=0, column=1)
        tk.Button(move_frame, text="←", command=self.move_left).grid(row=1, column=0)
        tk.Button(move_frame, text="→", command=self.move_right).grid(row=1, column=2)
        tk.Button(move_frame, text="↓", command=self.move_down).grid(row=1, column=1)

        # Resize buttons
        resize_frame = tk.Frame(button_frame)
        resize_frame.pack(side="left", padx=20)

        tk.Button(resize_frame, text="+", command=self.increase_size).pack()
        tk.Button(resize_frame, text="-", command=self.decrease_size).pack()

        # Next button
        self.next_button = tk.Button(button_frame, text="Next", command=self.save_and_next)
        self.next_button.pack(side="right")

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.perform_drag)
        self.canvas.bind("<Shift-ButtonPress-1>", self.start_scale)
        self.canvas.bind("<Shift-B1-Motion>", self.perform_scale)
        self.canvas.bind("<ButtonRelease-1>", self.end_action)

        # Initialize the rectangle and square properties
        self.rect = None
        self.dragging = False
        self.scaling = False
        self.square_size = 0
        self.square_x = 0
        self.square_y = 0
        self.scaling_factor = 1.0

        # Load the first image
        self.load_image()

    def load_image(self):
        """Loads the current image from the list and resizes it if necessary."""
        image_path = self.image_list[self.image_index]
        self.original_image = Image.open(image_path)
        img_width, img_height = self.original_image.size

        # Calculate scaling factor to fit image within screen size
        max_width = self.screen_width - 100
        max_height = self.screen_height - 200

        scaling_factor = min(max_width / img_width, max_height / img_height, 1)
        self.scaling_factor = scaling_factor

        display_width = int(img_width * scaling_factor)
        display_height = int(img_height * scaling_factor)

        self.display_image = self.original_image.resize(
            (display_width, display_height), Resampling.LANCZOS
        )

        # Adjust the canvas and window size to match the display image size
        self.canvas.config(width=display_width, height=display_height)
        self.geometry(f"{display_width}x{display_height+150}")  # Extra space for instructions and buttons

        self.update_canvas()

        # Initialize the square
        self.init_square()

    def update_canvas(self):
        """Updates the canvas with the current image."""
        self.tk_image = ImageTk.PhotoImage(self.display_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        self.draw_square()

    def init_square(self):
        """Initialize the square to be the largest possible square that fits in the image."""
        img_width, img_height = self.original_image.size
        square_size = min(img_width, img_height) * 0.5  # Start with half the size
        self.square_size = square_size

        # Center the square
        self.square_x = (img_width - square_size) / 2
        self.square_y = (img_height - square_size) / 2

    def draw_square(self):
        """Draw the square on the canvas."""
        self.canvas.delete("selection")

        # Map original image coordinates to display coordinates
        x0 = int(self.square_x * self.scaling_factor)
        y0 = int(self.square_y * self.scaling_factor)
        x1 = int((self.square_x + self.square_size) * self.scaling_factor)
        y1 = int((self.square_y + self.square_size) * self.scaling_factor)

        # Ensure coordinates are within canvas bounds
        x0 = max(0, min(x0, self.canvas.winfo_width()))
        y0 = max(0, min(y0, self.canvas.winfo_height()))
        x1 = max(0, min(x1, self.canvas.winfo_width()))
        y1 = max(0, min(y1, self.canvas.winfo_height()))

        self.rect = self.canvas.create_rectangle(
            x0, y0, x1, y1,
            outline="red", width=2, fill='', tags="selection"
        )

    def start_drag(self, event):
        """Handles mouse press to start dragging."""
        self.start_x = event.x / self.scaling_factor
        self.start_y = event.y / self.scaling_factor
        self.dragging = True

    def perform_drag(self, event):
        """Handles dragging the selection square."""
        if self.dragging:
            current_x = event.x / self.scaling_factor
            current_y = event.y / self.scaling_factor
            dx = current_x - self.start_x
            dy = current_y - self.start_y

            self.square_x += dx
            self.square_y += dy

            # Ensure square stays within image boundaries
            self.square_x = max(0, min(self.square_x, self.original_image.width - self.square_size))
            self.square_y = max(0, min(self.square_y, self.original_image.height - self.square_size))

            self.start_x, self.start_y = current_x, current_y
            self.draw_square()

    def start_scale(self, event):
        """Handles mouse press to start scaling."""
        self.start_y = event.y / self.scaling_factor
        self.scaling = True

    def perform_scale(self, event):
        """Handles scaling the selection square."""
        if self.scaling:
            current_y = event.y / self.scaling_factor
            delta = current_y - self.start_y
            new_size = self.square_size + delta

            if new_size > 10 and new_size <= min(self.original_image.width, self.original_image.height):
                self.square_x -= delta / 2
                self.square_y -= delta / 2
                self.square_size = new_size

                # Ensure square stays within image boundaries
                self.square_x = max(0, min(self.square_x, self.original_image.width - self.square_size))
                self.square_y = max(0, min(self.square_y, self.original_image.height - self.square_size))

            self.start_y = current_y
            self.draw_square()

    def end_action(self, event):
        """Ends dragging or scaling when mouse button is released."""
        self.dragging = False
        self.scaling = False

    def move_left(self):
        """Moves the selection square left."""
        self.square_x = max(0, self.square_x - 10)
        self.draw_square()

    def move_right(self):
        """Moves the selection square right."""
        self.square_x = min(self.original_image.width - self.square_size, self.square_x + 10)
        self.draw_square()

    def move_up(self):
        """Moves the selection square up."""
        self.square_y = max(0, self.square_y - 10)
        self.draw_square()

    def move_down(self):
        """Moves the selection square down."""
        self.square_y = min(self.original_image.height - self.square_size, self.square_y + 10)
        self.draw_square()

    def increase_size(self):
        """Increases the size of the selection square."""
        delta = 10
        new_size = self.square_size + delta

        if new_size <= min(self.original_image.width, self.original_image.height):
            self.square_x -= delta / 2
            self.square_y -= delta / 2
            self.square_size = new_size

            # Ensure square stays within image boundaries
            self.square_x = max(0, min(self.square_x, self.original_image.width - self.square_size))
            self.square_y = max(0, min(self.square_y, self.original_image.height - self.square_size))

            self.draw_square()

    def decrease_size(self):
        """Decreases the size of the selection square."""
        delta = 10
        new_size = self.square_size - delta

        if new_size >= 10:
            self.square_x += delta / 2
            self.square_y += delta / 2
            self.square_size = new_size

            # Ensure square stays within image boundaries
            self.square_x = max(0, min(self.square_x, self.original_image.width - self.square_size))
            self.square_y = max(0, min(self.square_y, self.original_image.height - self.square_size))

            self.draw_square()

    def save_and_next(self):
        """Crops, saves the current image, and loads the next one."""
        if self.rect:
            cropped_image = self.original_image.crop((
                int(self.square_x), int(self.square_y),
                int(self.square_x + self.square_size),
                int(self.square_y + self.square_size)
            ))
            # Resize the cropped image to a square
            square_image = cropped_image.resize((800, 800), Resampling.LANCZOS)
            save_path = os.path.join(OUTPUT_DIR, os.path.basename(self.image_list[self.image_index]))
            square_image.save(save_path)
            messagebox.showinfo("Saved", f"Saved cropped image as {save_path}")
        else:
            messagebox.showwarning("No Selection", "No cropping area was selected, skipping image.")
        
        # Move to next image
        self.image_index += 1
        if self.image_index < len(self.image_list):
            self.load_image()
        else:
            messagebox.showinfo("Done", "All images processed!")
            self.destroy()

def main():
    # Get all images in the directory
    image_list = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    if not image_list:
        messagebox.showerror("Error", "No images found in the directory.")
        return
    
    app = ImageCropper(image_list)
    app.mainloop()

if __name__ == "__main__":
    main()
