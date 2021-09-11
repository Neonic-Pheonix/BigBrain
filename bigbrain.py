from os import remove
from pyperclip import copy
from tkinter import Tk, Canvas
from PIL import ImageGrab, ImageTk
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


class app:
    def __init__(self):
        # taking the screenshot
        self.screen_shot = ImageGrab.grab()

        # initialising the GUI window
        self.root = Tk()
        self.root.attributes("-fullscreen", True)
        self.root.overrideredirect(1)
        self.root.focus_set() 

        # initializing the canvas for the screenshot to be displayed on
        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = Canvas(self.root,width=screen_w,height=screen_h,highlightthickness=0,cursor="tcross")
        self.canvas.pack()
        
        # displaying the screenshot
        image = ImageTk.PhotoImage(self.screen_shot)
        self.canvas.create_image(screen_w/2,screen_h/2,image=image)
        self.canvas.create_rectangle(0,0,screen_w,screen_h, fill="#36558f", stipple='gray12')

        # binding event handlers for mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: (e.widget.withdraw(), e.widget.quit()))

        # Get a client for the computer vision service
        self.cog_key = 'COG_KEY'
        self.cog_endpoint = 'COG_ENDPOINT'
        self.computervision_client = ComputerVisionClient(self.cog_endpoint, CognitiveServicesCredentials(self.cog_key))

        self.root.mainloop()

    def on_button_press(self, event):
        # saving the first corner for the clipped image
        self.start_x = event.x
        self.start_y = event.y

        # saving the current position of the bottom right corner
        self.end_x = event.x
        self.end_y = event.y

        # drawing the rectangle
        self.selection_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, fill=None, outline='white', width=2)

    def on_move_press(self, event):
        # saving the current position of the second corner
        self.end_x = event.x
        self.end_y = event.y

        # drawing the rectangle
        self.canvas.coords(self.selection_rect, self.start_x, self.start_y, self.end_x, self.end_y)

    def on_button_release(self, event):
        # hiding the window
        self.root.withdraw()

        # undinbing eventhadlers
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonPress-1>")
        self.root.unbind("<ButtonRelease-1>")
        self.root.unbind("<Control>")
        self.root.unbind("<Escape>")
        self.root.quit()

        #identifying coordinates
        if(self.start_x > self.end_x):
            self.start_x, self.end_x = self.end_x, self.start_x
        if(self.start_y > self.end_y):
            self.start_y, self.end_y = self.end_y, self.start_y
        # cropping the screenshot
        selection = self.screen_shot.crop(box=(self.start_x, self.start_y, self.end_x, self.end_y))

        selection.save('iugh8t7fniu408f7hq20oir-8.png', format='PNG')

        # Use the Computer Vision service to find text in the image
        read_results = self.computervision_client.recognize_printed_text_in_stream(open('iugh8t7fniu408f7hq20oir-8.png', 'rb'), detect_orientation=True)
        
        remove('iugh8t7fniu408f7hq20oir-8.png')

        outputText = ''
        # Process the text line by line & word by word
        for region in read_results.regions:
            for line in region.lines:
                # Read the words in the line of text
                line_text = ''
                for word in line.words:            
                    line_text += word.text + ' '
                outputText += line_text + '\n'
        # copy the result to clipboard
        if outputText != '':
            copy(outputText)


def main():
    app()

if __name__ == "__main__":
    main()
