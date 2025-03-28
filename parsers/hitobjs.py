def findHitObject(bMap, lastObject):
    """
    Parses a beatmap file to extract hit objects and their properties.

    Args:
        bMap (str): The file path to the beatmap (.osu) file.

    Returns:
        list: A list of hit objects, where each hit object is represented as a list:
            [x, y, time, objId, holdTime]
            - x (int): X coordinate of the hit object.
            - y (int): Y coordinate of the hit object.
            - time (int): Time in milliseconds when the hit object occurs.
            - objId (int): Type of the hit object:
                0 = Circle
                1 = Slider
                2 = Spinner
            - holdTime (int): Duration of the hit object in milliseconds (20 for circles, calculated for sliders and spinners).

    Notes:
        - The function reads and parses the [Difficulty], [TimingPoints], and [HitObjects] sections of the beatmap file.
        - Slider holdTime is calculated using the slider multiplier, timing points, and slider velocity.
        - Timing points are used to determine the beat length and slider velocity multiplier.
    """
    hitObjects = []
    sliderMultiplier = 1.0
    timingPoints = []
    currentSvMultiplier = 1.0  # Default slider velocity multiplier

    with open(bMap, "r") as bMapFile:
        sections = bMapFile.read().split("\n\n")
    
    # Parse the [Difficulty] section for SliderMultiplier
    for section in sections:
        if section.startswith("[Difficulty]"):
            for line in section.splitlines():
                if line.startswith("SliderMultiplier"):
                    sliderMultiplier = float(line.split(":")[1].strip())
                    break

    # Parse the [TimingPoints] section for timing points
    for section in sections:
        if section.startswith("[TimingPoints]"):
            for line in section.splitlines()[1:]:  # Skip the [TimingPoints] header
                parts = line.split(",")
                time = int(parts[0])  # Time in ms
                beatLength = float(parts[1])  # Beat length or slider velocity
                uninherited = int(parts[6])  # 1 = inherited, 0 = uninherited
                timingPoints.append((time, beatLength, uninherited))
            break

    # Parse the [HitObjects] section for hit objects
    hitObjectsSection = ""
    for section in sections:
        if section.startswith("[HitObjects]"):
            hitObjectsSection = section.splitlines()[1:]  # Skip the [HitObjects] header
            break

    for line in hitObjectsSection:
        parts = line.split(",")
        x = int(parts[0])  # X coordinate
        y = int(parts[1])  # Y coordinate
        time = int(parts[2])  # Time in ms
        objType = int(parts[3])  # Object type (bitmask)
        holdTime = 20  # Default holdTime is 20 for circles
        
        # Determine the object type
        if objType & 1:  # Circle
            objId = 0
        elif objType & 2:  # Slider
            objId = 1
            slides = int(parts[6])  # Number of slides
            length = float(parts[7])  # Slider length

            # Find the current beat length and slider velocity multiplier
            beatLength = 500.0  # Default beat length
            currentSvMultiplier = sliderMultiplier  # Default slider velocity multiplier
            for tp in timingPoints:
                if time >= tp[0]:
                    if tp[2] == 1:  # Inherited timing point
                        beatLength = tp[1]
                    else:  # Uninherited timing point
                        currentSvMultiplier = 1.0 + (-tp[1] / 100.0)
                else:
                    break

            # Calculate holdTime based on the next object's start time
            if hitObjectsSection.index(line) + 1 < len(hitObjectsSection):  # Check if there is a next object
                nextParts = hitObjectsSection[hitObjectsSection.index(line) + 1].split(",")
                nextObjectStart = int(nextParts[2])  # Start time of the next object
                holdTime = (nextObjectStart - time) * 0.8  # Shorten by 20%
            else:
                holdTime = (lastObject - time) * 1.1  # Extend by 10%
        elif objType & 8:  # Spinner
            objId = 2
            endTime = int(parts[5])  # End time for spinner
            holdTime = endTime - time  # Spinner holdTime
        
        # Append the parsed hit object to the list
        hitObjects.append([x, y, time, objId, holdTime])
    
    return hitObjects