import pyperclip
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'Tesseract\\tesseract.exe'
from tkinter import Tk, Canvas
from PIL import ImageGrab, ImageTk


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
        image = ImageTk.PhotoImage(self.pilImage)
        self.canvas.create_image(w/2,h/2,image=image)
        self.canvas.create_rectangle(0,0,w,h, fill="#36558f", stipple='gray12')

        # binding event handlers for mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.mainloop()

    def on_button_press(self, event):
        # saving the top left corner for the clipped image
        self.start_x = int(event.x)
        self.start_y = int(event.y)

        # saving the current position of the bottom right corner
        self.curX = int(event.x)
        self.curY = int(event.y)

        # drawing the rectangle
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.curX, self.curY, fill=None, outline='white', width=2)

    def on_move_press(self, event):
        # saving the current position of the bottom right corner
        self.curX = int(event.x)
        self.curY = int(event.y)

        # drawing the rectangle
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, self.curX, self.curY)    

    def on_button_release(self, event):
        # hiding the window
        self.root.withdraw()

        # undinbing eventhadlers for the mouse
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonPress-1>")
        self.root.unbind("<ButtonRelease-1>")
        self.root.quit()

        # cropping the screenshot
        if(self.start_x > self.curX):
            self.start_x, self.curX = self.curX, self.start_x
        if(self.start_y > self.curY):
            self.start_y, self.curY = self.curY, self.start_y
        selection = self.pilImage.crop(box=(self.start_x, self.start_y, self.curX, self.curY))
        
        # passing the image for text recognition
        recognized_text = pytesseract.image_to_string(selection)
        if recognized_text != "":
            pyperclip.copy(recognized_text)


app()