from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs

import asyncio
import os

conn = tosu.Tosu("ws://localhost:24050/websocket/v2")

async def relax(hitObjs, totalMapLength):
    print("wowowowo")
    

async def waitForMap():
    await conn.connectAll()

    # Get the game folder
    folders = await conn.Connection.getFolders()

    while True:
        state = await conn.Connection.getState()
        if state == tosu_classes.OsuState.Game:
            # Get the current map
            directPath = await conn.Connection.getPaths()
            beatmap = os.path.join(folders.songFolder, directPath.beatmapFile)

            # Get the game folder
            hitObjects = hitobjs.findHitObject(beatmap)
            await relax(hitObjects, 1)

asyncio.run(waitForMap())