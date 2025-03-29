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

async def relax(hitObjs, firstObject, lastObject, K1, K2, mod=None):
    currentTime = 0
    processedObjects = set()  # Keep track of processed hit objects
    keyToTapWith = K1
    realIndex = 0

    print(currentTime, lastObject)
    # Start processing hit objects
    while currentTime < lastObject:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        for index, obj in enumerate(hitObjs):  # Use enumerate to get the index
            x, y, objTime, objId, holdTime = obj

            if index > realIndex+1 or objTime in processedObjects:
                continue

            timeDifference = objTime - currentTime
            if -10 <= timeDifference <= 10:  # 10ms tolerance
                # print(f"Processing object at index {index}: ({x}, {y}), holdtime: {holdTime}, time difference: {timeDifference}")
                threading.Thread(target=tap, args=(keyToTapWith, holdTime)).start()
                processedObjects.add(objTime)  # Mark this object as processed
                keyToTapWith = K1 if keyToTapWith == K2 else K2
                realIndex += 1
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

    mods = await conn.Connection.getPlay()
    currentMod = mods.mods.name
    await relax(hitObjects, beatmapTime.firstObject, beatmapTime.lastObject, K1, K2, currentMod)


asyncio.run(waitForMap())
