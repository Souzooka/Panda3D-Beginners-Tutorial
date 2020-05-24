from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import WindowProperties
from panda3d.core import Vec4

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

		# Load in some lights to spice things up
		# ambientLight = AmbientLight("ambient light")
		# ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
		# self.ambientLightNodePath = render.attachNewNode(ambientLight)
		# render.setLight(self.ambientLightNodePath)

		# Kind of dark with just an ambient light, maybe a directional light eh
		mainLight = DirectionalLight("main light")
		self.mainLightNodePath = render.attachNewNode(mainLight)
		self.mainLightNodePath.setHpr(45, -45, 0)
		render.setLight(self.mainLightNodePath)

		# hook us up some automatic perpixel lighting
		render.setShaderAuto()

		# Load an animated model
		self.tempActor = Actor("Models/PandaChan/act_p3d_chan", {"walk" : "Models/PandaChan/a_p3d_chan_run"})
		self.tempActor.reparentTo(render)

		# Set an animation for the actor
		self.tempActor.loop("walk")

		# Rotate the camera so now the scene is in a top-down perspective
		self.camera.setPos(0, 0, 32) # 32 units above origin
		self.camera.setP(-90) # Camera facing down


game = Game()
game.run()