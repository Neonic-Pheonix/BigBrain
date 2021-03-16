import tkinter
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import pyperclip


class screen:
    def __init__(self, image_selected_callback):
        # initialising the GUI window
        self.root = tkinter.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(1)
        self.root.resizable(0, 0)
        self.root.focus_set()
        # making Esc key quit the program
        self.root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

        # initializing the canvas for the screenshot to be displayed on
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tkinter.Canvas(self.root,width=w,height=h,highlightthickness=0)
        self.canvas.pack()
        self.canvas.configure(background='black')
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", lambda event, callback=image_selected_callback: self.on_button_release(event, callback))

        # taking the screenshot
        self.pilImage = ImageGrab.grab()
        # resizing the image if it is too big
        imgWidth, imgHeight = self.pilImage.size
        if imgWidth > w or imgHeight > h:
            ratio = min(w/imgWidth, h/imgHeight)
            imgWidth = int(imgWidth*ratio)
            imgHeight = int(imgHeight*ratio)
            self.pilImage = self.pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(self.pilImage)
        imagesprite = self.canvas.create_image(w/2,h/2,image=image)
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
        # cropping the screenshot
        selection = self.pilImage.crop(box=(self.start_x, self.start_y, self.curX, self.curY))
        pyperclip.copy('type of the image: ' + str(type(selection)))

        # undinbing eventhadlers for the mouse
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonPress-1>")
        self.root.unbind("<ButtonRelease-1>")
        # hiding the window
        self.root.withdraw()
        self.root.quit()
        
        callback(Image.Image.getdata(selection))