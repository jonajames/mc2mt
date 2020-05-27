from block_conversion import convertBlock

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
    if section["blocks"].is_empty():
        converted_section["mappings"] = ["air"]
        return converted_section

    # Loop on all blocks
    for y in range(16):
        for z in range(16):
            for x in range(16):
                # Convert block
                block = section["blocks"][coord(y,z,15-x)] # X axis is flipped
                try:
                    itemstring,param1,param2 = convertBlock(block)
                except Exception as e:
                    print("Failed converting block:",block,"\n\tReason:",type(e).__name__,e)
                if itemstring not in converted_section["mappings"]:
                    converted_section["mappings"].append(itemstring)
                # Coordinates are swapped from XZY to XYZ
                converted_section["param0"][coord(z,y,x)] = converted_section["mappings"].index(itemstring)
                converted_section["param1"][coord(z,y,x)] = param1
                converted_section["param2"][coord(z,y,x)] = param2

    # End
    return converted_section
