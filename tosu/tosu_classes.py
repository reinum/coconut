from dataclasses import dataclass, field

@dataclass
class OsuState:
    # todo: add more lmao
    Menu: int = 0
    Game: int = 2
    SongSelect: int = 5

@dataclass
class Resolution:
    fullscreen: bool = False
    width: int = 1920
    height: int = 1080
    fullscreenWidth: int = 1920
    fullscreenHeight: int = 1080

@dataclass
class Mouse:
    rawInput: bool = False
    disableButtons: bool = False
    disableWheel: bool = False
    sensitivity: float = 1.0

@dataclass  
class Audio:
    ignoreBeatmapSounds: bool = False
    useSkinSamples: bool = False
    @dataclass
    class Volume:
        master: float = 1.0
        music: float = 1.0
        effect: float = 1.0
    volume: Volume = field(default_factory=Volume)
    universalOffset: float = 0.0

@dataclass
class Keybinds:
    @dataclass
    class Osu:
        k1: str 
        k2: str 
        smokeKey: str 

    @dataclass
    class Fruits:
        k1: str 
        k2: str 
        Dash: str 

    @dataclass
    class Taiko:
        innerLeft: str 
        innerRight: str 
        outerLeft: str 
        outerRight: str 

    osu: Osu = field(default_factory=Osu)
    fruits: Fruits = field(default_factory=Fruits)
    taiko: Taiko = field(default_factory=Taiko)
    quickRetry: str = "L"

@dataclass
class Profile:
    @dataclass
    class Status:
        number: int
        name: str

    @dataclass
    class Mode:
        number: int
        name: str

    @dataclass
    class CountryCode:
        number: int
        name: str

    userStatus: Status
    banchoStatus: Status
    id: int
    name: str
    mode: Mode
    rankedScore: int
    level: float
    accuracy: float
    pp: int
    playCount: int
    globalRank: int
    countryCode: CountryCode
    backgroundColour: str

@dataclass
class DirectPath:
    beatmapFile: str
    beatmapBackground: str
    beatmapAudio: str
    beatmapFolder: str
    skinFolder: str

@dataclass
class Folders:
    gameFolder: str
    skin: str
    songFolder: str
    beatmap: str

@dataclass
class BeatmapTime:
    live: int
    firstObject: int
    lastObject: int

@dataclass
class Play:
    @dataclass
    class Mode:
        number: int
        name: str

    @dataclass
    class Mods:
        number: int
        name: str