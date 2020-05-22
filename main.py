from direct.actor.Actor import Actor
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

		# Load a backdrop model and attach it to the Scene Graph
		self.environment = loader.loadModel("Models/Misc/environment")
		self.environment.reparentTo(render)

		# Load an animated model
		self.tempActor = Actor("Models/PandaChan/act_p3d_chan", {"walk" : "Models/PandaChan/a_p3d_chan_run"})
		self.tempActor.reparentTo(render)

		# Move the actor to a position where it is visible by the default camera
		self.tempActor.setPos(0, 7, 0)

		# Rotate the actor's orientation (heading) from 0 to 180 (now facing away from camera)
		self.tempActor.getChild(0).setH(180)

		# Set an animation for the actor
		self.tempActor.loop("walk")

		# Rotate the camera so now the scene is in a top-down perspective
		self.camera.setPos(0, 0, 32) # 32 units above origin
		self.camera.setP(-90) # Camera facing down


game = Game()
game.run()