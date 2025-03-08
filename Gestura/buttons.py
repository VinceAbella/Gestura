import tkinter as tk
from PIL import Image, ImageTk
from handtracking import hand_tracking

class MainMenu:
    def __init__(self, parent, start_command, learn_command):
        self.frame = tk.Frame(parent)
        
        self.start_button = tk.Button(
            self.frame, 
            text="Start", 
            font=("Arial", 15), 
            width=10, 
            command=start_command
        )
        self.learn_button = tk.Button(
            self.frame, 
            text="Learn", 
            font=("Arial", 15), 
            width=10, 
            command=learn_command
        )
        
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.learn_button.pack(side=tk.LEFT, padx=10)
        
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def show(self):
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    def hide(self):
        self.frame.place_forget()

class VideoFrame:
    def __init__(self, parent, stop_command):
        self.parent = parent
        
        self.video_label = tk.Label(parent)
        self.video_label.pack_forget()
        
        self.stop_frame = tk.Frame(parent)
        self.stop_button = tk.Button(
            self.stop_frame,
            text="Stop", 
            font=("Arial", 15), 
            width=10, 
            command=stop_command
        )
        self.stop_button.pack()
        self.stop_frame.place(relx=0.5, rely=1.0, anchor=tk.S, y=-20)
        self.stop_frame.place_forget()
    
    def show(self):
        self.video_label.pack()
        self.stop_frame.place(relx=0.5, rely=1.0, anchor=tk.S, y=-20)
    
    def hide(self):
        self.video_label.pack_forget()
        self.stop_frame.place_forget()
    
    def update_image(self, frame):
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

class HandTrackingController:
    def __init__(self):
        self.generator = hand_tracking()
    
    def get_next_frame(self):
        try:
            return next(self.generator)
        except StopIteration:
            return None
    
    def close(self):
        self.generator.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Basic Sign Language Translator")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        
        self.main_menu = MainMenu(root, self.start_video, self.learn)
        self.video_frame = VideoFrame(root, self.stop_video)
        self.hand_tracking_controller = None
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def start_video(self):
        """Start video processing and update UI"""
        self.hand_tracking_controller = HandTrackingController()
        self.main_menu.hide()
        self.video_frame.show()
        self.update_frame()
    
    def stop_video(self):
        """Stop video processing and reset UI"""
        if self.hand_tracking_controller:
            self.hand_tracking_controller.close()
            self.hand_tracking_controller = None
        self.video_frame.hide()
        self.main_menu.show()
    
    def update_frame(self):
        if self.hand_tracking_controller:
            frame = self.hand_tracking_controller.get_next_frame()
            if frame is not None:
                self.video_frame.update_image(frame)
                self.root.after(10, self.update_frame)
            else:
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