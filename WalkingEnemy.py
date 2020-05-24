from Enemy import *

class WalkingEnemy(Enemy):
    def __init__(self, pos):
        Enemy.__init__(self, pos,
                       "Models/SimpleEnemy/simpleEnemy",
                       {
                        "stand" : "Models/SimpleEnemy/simpleEnemy-stand",
                        "walk" : "Models/SimpleEnemy/simpleEnemy-walk",
                        "attack" : "Models/SimpleEnemy/simpleEnemy-attack",
                        "die" : "Models/SimpleEnemy/simpleEnemy-die",
                        "spawn" : "Models/SimpleEnemy/simpleEnemy-spawn"
                        },
                       3.0,
                       7.0,
                       "walkingEnemy")

        self.attackDistance = 0.75

        self.acceleration = 100.0

        # A reference vector, used to determine
        # which way to face the Actor.
        # Since the character faces along
        # the y-direction, we use the y-axis.
        self.yVector = Vec2(0, 1)

    def runLogic(self, player, dt):
        # In short: find the vector between
        # this enemy and the player.
        # If the enemy is far from the player,
        # use that vector to move towards the player.
        # Otherwise, just stop for now.
        # Finally, face the player.

        vectorToPlayer = player.actor.getPos() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        if distanceToPlayer > self.attackDistance*0.9:
            self.walking = True
            vectorToPlayer.setZ(0)
            vectorToPlayer.normalize()
            self.velocity += vectorToPlayer*self.acceleration*dt
        else:
            self.walking = False
            self.velocity.set(0, 0, 0)

        self.actor.setH(heading)