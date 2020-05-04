def convertSection(section,convert_block_function):
    converted_section = {
        'pos' : 0,
        'param0' : [0]*4096,
        'param1' : [15]*4096,
        'param2' : [0]*4096,
        'mappings' : [],
    }
    
    # Convert block coordinates
    def getBlockAsInteger(x,y,z):
        u = z*16777216 + y*4096 + x
        while u >= 2**63: u -= 2**64
        while u <= -2**63: u += 2**64
        return u
    chunk_pos = section["mca"].split(".")
    assert(chunk_pos[3]=="mca")
    converted_section["pos"] = getBlockAsInteger(
        section['x'] + int(chunk_pos[1])*32,
        section['y'] - 10,
        section['z'] + int(chunk_pos[2])*32,
    )

    # Skip if empty
    if section["blocks"].is_empty():
        converted_section["mappings"] = ["air"]
        return converted_section

    # Loop on all blocks
    for y in range(16):
        for z in range(16):
            for x in range(16):
                try:
                    itemstring,param1,param2 = convert_block_function(section["blocks"][y*256+z*16+x])
                except Exception as e:
                    print("Conversion of block",section["blocks"][y*256+z*16+x],"failed with",e)
                if itemstring not in converted_section["mappings"]:
                    converted_section["mappings"].append(itemstring)
                # Coordinates are swapped from XZY to XYZ
                converted_section["param0"][z*256+y*16+x] = converted_section["mappings"].index(itemstring)
                converted_section["param1"][z*256+y*16+x] = param1
                converted_section["param2"][z*256+y*16+x] = param2

    # End
    return converted_section
