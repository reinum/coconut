from dataclasses import dataclass, field

@dataclass
class OsuState:
    # todo: add more lmao
    Menu: int = 0
    Game: int = 2

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
        k1: str = "O"
        k2: str = "P"
        smokeKey: str = "S"

    @dataclass
    class Fruits:
        k1: str = "Left"
        k2: str = "Right"
        Dash: str = "LeftShift"

    @dataclass
    class Taiko:
        innerLeft: str = "X"
        innerRight: str = "C"
        outerLeft: str = "Z"
        outerRight: str = "V"

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

