from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import WindowProperties
from panda3d.core import Vec4, Vec3

class Game(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		# Call various initialization methods on class
		self.windowInit(1280, 720)
		self.levelInit("Models/Misc/environment")
		self.lightingInit()
		self.playerInit()
		self.cameraInit(pos=Vec3(0, 0, 32), hpr=Vec3(0, -90, 0))
		self.inputInit()

		# Set up a task that we'll run consistently
		self.updateTask = taskMgr.add(self.update, "update")

	def windowInit(self, h, w):
		# Set the window size to 1280x720
		properties = WindowProperties()
		properties.setSize(h, w)
		self.win.requestProperties(properties)

	def levelInit(self, levelname):
		# Load a backdrop model and attach it to the Scene Graph
		self.environment = loader.loadModel(levelname)
		self.environment.reparentTo(render)

	def lightingInit(self):
		# Kind of dark with just an ambient light, maybe a directional light eh
		mainLight = DirectionalLight("main light")
		self.mainLightNodePath = render.attachNewNode(mainLight)
		self.mainLightNodePath.setHpr(45, -45, 0)
		render.setLight(self.mainLightNodePath)

		# hook us up some automatic perpixel lighting
		render.setShaderAuto()

	def playerInit(self):
		# Initialize and render player character
		self.player = Character()
		self.player.reparentTo(render)

		# Set an animation for the actor
		self.player.loop("walk")

	def cameraInit(self, pos, hpr):
		self.camera.setPos(pos)
		self.camera.setHpr(hpr)

	def inputInit(self):
		# Input states
		self.keyMap = {
			"up" : False,
			"down" : False,
			"left" : False,
			"right" : False,
			"shoot" : False
		}

		# Disable the default camera control
		self.disableMouse()

		# Set up events to call self.updateKeyMap with args when certain keys are pressed or released
		self.accept("w", self.updateKeyMap, ["up", True])
		self.accept("w-up", self.updateKeyMap, ["up", False])
		self.accept("s", self.updateKeyMap, ["down", True])
		self.accept("s-up", self.updateKeyMap, ["down", False])
		self.accept("a", self.updateKeyMap, ["left", True])
		self.accept("a-up", self.updateKeyMap, ["left", False])
		self.accept("d", self.updateKeyMap, ["right", True])
		self.accept("d-up", self.updateKeyMap, ["right", False])
		self.accept("mouse1", self.updateKeyMap, ["shoot", True])
		self.accept("mouse1-up", self.updateKeyMap, ["shoot", False])

	# keyMap setter
	def updateKeyMap(self, controlName, controlState):
		self.keyMap[controlName] = controlState

	# Main game logic we have running every frame
	def update(self, task):
		# Get the amount of time since the last update
		dt = globalClock.getDt()

		if self.keyMap["up"]:
			self.player.move(Vec3(0, 1.0*dt, 0))
		if self.keyMap["down"]:
			self.player.move(Vec3(0, -1.0*dt, 0))
		if self.keyMap["left"]:
			self.player.move(Vec3(-1.0*dt, 0, 0))
		if self.keyMap["right"]:
			self.player.move(Vec3(1.0*dt, 0, 0))
		if self.keyMap["shoot"]:
			print ("Zap!")

		return task.cont

class Character(Actor):
	def __init__(self):
		Actor.__init__(self, "Models/PandaChan/act_p3d_chan", {"walk" : "Models/PandaChan/a_p3d_chan_run"})

		# Var for actor speed
		self.characterMovementSpeed = 5.0

	def move(self, delta):
		self.setPos(self.getPos() + delta * self.characterMovementSpeed)


game = Game()
game.run()