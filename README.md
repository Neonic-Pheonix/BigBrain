# Screen To Text

This is a tool for getting the text string out of a snippet from the screen.
It utilises the PyTesseract module to extract the text out of the screen snippet that the user takes using the snipping tool.
The text is copied to the clipboard for quick and easy access.
For a quick start of the programme, you can create a shortcut-key combination in the properties of the application file.


## Installation

To start using the app do next:

- Download and extract the 'ScreenToText' zipped folder
- In the extracted folder, find the 'ScreenToText.exe' file and create a shortcut for it
- In the properties of the shortcut, create a shortcut-key to easily start the app. Recommended key combinations can start with 'Ctrl+Alt' and have one more letter key (make sure that the combination is not used in other software).


## How to use

After starting the application, a screenshot of what was on the screen will be displayed. 
Use the cursor to draw a rectangle around the text you want to be extracted (very much like any other snipping tool).
Right after that, the screenshot will disappear and the extracted text (if any) will appear in the clipboard, ready for use.
Use 'Esc' key to exit the app.


## *Tips*

For better performance make sure the text is in high contrast with its background.
Having the text displayed with higher resolution also improves the quality and accuracy of text recognition.
If possible, leaving some padding around the text area can be helpful.


## Languages

The application is set to recognise texts in the English language only.
To change this you can follow the link https://github.com/UB-Mannheim/tesseract/wiki,
select either of the two download options:

![sorry, image not found](https://github.com/Neonic-Pheonix/BigBrain/blob/main/readme_image.png?raw=true)

Then open the downloaded installer and follow the steps in it to select the languages and scripts you want the app to recognize.
After that, replace the 'Tesseract' folder in the directory of the application with the 'Tesseract' folder that was installed by the wizard. This will essentially modify the configuration of the library.