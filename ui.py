import pyperclip
from tkinter import Tk, Canvas
from PIL import Image, ImageTk, ImageGrab


class screen:
    def __init__(self, image_selected_callback):
        # taking the screenshot
        self.pilImage = ImageGrab.grab()

        # initialising the GUI window
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(1)
        self.root.resizable(0, 0)
        self.root.focus_set()
        # making Esc key quit the program
        self.root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

        # initializing the canvas for the screenshot to be displayed on
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = Canvas(self.root,width=w,height=h,highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='black')
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", lambda event, callback=image_selected_callback: self.on_button_release(event, callback))

        # displaying the screenshot
        image = ImageTk.PhotoImage(self.pilImage)
        self.canvas.create_image(w/2,h/2,image=image)
        self.canvas.create_rectangle(0,0,w,h, fill="red", stipple='gray25')
        self.root.mainloop()

    def on_button_press(self, event):
        # saving the top left corner for the clipped image
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        # saving the current position of the bottom right corner
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)
        # drawing the rectangle
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, fill=None, outline='white', width=3)

    def on_move_press(self, event):
        # saving the current position of the bottom right corner
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)
        # drawing the rectangle
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, self.curX, self.curY)    

    def on_button_release(self, event, callback):
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
        
        recognized_text = callback(Image.Image.getdata(selection))
        pyperclip.copy(recognized_text)
