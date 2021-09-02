materials = {
    "acacia" : "acacia_wood",
    "andesite" : "stone",
    "birch" : "aspen_wood",
    "brick" : "brick",
    "cobblestone" : "cobble",
    "cut_red_sandstone" : "desert_stone_block",
    "cut_sandstone" : "sandstone_block",
    "dark_oak" : "wood",
    "dark_prismarine" : "ice",
    "diorite" : "silver_sandstone",
    "end_stone_brick" : "sandstonebrick",
    "granite" : "desert_cobble",
    "jungle" : "junglewood",
    "mossy_cobblestone" : "mossycobble",
    "mossy_stone_brick" : "mossycobble",
    "nether_brick" : "desert_stonebrick",
    "oak" : "wood",
    "petrified_oak" : "wood",
    "polished_andesite" : "stone_block",
    "polished_diorite" : "silver_sandstone", 
    "polished_granite" : "desert_stone_block",
    "prismarine" : "ice",
    "prismarine_brick" : "ice",
    "purpur" : "goldblock",
    "quartz" : "steelblock",
    "red_nether_brick" : "desert_stonebrick",
    "red_sandstone" : "desert_stone",
    "sandstone" : "sandstone",
    "smooth_quartz" : "steelblock",
    "smooth_red_sandstone" : "desert_stone_block",
    "smooth_sandstone" : "sandstone_block",
    "smooth_stone" : "stone_block",
    "spruce" : "pine_wood",
    "stone" : "stone",
    "stone_brick" : "stonebrick",
}

# Materials
def id2material(block):
    parts = block.id.split("_")
    for i in range(1,len(parts)):
        key_part = ("_".join(parts[:i]))
        if key_part in materials: return materials[key_part]
    for i in range(1,len(parts)):
        key_part = ("_".join(parts[i:]))
        if key_part in materials: return materials[key_part]
    return "wood"

# Flowing Liquids
def level2flowingliquid(block):
    return int(str(block.properties["level"]))//2

# Facedir
def rotation2facedir(block):
    return {
        "15":1,"0":1,"1":1,"2":1,
        "3":2,"4":2,"5":2,"6":2,
        "7":3,"8":3,"9":3,"10":3,
        "11":4,"12":4,"13":4,"14":4,
    }.get(str(block.properties["rotation"]),0)

def cardinal2facedir(block):
    if str(block.properties['north'])=='true': return 0
    if str(block.properties['south'])=='true': return 1
    if str(block.properties['east'])=='true': return 2
    if str(block.properties['west'])=='true': return 3
    return 0

def cardinalVine2facedir(block):
    if str(block.properties['north'])=='true': return 5
    if str(block.properties['south'])=='true': return 4
    if str(block.properties['east'])=='true': return 3
    if str(block.properties['west'])=='true': return 2
    if str(block.properties['up'])=='true': return 0
    return 0

def type2facedir(block):
    return {
        "bottom":0,"top":20,"double":0
    }.get(str(block.properties["type"]),0)

def facing2facedir(block):
    return {
        "north":2,"east":3,"south":0,"west":1,"up":4,"down":8
    }.get(str(block.properties["facing"]),0)

def carpetFacing2facedir(block):
    return {
        "north":8,"east":16,"south":4,"west":12
    }.get(str(block.properties["facing"]),0)

# Wallmounted
def facing2wallmounted(block):
    return {
        "north":4,"east":2,"south":5,"west":3
    }.get(str(block.properties["facing"]),0)

# Stairs
def stair2facedir(block):
    if str(block.properties["shape"]) in ["straight","inner_left","outer_left"]:
        return {
            "north":4,"east":3,"south":0,"west":1
        }.get(str(block.properties["facing"]),0) + {
            "top":20,"bottom":0
        }.get(str(block.properties["half"]),0)
    else:
        return {
            "north":0,"east":4,"south":1,"west":2
        }.get(str(block.properties["facing"]),0) + {
            "top":20,"bottom":0
        }.get(str(block.properties["half"]),0)

def shape2stair(block):
    return "stairs:stair" + {
        "straight":"",
        "outer_right":"_outer",
        "outer_left":"_outer",
        "inner_right":"_inner",
        "inner_left":"_inner"
    }.get(str(block.properties["shape"]),"") +\
    "_" + id2material(block)

def material2slab(block):
    return "stairs:slab_" + id2material(block)

# Doors
def door2ab(block):
    if str(block.properties["half"]) == "upper": return "air"
    material = "iron" in block.id and "steel" or "wood"
    return "doors:door_" + material + {
        ("true","right"):"_a",
        ("true","left"):"_b",
        ("false","left"):"_a",
        ("false","right"):"_b"
    }.get((str(block.properties["open"]),str(block.properties["hinge"])),"_a")

def door2facedir(block):
    return ( {
        "north":2,"east":3,"south":0,"west":1
    }.get(str(block.properties["facing"]),0) + {
        "true":0,"false":1
    }.get(str(block.properties["open"]),0) * {
        "right":-1,"left":1
    }.get(str(block.properties["hinge"]),0) ) % 4

# Print
def print_block(prefix,block):
    properties = {}
    for p in block.properties:
        properties[p] = str(block.properties[p])
    print(f"{prefix}~{block.id}~{properties}")
