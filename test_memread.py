from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs

import asyncio
import os

conn = tosu.Tosu("ws://localhost:24050/websocket/v2")

async def relax(hitObjs, lastObject):
    currentTime = 0
    while currentTime < lastObject:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        for obj in hitObjs:
            if obj[2] <= currentTime <= obj[2] + obj[4]:
                print(f"Hit object at {obj[0]}, {obj[1]}")
                break

async def waitForMap():
    await conn.connectAll()

    # Get the game folder
    folders = await conn.Connection.getFolders()

    state = await conn.Connection.getState()
    while state != tosu_classes.OsuState.Game:
        state = await conn.Connection.getState()
    # Get the current map
    directPath = await conn.Connection.getPaths()
    beatmap = os.path.join(folders.songFolder, directPath.beatmapFile)

    # Parse needed data from the beatmap
    hitObjects = hitobjs.findHitObject(beatmap)
    beatmapTime = await conn.Connection.getBeatmapTime()

    await relax(hitObjects, beatmapTime.lastObject)


asyncio.run(waitForMap())