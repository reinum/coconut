from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs

import threading
import interception
import asyncio
import os

interception.auto_capture_devices()

conn = tosu.Tosu("ws://localhost:24050/websocket/v2")

def tap(key, holdtime):
    interception.key_down(key)
    asyncio.sleep(holdtime / 1000)  # Convert milliseconds to seconds
    interception.key_up(key)

async def relax(hitObjs, lastObject, K1, K2):
    currentTime = 0
    while currentTime < lastObject:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        for obj in hitObjs:
            x, y, objTime, objId, holdTime = obj
            timeDifference = objTime - currentTime
            if -10 <= timeDifference <= 10:  # 10ms tolerance:        
                print(f"Hit object at {x}, {y}", K1, K2)
                if objId == 0:  # Circle
                    threading.Thread(target=tap, args=(K1, holdTime)).start()
                elif objId == 1:  # Slider
                    pass
                elif objId == 2:  # Spinner
                    pass
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