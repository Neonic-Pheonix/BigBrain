import tkinter
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import pyperclip


start_x = 0
curX = 0
start_y = 0
curY = 0
selection_rect = 0

def on_button_press(event):
    global start_x, start_y, canvas, selection_rect
    # save mouse drag start position
    start_x = canvas.canvasx(event.x)
    start_y = canvas.canvasy(event.y)

    selection_rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, fill=None, outline='white', width=3)

def on_move_press(event):
    global start_x, curX, start_y, curY, canvas, selection_rect
    curX = canvas.canvasx(event.x)
    curY = canvas.canvasy(event.y)

    # expand rectangle as you drag the mouse
    canvas.coords(selection_rect, start_x, start_y, curX, curY)    

def on_button_release(event):
    global start_x, curX, start_y, curY, selection_rect, root
    selection = pilImage.crop(box=(start_x, start_y, curX, curY))
    pyperclip.copy('type of the image: ' + str(type(selection)))

    event.widget.unbind("<B1-Motion>")
    event.widget.unbind("<ButtonPress-1>")
    event.widget.unbind("<ButtonRelease-1>")
    root.withdraw()
    root.quit()



root = tkinter.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
print(w, h)
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.focus_set()    
root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))
canvas = tkinter.Canvas(root,width=w,height=h)
canvas.pack()
canvas.configure(background='black')
canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_move_press)
canvas.bind("<ButtonRelease-1>", on_button_release)
pilImage = ImageGrab.grab()
imgWidth, imgHeight = pilImage.size
print(imgWidth, imgHeight)
if imgWidth > w or imgHeight > h:
    ratio = min(w/imgWidth, h/imgHeight)
    imgWidth = int(imgWidth*ratio)
    imgHeight = int(imgHeight*ratio)
    pilImage = pilImage.resize((imgWidth,imgHeight), Image.ANTIALIAS)
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(w/2,h/2,image=image)
root.mainloop()