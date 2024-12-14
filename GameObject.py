import math
import random
import uuid
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT

class GameObject:

    def __init__(self, x, y, r, v=0, o=0):
        self.guid = uuid.uuid4()
        self.cX = x
        self.cY = y
        self.cR = r
        self.v = v
        self.o = math.radians(o)
        self.vy = math.cos(self.o) * self.v
        self.vx = math.sin(self.o) * self.v
        self.isPaused = False

    def getGUID(self):
        return self.guid

    def canFitInRect(self, quadNode):
        pass

    def checkForHorizontalWallCollision(self):
        pass

    def getCircle(self):
        return (self.cX, self.cY, self.cR)

    def checkForVerticalWallCollision(self):
        pass

    def update(self):
        pass

    def doesIntersect(self, rect):
        pass

    def pause(self):
        self.isPaused = True

    def offset(self, offsetVector):
        pass

    def updateVelocity(self, newVelocity):
        self.vx = newVelocity[0]
        self.vy = newVelocity[1]

    def updateVelocityAfterCollision(self, newVelocity):
        self.vx = newVelocity[0]
        self.vy = newVelocity[1]

class Circle(GameObject):
    def __init__(self, x, y, r, v=0, o=0):
        super().__init__(x, y, r, v, o)
        self.mass = 3 * math.pow(self.cR, 2)

    def checkForHorizontalWallCollision(self):
        if self.cY - self.cR <= 0 or self.cY + self.cR >= SCREEN_HEIGHT:
            self.vy = -(self.vy)

    def checkForVerticalWallCollision(self):
        if self.cX - self.cR <= 0 or self.cX + self.cR >= SCREEN_WIDTH:
            self.vx = -(self.vx)

    def canFitInRect(self, quadNode):
        x1 = quadNode.rectBound.getX()
        x2 = x1 + quadNode.rectBound.getWidth()
        y1 = quadNode.rectBound.getY()
        y2 = y1 + quadNode.rectBound.getHeight()

        cx1 = self.cX - self.cR
        cx2 = self.cX + self.cR
        cy1 = self.cY - self.cR
        cy2 = self.cY + self.cR

        if (x1 <= cx1 <= x2) and (x1 <= cx2 <= x2) and (y1 <= cy1 <= y2) and (y1 <= cy2 <= y2):
            return True
        return False

    def doesIntersect(self, quadNode):
        x1 = quadNode.rectBound.getX()
        x2 = x1 + quadNode.rectBound.getWidth()
        y1 = quadNode.rectBound.getY()
        y2 = y1 + quadNode.rectBound.getHeight()
        deltaX = self.cX - max(x1, min(self.cX, x2))
        deltaY = self.cY - max(y1, min(self.cY, y2))
        return (deltaX * deltaX + deltaY * deltaY) < (self.cR * self.cR)

    def update(self):
        if not self.isPaused:
            self.checkForVerticalWallCollision()
            self.checkForHorizontalWallCollision()

            self.cX += self.vx
            self.cY += self.vy

    def updateVelocityAfterCollision(self, newVelocity):
        self.vx = newVelocity[0]
        self.vy = newVelocity[1]
        self.cX += self.vx
        self.cY += self.vy

def getRandomCircle(circleList):
    newCircleFound = False
    x, y, r = 0, 0, 0
    while not newCircleFound:
        x = random.randint(10, SCREEN_WIDTH)
        y = random.randint(10, SCREEN_HEIGHT)
        r = 4
        if len(circleList) == 0:
            return Circle(x, y, r, random.uniform(0.5, 2), random.randint(10, 180))
        cnt = 0
        for existingCircle in circleList:
            distFromPrevCircle = int(math.hypot(existingCircle.cX - x, existingCircle.cY - y))
            if not distFromPrevCircle <= int(existingCircle.cX + r):
                cnt = cnt + 1
                break
        if cnt == 1:
            newCircleFound = True
    return Circle(x, y, r, random.uniform(0.5, 2), random.randint(10, 180))
