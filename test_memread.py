from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs
import asyncio

conn = tosu.Tosu("ws://localhost:24050/websocket/v2")

async def relax(hitObjs, totalMapLength):
    print("wowowowo")
    

async def waitForMap():
    await conn.connectAll()
    while True:
        state = await conn.Connection.getState()
        if state == tosu_classes.OsuState.Game:
            directPath = await conn.Connection.getPaths()
            hitObjects = hitobjs.find_hitobject(map)
            await relax(hitObjects)

asyncio.run(waitForMap())