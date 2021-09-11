import pyperclip
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract\\tesseract.exe'
from tkinter import Tk, Canvas
from PIL import ImageGrab, ImageTk
from math import atan2, degrees


class app:
    def __init__(self):
        # taking the screenshot
        self.pilImage = ImageGrab.grab()

        # initialising the GUI window
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(1)
        self.root.focus_set()
        # making Esc key quit the program
        self.root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

        # initializing the canvas for the screenshot to be displayed on
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = Canvas(self.root,width=w,height=h,highlightthickness=0,cursor="tcross")
        self.canvas.pack()
        
        # displaying the screenshot
        image = ImageTk.PhotoImage(self.pilImage.rotate(90))
        self.canvas.create_image(w/2,h/2,image=image)
        self.canvas.create_rectangle(0,0,w,h, fill="#36558f", stipple='gray12')

        # binding event handlers for mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Control>", self.bind_rotation)

        self.root.mainloop()

    def on_button_press(self, event):
        # saving the first corner for the clipped image
        self.start_x = int(event.x)
        self.start_y = int(event.y)

        # saving the current position of the bottom right corner
        self.end_x = int(event.x)
        self.end_y = int(event.y)

        # drawing the rectangle
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, fill=None, outline='white', width=2)

    def on_move_press(self, event):
        # saving the current position of the second corner
        self.end_x = int(event.x)
        self.end_y = int(event.y)

        # drawing the rectangle
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_move_rotate(self, event):
        #calculating new rotation angle
        rel = (int(event.x) - self.rotation_centre[0], int(event.y) - self.rotation_centre[1])
        ang = degrees(atan2(rel[1], rel[0]) - atan2(rel[1], 0))
        self.cur_angle = ang + 360 if ang < 0 else ang

        #rotating the rectangle
        self.selection_rect.rotate()

    def bind_rotation(self, event):
        self.root.unbind("<B1-Motion>")

        #identifying coordinates
        if(self.start_x > self.end_x):
            self.start_x, self.end_x = self.end_x, self.start_x
        if(self.start_y > self.end_y):
            self.start_y, self.end_y = self.end_y, self.start_y
        
        #identifying the centre
        centre_x = self.start_y + self.selection_rect.height/2
        centre_y = self.start_x + self.selection_rect.width/2
        self.rotation_centre = (centre_x, centre_y)

        #recording staring angle before rotating
        rel = (self.end_x - centre_x, self.end_y - centre_y)
        ang = degrees(atan2(rel[1]-centre_y, rel[0]-centre_x) - atan2(rel[1]-centre_y, 0-centre_x))
        self.start_angle = ang + 360 if ang < 0 else ang

        self.canvas.bind("<B1-Motion>", self.on_move_rotate)

    def on_button_release(self, event):
        # hiding the window
        self.root.withdraw()

        # undinbing eventhadlers for the mouse
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonPress-1>")
        self.root.unbind("<ButtonRelease-1>")
        self.root.unbind("<Control>")
        self.root.quit()

        #identifying coordinates
        if(self.start_x > self.end_x):
            self.start_x, self.end_x = self.end_x, self.start_x
        if(self.start_y > self.end_y):
            self.start_y, self.end_y = self.end_y, self.start_y
        # cropping the screenshot
        selection = self.pilImage.crop(box=(self.start_x, self.start_y, self.end_x, self.end_y))
        
        # passing the image for text recognition
        recognized_text = pytesseract.image_to_string(selection)
        if recognized_text != "":
            pyperclip.copy(recognized_text)


app()