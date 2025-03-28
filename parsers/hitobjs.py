def find_hitobject(bmap):
    """
    Parses a beatmap file to extract hit objects and their properties.

    Args:
        bmap (str): The file path to the beatmap (.osu) file.

    Returns:
        list: A list of hit objects, where each hit object is represented as a list:
            [x, y, time, obj_id, holdtime]
            - x (int): X coordinate of the hit object.
            - y (int): Y coordinate of the hit object.
            - time (int): Time in milliseconds when the hit object occurs.
            - obj_id (int): Type of the hit object:
                0 = Circle
                1 = Slider
                2 = Spinner
            - holdtime (int): Duration of the hit object in milliseconds (20 for circles, calculated for sliders and spinners).

    Notes:
        - The function reads and parses the [Difficulty], [TimingPoints], and [HitObjects] sections of the beatmap file.
        - Slider holdtime is calculated using the slider multiplier, timing points, and slider velocity.
        - Timing points are used to determine the beat length and slider velocity multiplier.
    """
    hit_objects = []
    slider_multiplier = 1.0
    timing_points = []
    current_sv_multiplier = 1.0  # Default slider velocity multiplier

    with open(bmap, "r") as bmap_file:
        sections = bmap_file.read().split("\n\n")
    
    # Parse the [Difficulty] section for SliderMultiplier
    for section in sections:
        if section.startswith("[Difficulty]"):
            for line in section.splitlines():
                if line.startswith("SliderMultiplier"):
                    slider_multiplier = float(line.split(":")[1].strip())
                    break

    # Parse the [TimingPoints] section for timing points
    for section in sections:
        if section.startswith("[TimingPoints]"):
            for line in section.splitlines()[1:]:  # Skip the [TimingPoints] header
                parts = line.split(",")
                time = int(parts[0])  # Time in ms
                beat_length = float(parts[1])  # Beat length or slider velocity
                uninherited = int(parts[6])  # 1 = inherited, 0 = uninherited
                timing_points.append((time, beat_length, uninherited))
            break

    # Parse the [HitObjects] section for hit objects
    hitObjects = ""
    for section in sections:
        if section.startswith("[HitObjects]"):
            hitObjects = section.splitlines()[1:]  # Skip the [HitObjects] header
            break

    for line in hitObjects:
        parts = line.split(",")
        x = int(parts[0])  # X coordinate
        y = int(parts[1])  # Y coordinate
        time = int(parts[2])  # Time in ms
        obj_type = int(parts[3])  # Object type (bitmask)
        holdtime = 20  # Default holdtime is 20 for circles
        
        # Determine the object type
        if obj_type & 1:  # Circle
            obj_id = 0
        elif obj_type & 2:  # Slider
            obj_id = 1
            slides = int(parts[6])  # Number of slides
            length = float(parts[7])  # Slider length

            # Find the current beat length and slider velocity multiplier
            beat_length = 500.0  # Default beat length
            for tp in timing_points:
                if time >= tp[0]:
                    if tp[2] == 1:  # Inherited timing point
                        beat_length = tp[1]
                    else:  # Uninherited timing point
                        current_sv_multiplier = -tp[1] / 100.0
                else:
                    break

            # Calculate holdtime using the formula
            holdtime = int((length / (slider_multiplier * 100 * current_sv_multiplier)) * beat_length * slides)
        elif obj_type & 8:  # Spinner
            obj_id = 2
            end_time = int(parts[5])  # End time for spinner
            holdtime = end_time - time  # Spinner holdtime
        
        # Append the parsed hit object to the list
        hit_objects.append([x, y, time, obj_id, holdtime])
    
    return hit_objects