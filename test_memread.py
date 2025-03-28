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

    # Adjust hit object timings based on the mod
    if "DT" in mod or "NC" in mod:  # Double Time
        speedMultiplier = 1 / 1.5
    elif mod == "HT":  # Half Time
        speedMultiplier = 1 / 0.75
    else:  # No mod
        speedMultiplier = 1.0

    # Apply the speed multiplier to all hit objects
    for obj in hitObjs:
        obj[2] = int(obj[2] * speedMultiplier)  # Adjust objTime
        obj[4] = int(obj[4] * speedMultiplier)  # Adjust holdTime

    # Adjust first and last object times
    firstObject = int(firstObject * speedMultiplier)
    lastObject = int(lastObject * speedMultiplier)

    # Wait until the game time is synchronized
    while currentTime < firstObject - 100:  # Wait until we're close to the first object
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        await asyncio.sleep(0.01)

    # Start processing hit objects
    while currentTime < lastObject:
        currentTime = await conn.PreciseConnection.preciseCurrentTime()
        for index, obj in enumerate(hitObjs):  # Use enumerate to get the index
            x, y, objTime, objId, holdTime = obj

            if index > realIndex + 1:
                continue

            # Skip already processed objects
            if objTime in processedObjects:
                continue

            timeDifference = objTime - currentTime
            if -10 <= timeDifference <= 10:  # 10ms tolerance
                print(f"Processing object at index {index}: ({x}, {y}), holdtime: {holdTime}, time difference: {timeDifference}")
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
    currentMod = mods.Mods.name

    await asyncio.sleep(2)  # Give some time for the game to load the map

    await relax(hitObjects, beatmapTime.firstObject, beatmapTime.lastObject, K1, K2, currentMod)


asyncio.run(waitForMap())