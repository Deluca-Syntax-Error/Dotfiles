import datetime
import pyscreenshot

folder = "/home/fabri/Pictures/screenshot/"
image  = pyscreenshot.grab()
time   = datetime.datetime.now()
image.save(folder + str(time) + ".png")
