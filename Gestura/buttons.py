import tkinter as tk
from PIL import Image, ImageTk
from handtracking import hand_tracking

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Sign Language Translator")
        self.root.geometry("648x470")
        self.root.resizable(False, False)

        self.video_label = tk.Label(root)
        self.video_label.pack_forget()

        self.button_frame = tk.Frame(root)
        self.button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.start_button = tk.Button(
            self.button_frame, 
            text="Start", 
            font=("Arial", 15), 
            width=10, 
            command=self.start_video
        )
        self.learn_button = tk.Button(
            self.button_frame, 
            text="Learn", 
            font=("Arial", 15), 
            width=10, 
            command=self.learn
        )
        
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.learn_button.pack(side=tk.LEFT, padx=10)

        self.stop_frame = tk.Frame(root)
        self.stop_button = tk.Button(
            self.stop_frame,
            text="Stop", 
            font=("Arial", 15), 
            width=10, 
            command=self.stop_video
        )
        self.stop_button.pack()
        self.stop_frame.place(relx=0.5, rely=1.0, anchor=tk.S, y=-20)
        self.stop_frame.place_forget()

        self.hand_tracking_gen = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_video(self):
        """Start video processing and update UI"""
        self.video_label.pack() 
        self.button_frame.place_forget()  
        self.stop_frame.place(relx=0.5, rely=1.0, anchor=tk.S, y=-20)  
        self.hand_tracking_gen = hand_tracking()
        self.update_frame()

    def stop_video(self):
        """Stop video processing and reset UI"""
        self.video_label.pack_forget()  
        self.stop_frame.place_forget() 
        self.button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 
        if self.hand_tracking_gen:
            self.hand_tracking_gen.close()
            self.hand_tracking_gen = None

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
                self.stop_video()

    def learn(self):
        print("Learn button clicked")

    def on_closing(self):
        self.stop_video()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()