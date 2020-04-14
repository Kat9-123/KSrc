print("Importing")



from ctypes import windll # Import lib to make programme DPI Aware
from PIL import ImageGrab # Main screenshot lib
from pynput.mouse import Controller # Mouse controller for position
from datetime import datetime # Date lib
from tkinter import Tk, filedialog # Import TK from tkinter and import Filedialog for dir
from os import startfile, path # Import os lib
from infi.systray import SysTrayIcon # Import infi.systray for systray icon
from pathlib import Path # Pathlib to get path
from win32api import GetKeyState # Mous input
from sys import exit # For exit
print("Done Importing")

user32 = windll.user32 # Set user32 var
user32.SetProcessDPIAware() # Make programme DPI Aware

# Set some vars
mouse = Controller()

with open("Dir_Save", "r") as f: # Open the Dir_Save file
	temp = f.read() # Read file and set to temp
if temp == "": # Check if temp = null
	dirname = str(Path(__file__).parent.absolute()) + "\\KSrc_Screenshots\\" # Set screenshot path
	print("Dir_Save empty")
	with open("Dir_Save", "w") as f: # Write screenshot path to the save file
		f.write(dirname)
else:
	dirname = temp # It just dumps the lad in dirname

print("Dir now: " + dirname)


def Screenshot(systray):
	global state_left, Pressed, root
	state_left = GetKeyState(0x01) 
	Pressed = False

	def MainUpdate():
		global Pressed, state_left, root
		global anchorx, anchory, posx, posy
		global xsu, ysu, xa, ya, xs, ys
		a = GetKeyState(0x01)
		if a != state_left:
			state_left = a

			if a < 0:
				Pressed = True
				anchorx = mouse.position[0]
				anchory = mouse.position[1]
				root.attributes("-fullscreen", False)
			else:
				if xa == xs or ya == ys:
					root.destroy()
					return
				Pressed = False
				root.destroy()
				print("Saving: " + str(xa), str(ya), str(xs), str(ys))
				im = ImageGrab.grab(bbox=(xa,ya,xs,ys)) # Makes screenshot
				now = datetime.now().strftime("%Y-%m-%d %H_%M_%S") # Makes date thingy
				newfile = dirname + str(now) + ".png"

				# Possible check if file already exists but I'm to lazy

				im.save(newfile) # Saves screenshot
				print("Image Saved to: " + dirname)
				startfile(newfile) # Opens file for user
				return

		if Pressed == True:
			posx = mouse.position[0]
			posy = mouse.position[1]
			if anchorx > posx:
				xa = posx
				xs = anchorx
			else:
				xa = anchorx
				xs = posx

			if anchory > posy:
				ya = posy
				ys = anchory
			else:
				ya = anchory
				ys = posy
			xsu = xs - xa
			ysu = ys - ya 
			root.geometry(str(xsu) + "x" + str(ysu) + "+" + str(xa) + "+" + str(ya))
		root.after(1, MainUpdate)
	root = Tk()


	root.attributes("-alpha", 0.25) # Set alpha of UI to 25%
	root.attributes("-fullscreen", True) # Set UI to fullscreen
	root.configure(bg="grey") # UI Background set to grey
	
	root.attributes('-topmost', True) # Make the UI overlay
	root.overrideredirect(True) # No topbar (This will disable your window to be closed by regular means)
	MainUpdate()  # Start MainUpdate
	root.mainloop() # Start Mainloop

def OpenFolder(systray):
	global dirname 
	startfile(dirname) # OpenFolder

def AskDir(systray):
	global dirname 
	Dir = Tk() # Set tkinter root
	Dir.withdraw() # IDK stackoverflow said some
	Dir.iconbitmap('KSrcIcon.ico') # Set icon
	tempdir = filedialog.askdirectory(initialdir=dirname,  title='Please select a directory') # Do some stuff
	if tempdir != "": # Check if nothing was done
		dirname = tempdir # They did something? Brilliant!
		dirname += "\\" # Add this cuz python don't like me
	print("Dir set to: " + dirname)
	with open("Dir_Save", "w+") as f: # Set the dir back to save file
		f.write(dirname)
	


# I don't really understand this. Just copied it from stackoverflow

def on_exit(systray):
	exit()

	

menu_options = (("Screenshot", None, Screenshot), ("Open Folder", None, OpenFolder), ("Set Directory", None, AskDir)) # Some systray stuff idk
systray = SysTrayIcon("KSrcIcon.ico", "KSrc", menu_options, on_quit=on_exit) # Even more systray stuff
systray.start() # Start them systray
