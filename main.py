from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

class Game(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		# Set the window size to 1280x720
		properties = WindowProperties()
		properties.setSize(1280, 720)
		self.win.requestProperties(properties)

		# Disable the default camera control
		self.disableMouse()

game = Game()
game.run()