print("Importing")


from ctypes import windll # Import lib to make programme DPI Aware
from PIL import ImageGrab # Main screenshot lib
from pynput.mouse import Listener # Mouse input lib
from datetime import datetime # Date lib
from tkinter import filedialog # Import Filedialog from tkinter for dir
from tkinter import Tk # Import TK from tkinter 
import os # Import os lib
from infi.systray import SysTrayIcon # Import infi.systray for systray icon
import pathlib # Pathlib to get path
print("Done Importing")

user32 = windll.user32 # Set user32 var
user32.SetProcessDPIAware() # Make programme DPI Aware

# Set some vars
loc1x = -1
loc1y = -1
loc2x = -1
loc2y = -1

with open("Dir_Save", "r") as f: # Open the Dir_Save file
	temp = f.read() # Read file and set to temp
if temp == "": # Check if temp = null
	dirname = str(pathlib.Path(__file__).parent.absolute()) + "\\KSrc_Screenshots\\" # Set screenshot path
	print("Dir_Save empty")
	with open("Dir_Save", "w") as f: # Write screenshot path to the save file
		f.write(dirname)
else:
	dirname = temp # It just dumps the lad in dirname

print("Dir now: " + dirname)

def on_click(x, y, button, pressed):
	global loc1x, loc1y
	global loc2x, loc2y
	global dirname

	if str(button) == "Button.right" and pressed == True: # Checks if right mouse was pressed and stops screenshotting
		print("Cancelled")
		return False
		
	# Some bodged checksums
	if str(button) == "Button.left" and pressed == True:
		if loc1x == -1:
			loc1x = x
			loc1y = y
			print("Pos 1 set to:", loc1x, loc1y)
		else:
			loc2x = x
			loc2y = y

			# Stops screenshotting if area is 1x1 
			if loc1x == loc2x or loc1y == loc2y:
				return False
			print("Pos 2 set to:", loc2x, loc2y)

			# Very good code to make the vars 
			if loc1x > loc2x:
				x1 = loc2x
				x2 = loc1x
			else:
				x1 = loc1x
				x2 = loc2x

			if loc1y > loc2y:
				y1 = loc2y
				y2 = loc1y
			else:
				y1 = loc1y
				y2 = loc2y


			print("Saving: " + str(x1), str(y1), str(x2), str(y2))
			im = ImageGrab.grab(bbox=(x1,y1,x2,y2)) # Makes screenshot
			now = datetime.now().strftime("%Y-%m-%d %H-%M-%S") # Makes date thingy
			im.save(dirname + str(now) + ".png") # Saves screenshot
			print("Image Saved to: " + dirname)
			return False



def Screenshot(systray):
	global loc1x, loc1y, loc2x, loc2y
	# Set vars back original value
	loc1x = -1
	loc1y = -1
	loc2x = -1
	loc2y = -1
	print("Screenshotting . . .")
	with Listener(on_click=on_click) as listener: # Start listener
	    listener.join()


def OpenFolder(systray):
	global dirname 
	os.startfile(dirname) # OpenFolder

def AskDir(systray):
	global dirname 
	root = Tk() # Set tkinter root
	root.withdraw() # IDK stackoverflow said some
	root.iconbitmap('KSrcIcon.ico') # Set icon
	tempdir = filedialog.askdirectory(initialdir=dirname,  title='Please select a directory') # Do some stuff
	if tempdir != "": # Check if nothing was done
		dirname = tempdir # They did something? Brilliant!
	dirname += "\\" # Add this cuz python don't like me
	print("Dir set to: " + dirname)
	with open("Dir_Save", "w+") as f: # Set the dir back to save file
		f.write(dirname)
	


# I don't really understand this. Just copied it from stackoverflow
menu_options = (("Screenshot", None, Screenshot), ("Open Folder", None, OpenFolder), ("Set Directory", None, AskDir)) # Some systray stuff idk
systray = SysTrayIcon("KSrcIcon.ico", "KSrc", menu_options) # Even more systray stuff
systray.start() # Start them systray
