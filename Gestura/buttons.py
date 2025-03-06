import tkinter as tk
from PIL import Image, ImageTk
from handtracking import hand_tracking

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Sign Language Translator")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.video_label = tk.Label(root)
        self.video_label.pack()

        button_frame = tk.Frame(root)
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.start_button = tk.Button(button_frame, text="Start", font=("Arial", 15), width=10, command=self.start_video)
        self.learn_button = tk.Button(button_frame, text="Learn", font=("Arial", 15), width=10, command=self.learn)
       
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.learn_button.pack(side=tk.LEFT, padx=10)

        # Initialize the hand tracking generator
        self.hand_tracking_gen = None

    def start_video(self):
        self.hand_tracking_gen = hand_tracking()
        self.update_frame()

    def update_frame(self):
        if self.hand_tracking_gen:
            try:
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
        if self.hand_tracking_gen:
            self.hand_tracking_gen.close()  
        self.root.destroy()