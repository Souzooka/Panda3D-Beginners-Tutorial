from GameObject import *

class Player(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            Vec3(0, 0, 0),
                            "Models/PandaChan/act_p3d_chan",
                              {
                                  "stand" : "Models/PandaChan/a_p3d_chan_idle",
                                  "walk" : "Models/PandaChan/a_p3d_chan_run"
                              },
                            5,
                            10,
                            "player")

        # Panda-chan faces "backwards", so we just turn
        # the first sub-node of our Actor-NodePath
        # to have it face as we want.
        self.actor.getChild(0).setH(180)

        # Since our "Game" object is the "ShowBase" object,
        # we can access it via the global "base" variable.
        base.pusher.addCollider(self.collider, self.actor)
        base.cTrav.addCollider(self.collider, base.pusher)

        self.actor.loop("stand")

    def update(self, keys, dt):
        GameObject.update(self, dt)

        self.walking = False

        # If we're  pushing a movement key, add a relevant amount
        # to our velocity.
        if keys["up"]:
            self.walking = True
            self.velocity.addY(self.acceleration*dt)
        if keys["down"]:
            self.walking = True
            self.velocity.addY(-self.acceleration*dt)
        if keys["left"]:
            self.walking = True
            self.velocity.addX(-self.acceleration*dt)
        if keys["right"]:
            self.walking = True
            self.velocity.addX(self.acceleration*dt)

        # Run the appropriate animation for our current state.
        # See the text below this for an explanation
        if self.walking:
            standControl = self.actor.getAnimControl("stand")
            if standControl.isPlaying():
                standControl.stop()

            walkControl = self.actor.getAnimControl("walk")
            if not walkControl.isPlaying():
                self.actor.loop("walk")
        else:
            standControl = self.actor.getAnimControl("stand")
            if not standControl.isPlaying():
                self.actor.stop("walk")
                self.actor.loop("stand")