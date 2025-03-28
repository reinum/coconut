import pymem
import pymem.process
import pymem.pattern

# Open the target process (make sure to run with the appropriate privileges)
pm = pymem.Pymem("osu!.exe")

# Get the module object for the target process
module = pymem.process.module_from_name(pm.process_handle, "osu!.exe")

# Define your byte pattern
pattern = rb"\xF8\x01\x74\x04\x83\x65"

# Use the module object directly in the pattern scan
address = pymem.pattern.pattern_scan_module(pm.process_handle, module, pattern)

if address:
    print(f"Pattern found at: {hex(address)}")
else:
    print("Pattern not found.")
