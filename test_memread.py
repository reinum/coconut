from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs
import asyncio

conn = tosu.Tosu("https://localhost:20450/websocket/v2")

async def relax(hit_objs, totalMapLength):
    print("wowowowo")
    

async def wait_for_map():
    await conn.connectAll()
    while True:
        state = await conn.Connection.getState()
        if state == tosu_classes.OsuState.Game:
            map = await conn.Connection.getPaths()
            hit_objs = hitobjs.find_hitobject(map)
            await relax(hit_objs)

asyncio.run(wait_for_map())