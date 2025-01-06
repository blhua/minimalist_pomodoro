import tkinter as tk

class CircleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimalist Pomodoro")
        
        # Set the size of the window to 300x50
        self.root.geometry("260x80")  # Increased window size to fit reset button

        # Create a canvas to draw circles
        self.canvas = tk.Canvas(root, width=260, height=40)  # Adjust canvas size to fit the window
        self.canvas.pack()

        # List to hold the circle IDs (for managing circles)
        self.circles = []
        
        # Draw 5 circles on the canvas
        self.create_circles()

       # Create a frame to hold the buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, pady=0)  # Move the button frame higher by reducing pady
        
        # Create a Label with text "WORK" next to the Start button
        self.status_label = tk.Label(self.button_frame, text="WORK", font=("Helvetica", 12, "bold"), fg="black")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Add a start button
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_timing)
        self.start_button.pack(side=tk.LEFT, padx=10)  # Pack start button to the left

        # Add a reset button next to the start button
        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_app)
        self.reset_button.pack(side=tk.LEFT)  # Pack reset button to the left, next to the start button

        # Timer and circle index
        #5min * 60s/min * 1000ms/s
        self.work_interval = 5*60*1000  # 3 seconds for demo purposes
        #1min * 60s/min * 1000ms/s
        self.rest_interval = 1*60*1000
        self.circle_index = 0
        self.status="WORK"
        self.countdown_id=None

    def create_circles(self):
        """Create five circles and store their ids."""
        radius = 10  # Smaller radius for smaller window
        circle_spacing = 50  # Space the circles apart to fit across the width

        for i in range(5):
            # Position the circles along the x-axis, evenly spaced
            x = 30 + i * circle_spacing  # Starting x position + 50 pixels for each circle
            y = 25  # Center vertically within the 50-pixel height of the window
            circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue")
            self.circles.append(circle)

    def start_timing(self):

        if self.status=="WORK":
            self.clean_start()
                
            """Start the process of disappearing circles after a delay."""
            self.start_button.config(state=tk.DISABLED)  # Disable the start button after clicking
            # Schedule the first disappearance after 3 seconds (3000 ms) for testing purposes
            self.countdown_id=self.root.after(self.work_interval, self.update_circle)

        elif self.status=="REST":
            self.clean_start()
                
            """Start the process of disappearing circles after a delay."""
            self.start_button.config(state=tk.DISABLED)  # Disable the start button after clicking
            # Schedule the first disappearance after 3 seconds (3000 ms) for testing purposes
            self.countdown_id=self.root.after(self.rest_interval, self.update_circle)

    def update_circle(self):

        if self.status=="WORK":

            """Hide one circle every 3 seconds, then flash when all are gone."""
            if self.circle_index < 4:
                # Hide the next circle
                self.canvas.itemconfig(self.circles[self.circle_index], state="hidden")
                self.circle_index += 1
    
                # Schedule the next circle disappearance after another 3 seconds (3000 ms)
                self.countdown_id=self.root.after(self.work_interval, self.update_circle)
            else:
                # All circles have disappeared, stop any further scheduling and start flashing immediately
                self.flash_circles()

        elif self.status=="REST":

            """Hide one circle every 3 seconds, then flash when all are gone."""
            if self.circle_index < 4:
                # Hide the next circle
                self.canvas.itemconfig(self.circles[self.circle_index], state="hidden")
                self.circle_index += 1
    
                # Schedule the next circle disappearance after another 3 seconds (3000 ms)
                self.countdown_id=self.root.after(self.rest_interval, self.update_circle)
            else:
                # All circles have disappeared, stop any further scheduling and start flashing immediately
                self.flash_circles()

    def flash_circles(self):
        """Make all circles flash by toggling their visibility immediately."""
        # Make sure all circles are visible immediately after disappearance
        for i in range(5):
            self.canvas.itemconfig(self.circles[i], state="normal")
        
        # Start flashing immediately by toggling states directly
        self._flash_step(0)  # Start the flashing sequence immediately
        self.start_button.config(state=tk.NORMAL)

        if self.status=="WORK":
            self.status_label.config(text="REST")
            self.status="REST"
        elif self.status=="REST":
            self.status_label.config(text="WORK")
            self.status="WORK"

        

    def _flash_step(self, step):
        """Recursively toggle the visibility of circles for the flashing effect."""
        # Toggle the state of circles between visible and hidden
        state = "normal" if step % 2 == 0 else "hidden"

        # Apply the state change to all circles
        for i in range(5):
            self.canvas.itemconfig(self.circles[i], state=state)

        # Continue flashing by calling this function again after 200ms
        if step < 20:  # Flash for a total of 5 steps (each step toggles visibility)
            self.root.after(200, self._flash_step, step + 1)  # Toggle every 200ms

    def clean_start(self):
        """Reset the application to its initial state."""
        # Cancel any ongoing countdown if it exists
        if self.countdown_id is not None:
            self.root.after_cancel(self.countdown_id)
            self.countdown_id = None  # Clear the countdown ID        
        
        # Reset circle visibility
        self.circle_index = 0
        for i in range(5):
            self.canvas.itemconfig(self.circles[i], state="normal")


    def reset_app(self):
        """Reset the application to its initial state."""
        # Cancel any ongoing countdown if it exists
        if self.countdown_id is not None:
            self.root.after_cancel(self.countdown_id)
            self.countdown_id = None  # Clear the countdown ID        
        
        # Reset circle visibility
        self.circle_index = 0
        for i in range(5):
            self.canvas.itemconfig(self.circles[i], state="normal")

        # Enable the start button again and disable reset during the game
        self.status_label.config(text="WORK")
        self.status="WORK"
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.NORMAL)
        
# Set up the main Tkinter window
root = tk.Tk()
app = CircleApp(root)
root.mainloop()
