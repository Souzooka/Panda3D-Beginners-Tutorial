from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import WindowProperties
from panda3d.core import Vec4, Vec3
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerPusher
from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import CollisionTube
from Player import *
from WalkingEnemy import *

class Game(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		# Call various initialization methods on class
		self.windowInit(1280, 720)
		self.levelInit("Models/Environment/environment")
		self.lightingInit()
		self.playerInit()
		self.cameraInit(pos=Vec3(0, 0, 32), hpr=Vec3(0, -90, 0))
		self.inputInit()
		self.collisionInit()

		self.tempEnemy = WalkingEnemy(Vec3(5, 0, 0))

		# Set up a task that we'll run consistently
		self.updateTask = taskMgr.add(self.update, "update")

	def windowInit(self, h, w):
		properties = WindowProperties()
		properties.setSize(h, w)
		self.win.requestProperties(properties)

	def levelInit(self, levelname):
		# Load a backdrop model and attach it to the Scene Graph
		self.environment = loader.loadModel(levelname)
		self.environment.reparentTo(render)

		# Set up level collision
		self.cTrav = CollisionTraverser()
		self.pusher = CollisionHandlerPusher()


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
		self.player = Player()
		self.player.actor.reparentTo(render)

	def cameraInit(self, pos, hpr):
		self.camera.setPos(pos)
		self.camera.setHpr(hpr)

	def collisionInit(self):
		self.pusher.addCollider(self.player.collider, self.player.actor)
		self.cTrav.addCollider(self.player.collider, self.pusher)
		self.pusher.setHorizontal(True)

		wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
		wallNode = CollisionNode("wall")
		wallNode.addSolid(wallSolid)
		wall = render.attachNewNode(wallNode)
		wall.setY(8.0)

		wallSolid = CollisionTube(-8.0, 0, 0, 8.0, 0, 0, 0.2)
		wallNode = CollisionNode("wall")
		wallNode.addSolid(wallSolid)
		wall = render.attachNewNode(wallNode)
		wall.setY(-8.0)

		wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
		wallNode = CollisionNode("wall")
		wallNode.addSolid(wallSolid)
		wall = render.attachNewNode(wallNode)
		wall.setX(8.0)

		wallSolid = CollisionTube(0, -8.0, 0, 0, 8.0, 0, 0.2)
		wallNode = CollisionNode("wall")
		wallNode.addSolid(wallSolid)
		wall = render.attachNewNode(wallNode)
		wall.setX(-8.0)

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
		dt = globalClock.getDt()

		self.player.update(self.keyMap, dt)

		self.tempEnemy.update(self.player, dt)

		return task.cont

game = Game()
game.run()