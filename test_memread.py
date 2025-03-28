from tosu import tosu_connection as tosu
from tosu import tosu_classes
from parsers import hitobjs

conn = tosu.Tosu("https://localhost:20450/websocket/v2")
conn.connect()

async def relax(hit_objs, totalMapLength):
    print("wowowowo")
    

async def wait_for_map():
    while True:
        state = conn.Connection.getState()
        if state == tosu_classes.OsuState.Game:
            map = conn.Connection.getPaths()
            hit_objs = hitobjs.find_hitobject(map)
            await relax(hit_objs)