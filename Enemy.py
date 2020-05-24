from GameObject import *

class Enemy(GameObject):
    def __init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName):
        GameObject.__init__(self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName)

        # This is the number of points to award
        # if the enemy is killed.
        self.scoreValue = 1

    def update(self, player, dt):
        # In short, update as a GameObject, then
        # run whatever enemy-specific logic is to be done.
        # The use of a separate "runLogic" method
        # allows us to customise that specific logic
        # to the enemy, without re-writing the rest.

        GameObject.update(self, dt)

        self.runLogic(player, dt)

        # As with the player, play the appropriate animation.
        if self.walking:
            walkingControl = self.actor.getAnimControl("walk")
            if not walkingControl.isPlaying():
                self.actor.loop("walk")
        else:
            spawnControl = self.actor.getAnimControl("spawn")
            if spawnControl is None or not spawnControl.isPlaying():
                attackControl = self.actor.getAnimControl("attack")
                if attackControl is None or not attackControl.isPlaying():
                    standControl = self.actor.getAnimControl("stand")
                    if not standControl.isPlaying():
                        self.actor.loop("stand")


    def runLogic(self, player, dt):
        pass