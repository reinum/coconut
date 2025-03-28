## osu memory offsets

class StableMemory:
    def __init__(self):
        self.scan_patterns = {
            "baseAddr": {
                "pattern": rb"\xF8\x01\x74\x04\x83\x65"
                
            },
            "playTimeAddr": {
                "pattern": rb"\x5E\x5F\x5D\xC3\xA1....\x89.\x04"
                
            },
            "chatCheckerPtr": {
                "pattern": rb"\x8B\xCE\x83\x3D\....\x00\x75.\x80",
                
                "offset": 0x4
            },
            "skinDataAddr": {
                "pattern": rb"\x74\x2C\x85\xFF\x75\x28\xA1....\x8D\x15"
                
            },
            "settingsClassAddr": {
                "pattern": rb"\x83\xE0\x20\x85\xC0\x7E\x2F",
                
            },
            "configurationAddr": {
                "pattern": rb"\x8D\x45\xEC\x50\x8B\x0D\....\x8B\xD7\x39\x09\xE8....\x85\xC0\x74.\x8B\x4D\xEC",
                
                "offset": 0x6
            },
            "bindingsAddr": {
                "pattern": rb"\x8D\x7D\xD0\xB9\x08\x00\x00\x00\x33\xC0\xF3\xAB\x8B\xCE\x89\x4D\xDC\xB9",
                
                "offset": 0x2a
            },
            "rulesetsAddr": {
                "pattern": rb"\x7D\x15\xA1\....\x85\xC0",
                
            },
            "canRunSlowlyAddr": {
                "pattern": rb"\x55\x8B\xEC\x80\x3D\....\x00\x75\x26\x80\x3D",
                
            },
            "statusPtr": {
                "pattern": rb"\x48\x83\xF8\x04\x73\x1E",
                "offset": -0x4
            },
            "menuModsPtr": {
                "pattern": rb"\xC8\xFF.....\x81\x0D\.....\x08\x00\x00",
                "offset": 0x9
            },
            "getAudioLengthPtr": {
                "pattern": rb"\x55\x8B\xEC\x83\xEC\x08\xA1\....\x85\xC0",
                "offset": 0x7
            },
            "userProfilePtr": {
                "pattern": rb"\xFF\x15....\xA1....\x8B\x48\x54\x33\xD2",
                "offset": 0x7
            },
            "rawLoginStatusPtr": {
                "pattern": rb"\xB8\x0B\x00\x00\x8B\x35",
                "offset": -0xb
            },
            "spectatingUserPtr": {
                "pattern": rb"\x8B\x0D\....\x85\xC0\x74\x05\x8B\x50\x30",
                "offset": -0x4
            },
            "gameTimePtr": {
                "pattern": rb"\xA1....\x89\x46\x04\x8B\xD6\xE8",
                "offset": 0x1
            }
        }

        self.patterns = {
            "baseAddr": 0,
            "playTimeAddr": 0,
            "chatCheckerPtr": 0,
            "skinDataAddr": 0,
            "settingsClassAddr": 0,
            "configurationAddr": 0,
            "bindingsAddr": 0,
            "rulesetsAddr": 0,
            "canRunSlowlyAddr": 0,
            "statusPtr": 0,
            "menuModsPtr": 0,
            "getAudioLengthPtr": 0,
            "userProfilePtr": 0,
            "rawLoginStatusPtr": 0,
            "spectatingUserPtr": 0,
            "gameTimePtr": 0
        }

    def find_offset(self, key):
        """Retrieve the pattern and offset for a given key."""
        return self.scan_patterns.get(key, None)