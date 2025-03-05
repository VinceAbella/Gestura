import tkinter as tk
from PIL import Image, ImageTk
from handtracking import hand_tracking

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Sign Language Translator")

        # Create a label for the video feed
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # buttons
        self.start_button = tk.Button(root, text="Start", font=("Arial", 16), command=self.start_video)
        self.learn_button = tk.Button(root, text="Learn", font=("Arial", 16), command=self.learn)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.learn_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Initialize the hand tracking generator
        self.hand_tracking_gen = None

    def start_video(self):
        # Start the hand tracking generator
        self.hand_tracking_gen = hand_tracking()
        self.update_frame()

    def update_frame(self):
        if self.hand_tracking_gen:
            try:
                # Get the next frame from the generator
                frame = next(self.hand_tracking_gen)

                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                self.video_label.after(10, self.update_frame)
            except StopIteration:
                
                self.hand_tracking_gen = None

    def learn(self):
        print("Learn button clicked")

    def on_closing(self):
        # Clean up resources when the window is closed
        if self.hand_tracking_gen:
            self.hand_tracking_gen.close()  
        self.root.destroy()