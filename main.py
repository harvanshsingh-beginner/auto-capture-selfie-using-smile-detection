import os
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import threading


class face_recognition_system:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        
        # Create selfies directory if it doesn't exist
        self.selfie_dir = "selfies"
        if not os.path.exists(self.selfie_dir):
            os.makedirs(self.selfie_dir)

        # Try to load images with error handling
        self.setup_images()
        
        # Setup the GUI elements
        self.setup_gui()

    def setup_images(self):
        """Setup all images with error handling for missing files."""
        try:
            # Create a default colored rectangle if images don't exist
            default_size = (500, 250)
            
            # Try to load first image or create default
            try:
                img1 = Image.open(r"C:\Users\harsh bhaskar\OneDrive\Desktop\coding\face_recognization_software\software images\color.jpg")
                img1 = img1.resize(default_size, Image.Resampling.LANCZOS)
            except (FileNotFoundError, OSError):
                # Create a default colored image
                img1 = Image.new('RGB', default_size, color='lightblue')
            self.photoimg1 = ImageTk.PhotoImage(img1)

            # Try to load second image or create default
            try:
                img2 = Image.open(r"C:\Users\harsh bhaskar\OneDrive\Desktop\coding\face_recognization_software\software images\face.jpg")
                img2 = img2.resize(default_size, Image.Resampling.LANCZOS)
            except (FileNotFoundError, OSError):
                img2 = Image.new('RGB', default_size, color='lightgreen')
            self.photoimg2 = ImageTk.PhotoImage(img2)

            # Try to load third image or create default
            try:
                img3 = Image.open(r"C:\Users\harsh bhaskar\OneDrive\Desktop\coding\face_recognization_software\software images\color.jpg")
                img3 = img3.resize(default_size, Image.Resampling.LANCZOS)
            except (FileNotFoundError, OSError):
                img3 = Image.new('RGB', default_size, color='lightcoral')
            self.photoimg3 = ImageTk.PhotoImage(img3)

            # Try to load background image or create default
            bg_size = (1530, 810)
            try:
                img = Image.open(r"C:\Users\harsh bhaskar\OneDrive\Desktop\coding\face_recognization_software\software images\background.jpg")
                img = img.resize(bg_size, Image.Resampling.LANCZOS)
            except (FileNotFoundError, OSError):
                img = Image.new('RGB', bg_size, color='white')
            self.photoimg = ImageTk.PhotoImage(img)

            # Try to load button image or create default
            button_size = (120, 120)
            try:
                img4 = Image.open(r"C:\Users\harsh bhaskar\OneDrive\Desktop\coding\face_recognization_software\software images\button.jpg")
                img4 = img4.resize(button_size, Image.Resampling.LANCZOS)
            except (FileNotFoundError, OSError):
                img4 = Image.new('RGB', button_size, color='skyblue')
            self.photoimg4 = ImageTk.PhotoImage(img4)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Create minimal default images
            self.photoimg1 = self.photoimg2 = self.photoimg3 = None
            self.photoimg = self.photoimg4 = None

    def setup_gui(self):
        """Setup the GUI elements."""
        # Display header images
        if self.photoimg1:
            f_label1 = Label(self.root, image=self.photoimg1)
            f_label1.place(x=0, y=0, width=500, height=250)

        if self.photoimg2:
            f_label2 = Label(self.root, image=self.photoimg2)
            f_label2.place(x=500, y=0, width=500, height=250)

        if self.photoimg3:
            f_label3 = Label(self.root, image=self.photoimg3)
            f_label3.place(x=1000, y=0, width=500, height=250)

        # Background image
        if self.photoimg:
            bg_image = Label(self.root, image=self.photoimg)
            bg_image.place(x=0, y=250, width=1530, height=810)
        else:
            # Create a simple background if image not found
            bg_image = Label(self.root, bg='lightgray')
            bg_image.place(x=0, y=250, width=1530, height=810)

        # Title label
        title_lbl = Label(bg_image, text="AUTO CAPTURE SELFIE BY DETECTING SMILE",
                          font=("times new roman", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=55)

        # Start Camera Button
        if self.photoimg4:
            b1 = Button(bg_image, image=self.photoimg4, command=self.run_test_script,
                        cursor="hand2")
        else:
            b1 = Button(bg_image, text="Start\nCamera", command=self.run_test_script,
                        font=("times new roman", 12, "bold"), bg="lightblue", fg="black",
                        cursor="hand2")
        b1.place(x=635, y=100, width=120, height=120)

        # Button label
        b1_label = Label(bg_image, text="Start Camera", font=("times new roman", 12, "bold"),
                         bg="white", fg="black")
        b1_label.place(x=635, y=230, width=120, height=25)

        # View Photos Button
        b2 = Button(bg_image, text="View Photos", command=self.view_photos, 
                    font=("times new roman", 15, "bold"),
                    bg="lightcyan", fg="black", cursor="hand2")
        b2.place(x=775, y=100, width=120, height=120)

        # Status label
        self.status_label = Label(bg_image, text="Ready to start", 
                                  font=("times new roman", 14), bg="white", fg="green")
        self.status_label.place(x=600, y=280, width=300, height=30)

    def run_test_script(self):
        """Run the test.py script."""
        try:
            # Get the directory where main.py is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            test_py_path = os.path.join(script_dir, "test.py")
            
            # Debug information
            print("Script directory:", script_dir)
            print("Looking for test.py at:", test_py_path)
            
            # Change to the correct directory
            original_cwd = os.getcwd()
            os.chdir(script_dir)
            
            # Check if test.py exists in the correct directory
            if not os.path.exists("test.py"):
                messagebox.showerror("Error", f"test.py file not found in {script_dir}!\n\nPlease make sure test.py is in the same directory as main.py")
                print("Files in script directory:", os.listdir(script_dir))
                os.chdir(original_cwd)  # Change back
                return
            
            print("Found test.py, starting camera...")
            self.status_label.config(text="Starting camera...", fg="orange")
            self.root.update()

            # Method 1: Try subprocess first
            def run_with_subprocess():
                try:
                    result = subprocess.run(["python", "test.py"], 
                                          capture_output=False,  # Let output show in console
                                          cwd=script_dir)  # Use correct working directory
                    
                    # Change back to original directory
                    os.chdir(original_cwd)
                    
                    if result.returncode == 0:
                        self.status_label.config(text="Camera session completed", fg="green")
                        self.root.after(1000, self.update_status)
                    else:
                        self.status_label.config(text="Camera session ended", fg="orange")
                        
                except Exception as e:
                    print(f"Subprocess error: {e}")
                    # Fallback to os.system
                    run_with_os_system()

            # Method 2: Fallback using os.system
            def run_with_os_system():
                try:
                    print("Using os.system fallback...")
                    # Make sure we're in the right directory
                    os.chdir(script_dir)
                    result = os.system('python test.py')
                    
                    # Change back to original directory
                    os.chdir(original_cwd)
                    
                    if result == 0:
                        self.status_label.config(text="Camera session completed", fg="green")
                    else:
                        self.status_label.config(text="Camera session ended", fg="orange")
                    self.root.after(1000, self.update_status)
                except Exception as e:
                    print(f"OS system error: {e}")
                    self.status_label.config(text="Failed to start camera", fg="red")
                    os.chdir(original_cwd)  # Ensure we change back even on error

            # Start in separate thread to prevent GUI freezing
            script_thread = threading.Thread(target=run_with_subprocess, daemon=True)
            script_thread.start()

        except Exception as e:
            print(f"Error running test script: {e}")
            messagebox.showerror("Error", f"Failed to start camera:\n{str(e)}")
            self.status_label.config(text="Failed to start camera", fg="red")

    def update_status(self):
        """Update the status with current photo count."""
        photo_count = self.count_photos()
        self.status_label.config(text=f"Ready - {photo_count} photos saved", fg="green")

    def count_photos(self):
        """Count the number of selfies saved."""
        try:
            # First check in selfies directory
            if os.path.exists(self.selfie_dir):
                selfie_photos = [f for f in os.listdir(self.selfie_dir) 
                               if f.startswith("selfie_") and f.endswith(".png")]
            else:
                selfie_photos = []
            
            # Also check in current directory (in case test.py saves there)
            current_dir_photos = [f for f in os.listdir('.') 
                                if f.startswith("selfie_") and f.endswith(".png")]
            
            return len(selfie_photos) + len(current_dir_photos)
        except:
            return 0

    def view_photos(self):
        """Open a new window to display clicked photos."""
        try:
            viewer = Toplevel(self.root)
            viewer.title("Clicked Photos")
            viewer.geometry("1000x600")
            viewer.configure(bg="white")

            # Add a canvas and scrollbar for scrolling
            main_frame = Frame(viewer)
            main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

            canvas = Canvas(main_frame, bg="white")
            scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
            scrollable_frame = Frame(canvas, bg="white")

            # Configure scrollable content
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            # Fetch all the saved photos from both directories
            photos = []
            
            # Check selfies directory
            if os.path.exists(self.selfie_dir):
                selfie_photos = [(os.path.join(self.selfie_dir, f), f) for f in os.listdir(self.selfie_dir) 
                               if f.startswith("selfie_") and f.endswith(".png")]
                photos.extend(selfie_photos)
            
            # Check current directory
            current_photos = [(f, f) for f in os.listdir('.') 
                            if f.startswith("selfie_") and f.endswith(".png")]
            photos.extend(current_photos)

            if not photos:
                no_photos_label = Label(scrollable_frame, 
                                       text="No photos found!\n\nStart the camera and smile to capture selfies.", 
                                       font=("times new roman", 16), 
                                       bg="white", fg="gray")
                no_photos_label.pack(pady=50)
                return

            # Sort photos by filename (newest first)
            photos.sort(key=lambda x: x[1], reverse=True)

            # Title
            title_label = Label(scrollable_frame, 
                               text=f"Your Selfies ({len(photos)} photos)", 
                               font=("times new roman", 20, "bold"), 
                               bg="white", fg="darkblue")
            title_label.pack(pady=10)

            # Create a frame for the photo grid
            photo_grid = Frame(scrollable_frame, bg="white")
            photo_grid.pack(pady=10)

            # Display each photo in a grid
            row = 0
            column = 0
            for i, (photo_path, photo_name) in enumerate(photos):
                try:
                    # Load and resize the photo
                    image = Image.open(photo_path)
                    image = image.resize((150, 150), Image.Resampling.LANCZOS)
                    photo_image = ImageTk.PhotoImage(image)

                    # Create a frame for each photo with label
                    photo_frame = Frame(photo_grid, bg="white", relief=RAISED, borderwidth=2)
                    photo_frame.grid(row=row, column=column, padx=10, pady=10)

                    # Display the photo
                    lbl = Label(photo_frame, image=photo_image)
                    lbl.image = photo_image  # Keep a reference
                    lbl.pack()

                    # Add photo name/date
                    name_label = Label(photo_frame, text=photo_name.replace("selfie_", "").replace(".png", ""),
                                      font=("arial", 8), bg="white", fg="gray")
                    name_label.pack()

                    column += 1
                    if column > 5:  # 6 photos per row
                        column = 0
                        row += 1

                except Exception as e:
                    print(f"Error loading photo {photo_name}: {e}")
                    continue

            # Add mouse wheel scrolling
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            canvas.bind("<MouseWheel>", on_mousewheel)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open photo viewer:\n{str(e)}")


if __name__ == "__main__":
    try:
        root = Tk()
        obj = face_recognition_system(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n{str(e)}")