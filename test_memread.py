from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs

import interception
import asyncio
import os

interception.auto_capture_devices()

conn = tosu.Tosu("ws://localhost:24050/websocket/v2")

async def relax(hitObjs, lastObject, K1, K2):
    currentTime = 0
    while currentTime < lastObject:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        for obj in hitObjs:
            x, y, objTime, objId, holdTime = obj
            if (objTime - currentTime) < -10 and (currentTime - objTime) > 10:  # 10ms tolerance:        
                print(f"Hit object at {x}, {y}")
                if objId == 0:  # Circle
                    interception.press(K1)
                    await asyncio.sleep(holdTime / 1000)
                    interception.release(K1)
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
    osuKeys = (await conn.Connection.getKeybinds()).Osu
    K1 = osuKeys.k1
    K2 = osuKeys.k2

    await relax(hitObjects, beatmapTime.lastObject, K1, K2)


asyncio.run(waitForMap())