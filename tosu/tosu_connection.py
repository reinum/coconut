import websockets
import json
from tosu import tosu_classes

class Tosu:
    def __init__(self, baseUrl):
        self.Connection = TosuConnection(baseUrl)
        self.PreciseConnection = TosuConnection(baseUrl + "/precise")
    
    async def connectAll(self):
        await self.Connection.connect()
        await self.PreciseConnection.connect()

    async def closeAll(self):
        await self.Connection.close()
        await self.PreciseConnection.close()


class TosuConnection:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.data = None
        self.isPrecise = self.uri.endswith("precise")

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            print(f"Connected to {self.uri}")
        except Exception as e:
            print(f"Failed to connect: {e}")
            raise e

    async def getState(self):
        self.data = await self.websocket.recv()
        if self.isPrecise:
            raise ValueError("Cannot get state from precise connection.")
        if not self.data:
            raise ValueError("No data received yet.")
        jsondata = json.loads(self.data)
        state = jsondata["state"]["number"]
        if state == 0:
            return tosu_classes.OsuState.Menu
        elif state == 2:
            return tosu_classes.OsuState.Game
        elif state == 5:
            return tosu_classes.OsuState.SongSelect
        else:
            raise ValueError(f"Unknown state: {state}")
        
    async def preciseCurrentTime(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if not self.isPrecise:
            raise ValueError("Cannot get precise time from non-precise connection.")
        jsondata = json.loads(self.data)
        return jsondata["currentTime"]


    async def getResolution(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get resolution from precise connection.")
        jsondata = json.loads(self.data)
        resolution = jsondata["resolution"]
        return tosu_classes.Resolution(
            fullscreen=resolution["fullscreen"],
            width=resolution["width"],
            height=resolution["height"],
            fullscreenWidth=resolution["widthFullscreen"],
            fullscreenHeight=resolution["heightFullscreen"],
        )

    async def getMouse(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get mouse settings from precise connection.")
        jsondata = json.loads(self.data)
        mouse = jsondata["mouse"]
        return tosu_classes.Mouse(
            rawInput=mouse["rawInput"],
            disableButtons=mouse["disableButtons"],
            disableWheel=mouse["disableWheel"],
            sensitivity=mouse["sensitivity"],
        )

    async def getAudio(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get audio settings from precise connection.")
        jsondata = json.loads(self.data)
        audio = jsondata["audio"]
        volume = audio["volume"]
        return tosu_classes.Audio(
            ignoreBeatmapSounds=audio["ignoreBeatmapSounds"],
            useSkinSamples=audio["useSkinSamples"],
            volume=tosu_classes.Audio.Volume(
                master=volume["master"],
                music=volume["music"],
                effect=volume["effect"]
            ),
            universalOffset=audio["universalOffset"]
        )
    async def getKeybinds(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get keybinds from precise connection.")
        jsondata = json.loads(self.data)
        keybinds = jsondata["keybinds"]
        osu = keybinds["osu"]
        fruits = keybinds["fruits"]
        taiko = keybinds["taiko"]
        quickRetry = keybinds["quickRetry"]
        return tosu_classes.Keybinds(
            osu=tosu_classes.OsuKeybinds(
                k1=osu["k1"],
                k2=osu["k2"],
                smokeKey=osu["smokeKey"]
            ),
            fruits=tosu_classes.FruitsKeybinds(
                k1=fruits["k1"],
                k2=fruits["k2"],
                Dash=fruits["Dash"]
            ),
            taiko=tosu_classes.TaikoKeybinds(
                innerLeft=taiko["innerLeft"],
                innerRight=taiko["innerRight"],
                outerLeft=taiko["outerLeft"],
                outerRight=taiko["outerRight"]
            ),
            quickRetry=quickRetry
        )

    async def getProfile(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get profile from precise connection.")
        jsondata = json.loads(self.data)
        profile = jsondata["profile"]
        status = profile["status"]
        mode = profile["mode"]
        countryCode = profile["countryCode"]
        return tosu_classes.Profile(
            status=tosu_classes.Profile.Status(
                number=status["number"],
                name=status["name"]
            ),
            mode=tosu_classes.Profile.Mode(
                number=mode["number"],
                name=mode["name"]
            ),
            countryCode=tosu_classes.Profile.CountryCode(
                code=countryCode["code"],
                name=countryCode["name"]
            ),
            id=profile["id"],
            name=profile["name"],
            rankedScore=profile["rankedScore"],
            level=profile["level"],
            accuracy=profile["accuracy"],
            pp=profile["pp"],
            playCount=profile["playCount"],
            globalRank=profile["globalRank"],
            backgroundColour=profile["backgroundColour"],
        )

    async def getPaths(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get paths from precise connection.")
        jsondata = json.loads(self.data)
        paths = jsondata["directPath"]
        return tosu_classes.DirectPath(
            beatmapFile=paths["beatmapFile"],
            beatmapBackground=paths["beatmapBackground"],
            beatmapAudio=paths["beatmapAudio"],
            beatmapFolder=paths["beatmapFolder"],
            skinFolder=paths["skinFolder"]
        )
    async def getFolders(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get folders from precise connection.")
        jsondata = json.loads(self.data)
        folders = jsondata["folders"]
        return tosu_classes.Folders(
            gameFolder=folders["game"],
            skin=folders["skin"],
            songFolder=folders["songs"],
            beatmap=folders["beatmap"]
        )
    async def getBeatmapTime(self):
        self.data = await self.websocket.recv()
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get beatmap time from precise connection.")
        jsondata = json.loads(self.data)
        return tosu_classes.BeatmapTime(
            live=jsondata["beatmap"]["time"]["live"],
            firstObject=jsondata["beatmap"]["time"]["firstObject"],
            lastObject=jsondata["beatmap"]["time"]["lastObject"]
        )
    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("Connection closed")
        else:
            print("No active connection to close")