from ../tosu import tosu_classes
from ../tosu import tosu_connection as tosu
from parsers import hitobjs
import os
import asyncio
from interception import beziercurve,move_to
import math
import win32gui
class Aimbot:
    def __init__(self,url):
        self.connections = tosu.Tosu(url)
        self.connections.connectAll()
        self.firstObject = 0
        self.lastObject = 0
        self.hitObjects = []
        self.mod = None
        self.curve_params = beziercurve.BezierCurveParams()
        self.resolution = (0,0)

    def adjustHitObjects(self):
        # Adjust hit object timings based on the mod
        if "DT" in self.mod or "NC" in self.mod:  # Double Time
            speedMultiplier = 1 / 1.5
        elif self.mod == "HT":  # Half Time
            speedMultiplier = 1 / 0.75
        else:  # No mod
            speedMultiplier = 1.0

        # Apply the speed multiplier to all hit objects
        hitobjects = []
        for obj in self.hitObjects:
            obj[2] = int(obj[2] * speedMultiplier)  # Adjust objTime
            obj[4] = int(obj[4] * speedMultiplier)  # Adjust holdTime
            hitobjects.append(obj)

        self.hitObjects = hitobjects
        # Adjust first and last object times
        self.firstObject = int(self.firstObject * speedMultiplier)
        self.lastObject = int(self.lastObject * speedMultiplier)
    async def aimbot(self):
        # Wait for the game to start
        await self.WaitForMap()
        # Get the current time from the precise connection
        time = await self.connections.PreciseConnection.preciseCurrentTime()
        # Adjust hit objects based on the mod
        self.adjustHitObjects()

        resolution = (await self.connections.Connection.getResolution())
        self.resolution = resolution.width, resolution.height
        # get the window position
        


        # Wait until the game time is synchronized
        while currentTime < self.firstObject - 100:  # Wait until we're close to the first object
            currentTime = await self.connections.PreciseConnection.preciseCurrentTime()
            await asyncio.sleep(0.01)

        # get the position of the current hit object
        reversedhitObjects = self.hitObjects.copy()
        reversedhitObjects.reverse()
        for obj in reversedhitObjects:
            x, y, objTime, objId, holdTime = obj
            # Check if the object is within the current time
            if objTime <= time:
                # If the object is a circle or slider, break the loop
                if objId == 0 or objId == 1:
                    currentObject = obj
                    break
                # If the object is a spinner, continue to the next object
                elif objId == 2:
                    continue
        # get the position of the next hit object
        for obj in self.hitObjects:
            x, y, objTime, objId, holdTime = obj
            # Check if the object is within the current time
            if objTime > time:
                # If the object is a circle or slider, break the loop
                if objId == 0 or objId == 1:
                    nextObject = obj
                    break
                # If the object is a spinner, continue to the next object
                elif objId == 2:
                    continue
            
        # Calculate the time until the next hit object
        timeUntilNextHitObject = nextObject[2] - time

        nextX,nextY = nextObject[0],nextObject[1]

        #get the position of the next next hit object
        for obj in self.hitObjects:
            x, y, objTime, objId, holdTime = obj
            # Check if the object is within the current time
            if objTime > nextObject[2]:
                # If the object is a circle or slider, break the loop
                if objId == 0 or objId == 1:
                    nextNextObject = obj
                    break
                # If the object is a spinner, continue to the next object
                elif objId == 2:
                    continue
        
        # calculate angle next to the next hit object between the current hit object and the next next hit object using the law of cosines
        angle = math.atan2(nextNextObject[1] - currentObject[1], nextNextObject[0] - currentObject[0]) * 180 / math.pi
        # calculate distance between the current hit object and the next hit object
        distance = math.sqrt((nextX - currentObject[0]) ** 2 + (nextY - currentObject[1]) ** 2)
        # calculate distance between the current hit object and the next next hit object
        distanceNext = math.sqrt((nextNextObject[0] - currentObject[0]) ** 2 + (nextNextObject[1] - currentObject[1]) ** 2)
        
        # if the angle is sharp move directly, if not move in a curve
        if abs(angle) > 45:
            # move directly to the next hit object
            self.curve_params.setCurveParams(currentObject[0], currentObject[1], nextX, nextY, timeUntilNextHitObject, self.resolution)
            
        else:
            # move in a curve to the next hit object
            self.curve_params.setCurveParams(currentObject[0], currentObject[1], nextX, nextY, timeUntilNextHitObject, self.resolution)
            
        
        # get the osu window position using win32gui
        osu_window = win32gui.FindWindow(None, "osu!")
        if osu_window:
            # get the window position
            rect = win32gui.GetWindowRect(osu_window)
            x, y, width, height = rect
        
        # move to the next hit object using the bezier curve
        move_to(nextX + x, nextY + y, self.curve_params, timeUntilNextHitObject)
        # wait for the hit object to be hit
        await asyncio.sleep(0.01)

    async def WaitForMap(self):
        state = await self.connections.Connection.getState()
        while state != tosu_classes.OsuState.Game:
            print(f"Current state: {state}")
            folder = (await self.connections.Connection.getFolders()).songFolder
            beatmap = (await self.connections.Connection.getPaths()).beatmapFile
            time = (await self.connections.Connection.getBeatmapTime())
            self.firstObject = time.firstObject
            self.lastObject = time.lastObject
            self.hitobjects = hitobjs.findHitObject(os.path.join(folder, beatmap), time.lastObject)
            await self.connections.Connection.getState()
        

    

    



