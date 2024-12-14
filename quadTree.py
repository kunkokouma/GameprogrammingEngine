import math

from Constants import MAX_OBJECTS

class Bound():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

class QuadTree():

    def __init__(self, level, rectBound):
        self.level = level
        self.rectBound = rectBound
        self.objects = []
        self.nodes = [] 

    def clear(self):
        self.objects.clear()
        for node in self.nodes:
            node.clear()
        self.nodes.clear()

    def getGameObjects(self):
        return self.objects

    def getAllNodes(self, allNodes):
        allNodes.append(self.rectBound)
        if len(self.nodes) > 0:
            for node in self.nodes:
                node.getAllNodes(allNodes)
        return allNodes

    def splitNode(self):
        subWidth = int(self.rectBound.getWidth() / 2)
        subHeight = int(self.rectBound.getHeight() / 2)
        x = self.rectBound.getX()
        y = self.rectBound.getY()

        self.nodes.append(QuadTree(self.level + 1, Bound(x, y, subWidth, subHeight)))
        self.nodes.append(QuadTree(self.level + 1, Bound(x + subWidth, y, subWidth, subHeight)))
        self.nodes.append(QuadTree(self.level + 1, Bound(x + subWidth, y + subHeight, subWidth, subHeight)))
        self.nodes.append(QuadTree(self.level + 1, Bound(x, y + subHeight, subWidth, subHeight)))

    def getIndex(self, gameObject):
        if len(self.nodes) <= 0:
            return -1
        if gameObject.canFitInRect(self.nodes[0]):
            return 0
        elif gameObject.canFitInRect(self.nodes[1]):
            return 1
        elif gameObject.canFitInRect(self.nodes[2]):
            return 2
        elif gameObject.canFitInRect(self.nodes[3]):
            return 3
        else:
            return -1

    def insertObject(self, gameObject):
        if len(self.nodes) > 0:
            subNodeIndex = self.getIndex(gameObject)
            if subNodeIndex > -1:
                self.nodes[subNodeIndex].insertObject(gameObject)
                return
        self.objects.append(gameObject)

        if len(self.objects) > MAX_OBJECTS:
            if len(self.nodes) == 0:
                self.splitNode()
            newObjects = []
            for object in self.objects:
                subNodeIndex = self.getIndex(object)
                if subNodeIndex > -1:
                    self.nodes[subNodeIndex].insertObject(object)
                else:
                    newObjects.append(object)
            self.objects = newObjects

    def retrieveObjs(self, gameObject):
        subNodeIndex = self.getIndex(gameObject)
        returnList = []
        if subNodeIndex > -1:
            returnList.extend(self.objects)
            returnList.extend(self.nodes[subNodeIndex].retrieveObjs(gameObject))
        else:
            returnList.extend(self.objects)
            if len(self.nodes) > 0:
                for node in self.nodes:
                    if gameObject.doesIntersect(node):
                        returnList.extend(node.retrieveObjs(gameObject))
        return returnList

    def updateGameObjects(self):
        for gameObject in self.objects:
            gameObject.update()

    def handleCircleCollision(self, circleList):
        collidedTuples = []
        for gameObject in circleList:
            possibleHits = self.retrieveObjs(gameObject)
            for possibleHit in possibleHits:
                centerDis = math.fabs(math.sqrt(
                    math.pow(possibleHit.cX - gameObject.cX, 2) + math.pow(possibleHit.cY - gameObject.cY, 2)))
                radiusSum = possibleHit.cR + gameObject.cR

                if centerDis <= radiusSum \
                        and (possibleHit.getGUID(), gameObject.getGUID()) not in collidedTuples \
                        and possibleHit.getGUID() != gameObject.getGUID():
                    collidedTuples.append((gameObject.getGUID(), possibleHit.getGUID()))
                    vx1 = (possibleHit.vx * (possibleHit.mass - gameObject.mass) +
                           (2 * gameObject.mass * gameObject.vx)) / (possibleHit.mass + gameObject.mass)
                    vy1 = (possibleHit.vy * (possibleHit.mass - gameObject.mass) +
                           (2 * gameObject.mass * gameObject.vy)) / (possibleHit.mass + gameObject.mass)
                    vx2 = (gameObject.vx * (gameObject.mass - possibleHit.mass) +
                           (2 * possibleHit.mass * possibleHit.vx)) / (possibleHit.mass + gameObject.mass)
                    vy2 = (gameObject.vy * (gameObject.mass - possibleHit.mass) +
                           (2 * possibleHit.mass * possibleHit.vy)) / (possibleHit.mass + gameObject.mass)
                    gameObject.updateVelocityAfterCollision((vx2, vy2))
                    possibleHit.updateVelocityAfterCollision((vx1, vy1))
