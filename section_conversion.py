import block_conversion

def coord(z,y,x):
    return (z<<8) | (y<<4) | x 

def convertSection(section):
    converted_section = {
        'pos' : (0,0,0),
        'param0' : [0]*4096,
        'param1' : [255]*4096,
        'param2' : [0]*4096,
        'mappings' : [],
    }
    
    # Convert block coordinates
    r,chunk_x,chunk_z,mca = section["mca"].split(".")
    chunk_x = (-int(chunk_x) << 5) | (31-section['x']) # X axis is flipped
    chunk_z = (int(chunk_z) << 5) | section['z']
    converted_section["pos"] = (chunk_x,section['y'],chunk_z)

    # Skip if empty
    try:
        if section["blocks"].is_empty():
            converted_section["mappings"] = ["air"]
            return converted_section
    except Exception as e:
        #print("Failed reading section:",chunk_x,chunk_z)
        #print("\tReason:",type(e).__name__,e)
        #print("\tSection is probably empty")
        converted_section["mappings"] = ["air"]
        return converted_section

    # Loop on all blocks
    for y in range(16):
        for z in range(16):
            for x in range(16):
                # Convert block
                block = section["blocks"][coord(y,z,15-x)] # X axis is flipped
                try:
                    itemstr,param1,param2 = block_conversion.convertBlock(block)
                except Exception as e:
                    print("Failed converting block:",block)
                    print("\tReason:",type(e).__name__,e)
                if itemstr not in converted_section["mappings"]:
                    converted_section["mappings"].append(itemstr)
                # Coordinates are swapped from XZY to XYZ
                param0 = converted_section["mappings"].index(itemstr)
                converted_section["param0"][coord(z,y,x)] = param0
                converted_section["param1"][coord(z,y,x)] = param1
                converted_section["param2"][coord(z,y,x)] = param2

    # End
    return converted_section
