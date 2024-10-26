import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

# Directory where your fruit images are stored
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
        self.title("Fruit Image Cropper")
        self.geometry("800x800")
        
        self.canvas = tk.Canvas(self, width=800, height=800)
        self.canvas.pack(fill="both", expand=True)
        
        self.load_image()
        
        # Instructions
        instructions = tk.Label(self, text="Drag to move, Shift+Drag to resize, press 'Next' to save and continue")
        instructions.pack()
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(side="bottom", fill="x")
        
        self.next_button = tk.Button(button_frame, text="Next", command=self.save_and_next)
        self.next_button.pack(side="right")

        # Bind mouse events
        self.bind("<ButtonPress-1>", self.start_drag)
        self.bind("<B1-Motion>", self.perform_action)
        self.bind("<ButtonRelease-1>", self.end_action)

        # Initialize the rectangle and square properties
        self.rect = None
        self.dragging = False
        self.scaling = False
        self.square_size = 0
        self.square_x = 0
        self.square_y = 0

    def load_image(self):
        """Loads the current image from the list."""
        image_path = self.image_list[self.image_index]
        self.original_image = Image.open(image_path)
        self.display_image = self.original_image.copy()
        self.update_canvas()

        # Initialize the square
        self.init_square()

    def update_canvas(self):
        """Updates the canvas with the current image."""
        self.tk_image = ImageTk.PhotoImage(self.display_image.resize((800, 800), Image.Resampling.LANCZOS))
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

    def init_square(self):
        """Initialize the square to be the largest possible square that fits in the image."""
        img_width, img_height = self.original_image.size
        square_size = min(img_width, img_height)
        self.square_size = square_size

        # Center the square
        self.square_x = (img_width - square_size) // 2
        self.square_y = (img_height - square_size) // 2

        # Draw the square
        self.draw_square()

    def draw_square(self):
        """Draw the square with a semi-transparent fill."""
        self.canvas.delete("selection")

        # Convert square coordinates to canvas coordinates
        canvas_square_x0 = int(self.square_x * 800 / self.original_image.width)
        canvas_square_y0 = int(self.square_y * 800 / self.original_image.height)
        canvas_square_x1 = int((self.square_x + self.square_size) * 800 / self.original_image.width)
        canvas_square_y1 = int((self.square_y + self.square_size) * 800 / self.original_image.height)

        self.rect = self.canvas.create_rectangle(canvas_square_x0, canvas_square_y0, 
                                                 canvas_square_x1, canvas_square_y1, 
                                                 outline="red", width=2, fill='gray', stipple='gray50', tags="selection")

    def start_drag(self, event):
        """Handles mouse press to start dragging or scaling."""
        self.start_x = event.x
        self.start_y = event.y

        if event.state & 0x0001:  # If Shift key is held
            self.scaling = True
        else:
            self.dragging = True

    def perform_action(self, event):
        """Handles dragging or scaling based on user input."""
        if self.dragging:
            dx = (event.x - self.start_x) * self.original_image.width / 800
            dy = (event.y - self.start_y) * self.original_image.height / 800

            self.square_x = max(0, min(self.square_x + dx, self.original_image.width - self.square_size))
            self.square_y = max(0, min(self.square_y + dy, self.original_image.height - self.square_size))

            self.start_x, self.start_y = event.x, event.y
            self.draw_square()

        elif self.scaling:
            delta = (event.y - self.start_y) * self.original_image.height / 800
            new_size = self.square_size + delta

            if new_size > 0 and new_size <= min(self.original_image.width, self.original_image.height):
                self.square_size = new_size

            self.square_x = max(0, min(self.square_x, self.original_image.width - self.square_size))
            self.square_y = max(0, min(self.square_y, self.original_image.height - self.square_size))

            self.start_y = event.y
            self.draw_square()

    def end_action(self, event):
        """Ends dragging or scaling when mouse button is released."""
        self.dragging = False
        self.scaling = False

    def save_and_next(self):
        """Crops, saves the current image, and loads the next one."""
        if self.rect:
            cropped_image = self.original_image.crop((self.square_x, self.square_y, 
                                                      self.square_x + self.square_size, 
                                                      self.square_y + self.square_size))
            # Resize the cropped image to a square
            square_image = cropped_image.resize((800, 800))
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
    image_list = [os.path.join(IMAGE_DIR, f) for f in os.listdir(IMAGE_DIR) if f.endswith('.png')]
    
    if not image_list:
        messagebox.showerror("Error", "No images found in the directory.")
        return
    
    app = ImageCropper(image_list)
    app.mainloop()

if __name__ == "__main__":
    main()
