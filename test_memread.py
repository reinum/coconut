from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs

import threading
import interception
import asyncio
import os
import time

interception.auto_capture_devices()

conn = tosu.Tosu("ws://localhost:24050/websocket/v2")

def tap(key, holdtime):
    interception.key_down(key)
    time.sleep(holdtime / 1000)  # Convert milliseconds to seconds
    interception.key_up(key)

async def relax(hitObjs, firstObject, lastObject, K1, K2):
    currentTime = 0
    processedObjects = set()  # Keep track of processed hit objects
    keyToTapWith = K1

    while currentTime < 100:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()

    while currentTime < lastObject:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        for obj in hitObjs:
            x, y, objTime, objId, holdTime = obj

            # Skip already processed objects
            if objTime in processedObjects:
                continue

            timeDifference = objTime - currentTime
            if -10 <= timeDifference <= 10:  # 10ms tolerance
                print(f"Hit object at {x}, {y}, holdtime: {holdTime}, time difference: {timeDifference}")
                threading.Thread(target=tap, args=(keyToTapWith, holdTime)).start()
                processedObjects.add(objTime)  # Mark this object as processed
                keyToTapWith = K1 if keyToTapWith == K2 else K2
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
    beatmapTime = await conn.Connection.getBeatmapTime()
    osuKeys = (await conn.Connection.getKeybinds()).osu
    K1 = osuKeys.k1
    K2 = osuKeys.k2
    hitObjects = hitobjs.findHitObject(beatmap, beatmapTime.lastObject)

    await asyncio.sleep(2)  # Give some time for the game to load the map

    await relax(hitObjects, beatmapTime.firstObject, beatmapTime.lastObject, K1, K2)


asyncio.run(waitForMap())