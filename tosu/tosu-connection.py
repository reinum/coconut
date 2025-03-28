import websockets
import json
from tosu import tosu_classes

class Tosu:
    def __init__(self, baseUrl):
        self.Connection = TosuConnection(baseUrl)
        self.PreciseConnection = TosuConnection(baseUrl + "/precise")
    
    def closeAll(self):
        self.Connection.close()
        self.PreciseConnection.close()


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
        while True:
            self.data = await self.websocket.recv()
            print(f"Received: {self.data}")

    async def getState(self):
        if self.isPrecise:
            raise ValueError("Cannot get state from precise connection.")
        if not self.data:
            raise ValueError("No data received yet.")
        json = json.loads(self.data)
        state = json["state"]["number"]
        if state == 0:
            return tosu_classes.OsuState.Menu
        elif state == 2:
            return tosu_classes.OsuState.Game
        else:
            raise ValueError(f"Unknown state: {state}")
        
    async def preciseCurrentTime(self):
        if not self.data:
            raise ValueError("No data received yet.")
        if not self.isPrecise:
            raise ValueError("Cannot get precise time from non-precise connection.")
        json = json.loads(self.data)
        return json["currentTime"]


    async def getResolution(self):
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get resolution from precise connection.")
        json = json.loads(self.data)
        resolution = json["resolution"]
        return tosu_classes.Resolution(
            fullscreen=resolution["fullscreen"],
            width=resolution["width"],
            height=resolution["height"],
            fullscreenWidth=resolution["widthFullscreen"],
            fullscreenHeight=resolution["heightFullscreen"],
        )

    async def getMouse(self):
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get mouse settings from precise connection.")
        json = json.loads(self.data)
        mouse = json["mouse"]
        return tosu_classes.Mouse(
            rawInput=mouse["rawInput"],
            disableButtons=mouse["disableButtons"],
            disableWheel=mouse["disableWheel"],
            sensitivity=mouse["sensitivity"],
        )

    async def getAudio(self):
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get audio settings from precise connection.")
        json = json.loads(self.data)
        audio = json["audio"]
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
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get keybinds from precise connection.")
        json = json.loads(self.data)
        keybinds = json["keybinds"]
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
        if not self.data:
            raise ValueError("No data received yet.")
        if self.isPrecise:
            raise ValueError("Cannot get profile from precise connection.")
        json = json.loads(self.data)
        profile = json["profile"]
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



    async def close(self):
        if self.websocket:
            await self.websocket.close()
            print("Connection closed")
        else:
            print("No active connection to close")