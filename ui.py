import tkinter
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import pyperclip


class screen:
    def __init__(self):
        self.root = tkinter.Tk()
        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.overrideredirect(1)
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.focus_set()    
        self.root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
        self.canvas = tkinter.Canvas(self.root,width=w,height=h)
        self.canvas.pack()
        self.canvas.configure(background='black')
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.pilImage = ImageGrab.grab()
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
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, fill=None, outline='white', width=3)

    def on_move_press(self, event):
        self.curX = self.canvas.canvasx(event.x)
        self.curY = self.canvas.canvasy(event.y)
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, self.curX, self.curY)    

    def on_button_release(self, event):
        selection = self.pilImage.crop(box=(self.start_x, self.start_y, self.curX, self.curY))
        pyperclip.copy('type of the image: ' + str(type(selection)))

        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonPress-1>")
        self.root.unbind("<ButtonRelease-1>")
        self.root.withdraw()
        self.root.quit()